from __future__ import annotations

import logging
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Union
from urllib.request import urlopen

import boto3
import botocore
from typeguard import typechecked

from ..base_path import BasePath
from ..configs import Configs
from ..helpers.getattr_safe_property import getattr_safe_property
from ..helpers.responses import (
    DeleteResponse,
    HeadResponse,
    VersionsResponse,
    WriteResponse,
)
from ..helpers.utils import (
    DEFAULT_S3_RETRIES,
    DEFAULT_S3_TIMEOUT,
    convert_storage_unit,
    list_by_thousands,
)

if TYPE_CHECKING:
    from ..helpers.enums import ClientTypeEnum

logger = logging.getLogger("allonias3.boto_path")


class BotoPath(BasePath):
    """Use this class to interact with S3 using boto3."""

    CONFIG: ClassVar[dict] = {}
    CLIENT_TYPE: ClassVar[ClientTypeEnum] = "boto"
    """So you can check you are using the client you wanted"""
    _S3Error = botocore.exceptions.ClientError

    # Class methods

    @classmethod
    def _initialize(cls) -> None:
        key = (
            Configs.instance.USER_TOKEN_ID,
            Configs.instance.USER_TOKEN_SECRET,
        )
        if cls._KEY is None or key != cls._KEY:
            # Remove clients corresponding to old creds

            boto_config = {
                "retries": {"max_attempts": DEFAULT_S3_RETRIES + 1},
                "read_timeout": DEFAULT_S3_TIMEOUT,
                "connect_timeout": DEFAULT_S3_TIMEOUT,
            }
            # override any previous value with the user-set config
            boto_config.update(**cls.CONFIG)
            boto_config = botocore.config.Config(**boto_config)

            cls._CLIENT = boto3.client(
                "s3",
                use_ssl=False,
                endpoint_url=Configs.instance.s3_proxy_url,
                aws_access_key_id=key[0],
                aws_secret_access_key=key[1],
                config=boto_config,
            )
            # test the connection using a lightweight head_bucket call
            bucket = Configs.instance.persistent_bucket_name
            try:
                cls._CLIENT.head_bucket(Bucket=bucket)
            except botocore.exceptions.ClientError as error:
                raise NotADirectoryError(
                    f"Bucket {bucket} does not exist."
                ) from error
            cls._KEY = key

    def _check_existing_type(self):
        try:
            existing_type = self.head().type
            if not existing_type:
                existing_type = "unknown"
            if existing_type != self.object_type:
                raise TypeError(
                    f"{self.str_persistent} {self} already exists with type "
                    f"'{existing_type}'."
                )
        except botocore.exceptions.ClientError as error:
            if (
                error.response.get("ResponseMetadata", {})
                .get("HTTPHeaders", {})
                .get("x-amz-delete-marker", False)
            ):
                # File is deleted, so no type conflict
                return
            if error.response["Error"]["Code"] == "404":
                # File does not exist, so no type conflict
                return
            raise error

    def _get_object(self, version_id: Union[str, None]) -> dict:
        return (
            self.client.get_object(
                Bucket=self.bucket, Key=str(self), VersionId=version_id
            )
            if version_id
            else self.client.get_object(Bucket=self.bucket, Key=str(self))
        )

    def _close_response(self) -> None:
        pass

    def _write_default(self, content, **write_kwargs) -> dict:
        content = self._Encoder(
            str(self), self.encoding, deactivate=not self.handle_type
        )(content, **write_kwargs)
        response = self.client.put_object(
            Bucket=self.bucket,
            Key=str(self),
            Body=content,
            Metadata={
                "type": self.object_type,
                "author": str(Configs.instance.user_id)
                if Configs.instance.user_id
                else "",
            },
        )
        response["Key"] = str(self)
        response["Bucket"] = self.bucket
        response["LastModified"] = self.head(
            version_id=response["VersionId"]
        ).last_modified
        return response

    def _append(
        self, content, read_kwargs, write_kwargs, append_kwargs
    ) -> dict:
        existing_content = self.read(**read_kwargs)
        content = self._Appender(
            str(self), self.encoding, deactivate=not self.handle_type
        )(
            existing_content,
            content,
            write_kwargs=write_kwargs,
            append_kwargs=append_kwargs,
        )
        response = self.client.put_object(
            Bucket=self.bucket,
            Key=str(self),
            Body=content,
            Metadata={"type": self.object_type},
        )
        response["Key"] = str(self)
        response["Bucket"] = self.bucket
        return response

    def _write_pathlib(self, content: Path) -> dict:
        self.client.upload_file(
            str(content),
            self.bucket,
            str(self),
            ExtraArgs={
                "Metadata": {
                    "type": self.object_type,
                    "author": str(Configs.instance.user_id)
                    if Configs.instance.user_id
                    else "",
                }
            },
        )
        return self.head().to_dict()

    def _write_url(self, content: str, timeout: int) -> dict:
        response = self.client.put_object(
            Bucket=self.bucket,
            Key=str(self),
            Body=urlopen(content, timeout=timeout).read(),  # nosec
            Metadata={
                "type": self.object_type,
                "author": str(Configs.instance.user_id)
                if Configs.instance.user_id
                else "",
            },
        )
        response["Key"] = str(self)
        response["Bucket"] = self.bucket
        return response

    def _put_object(self, body: str) -> dict:
        response = self.client.put_object(
            Bucket=self.bucket, Key=str(self), Body=body.encode(self.encoding)
        )
        response["Key"] = str(self)
        response["Bucket"] = self.bucket
        return response

    def _copy_object(
        self, destination: BotoPath, version_id: Union[str, None] = None
    ) -> dict:
        response = self.client.copy_object(
            Bucket=destination.bucket,
            Key=str(destination),
            CopySource={
                "Bucket": self.bucket,
                "Key": str(self),
                "VersionId": version_id,
            }
            if version_id
            else {
                "Bucket": self.bucket,
                "Key": str(self),
            },
        )
        response["Key"] = str(destination)
        response["Bucket"] = str(destination.bucket)
        response["LastModified"] = response.pop("CopyObjectResult", {}).get(
            "LastModified"
        )
        return response

    def _download(
        self,
        localpath: str | Path | None = None,
        version_id: Union[str, None] = None,
    ):
        content = self._Encoder(
            str(self), encoding=self.encoding, deactivate=not self.handle_type
        )(self.read(version_id=version_id))
        open_mode = "wb" if isinstance(content, bytes) else "w"

        with Path(localpath).open(open_mode) as f:
            f.write(content)
        if self.verbose:
            logger.info(f"Copied {self.str_persistent} {self} to {localpath}.")

    def _upload(self, localpath: Path) -> WriteResponse:
        decoder = self._Decoder(
            str(self),
            self.encoding,
            deactivate=not self.handle_type,
            raise_if_unpickle_fails=False,
        )
        content = decoder({"LocalPath": str(localpath)})
        response = self.write(content)
        decoder.close()
        return response

    def _delete_one(self, version_id: Union[str, None]) -> dict:
        result = (
            self.client.delete_object(
                Bucket=self.bucket, Key=str(self), VersionId=version_id
            )
            if version_id
            else self.client.delete_object(Bucket=self.bucket, Key=str(self))
        )
        result["Key"] = str(self)
        if version_id is None and result["DeleteMarker"]:
            result["DeleteMarkerVersionId"] = result.pop("VersionId")
        return {"Deleted": [result]}

    def _delete_all(self) -> dict:
        delete_objects = [
            {"Key": str(self), "VersionId": version}
            for version in self.versions(include_deleted=True)
        ]
        return self.client.delete_objects(
            Bucket=self.bucket, Delete={"Objects": delete_objects}
        )

    # Properties

    @cached_property
    @getattr_safe_property
    def versioned(self) -> bool:
        """Is the bucket the file is in versioned?"""
        return (
            self.client.get_bucket_versioning(Bucket=self.bucket).get("Status")
            == "Enabled"
        )

    # Methods using the S3 client or an API

    # Methods reading stuff from S3 or an API

    @typechecked
    def versions(
        self,
        include_deleted: bool = False,
        details: bool = False,
    ) -> VersionsResponse | list[str]:
        """list all the versions of this S3Path.

        The most recent appears first.

        Args:
            include_deleted: If False (default), ignores delete marekrs. Else,
                includes them.
            details: In that case,
                returns a
                :obj:`~allonias3.helpers.responses.VersionsResponse`

        Returns:
            :
                return a list of version uuids if details is False or a
                    :obj:`~allonias3.helpers.responses.VersionsResponse`
        """
        if not self.versioned:
            logger.warning("This S3Path is not on a versioned bucket")
            return VersionsResponse({}, True)
        response = list_by_thousands(
            "list_object_versions",
            self.client,
            Bucket=self.bucket,
            Prefix=str(self),
        )
        response = VersionsResponse(response, not include_deleted)
        return response if details else response.simple

    @typechecked
    def is_file(
        self, include_deleted: bool = False, version_id: Union[str, None] = None
    ) -> bool:
        try:
            self.client.head_object(
                Bucket=self.bucket, Key=str(self), VersionId=version_id
            ) if version_id else self.client.head_object(
                Bucket=self.bucket, Key=str(self)
            )
        except botocore.exceptions.ClientError as error:
            if (
                error.response.get("ResponseMetadata", {})
                .get("HTTPHeaders", {})
                .get("x-amz-delete-marker", "false")
                == "true"
            ):
                return include_deleted
            # 405 is Method Not Allowd, happens when trying to head a
            # delete marker by giving its version_id explicitely
            # Invalid version (like, not a UUID) will raise 404 with boto3
            if error.response["Error"]["Code"] in ("404", "405"):
                return False
            raise error
        else:
            return True

    def is_dir(self, check_s3keep: bool = False) -> bool:
        """Check that this S3Path is a directory on S3.

        It is a directory if it contains something (i.e. listing its content
        returns something) or if it is a bucket.

        Args:
            check_s3keep: If True, even if there is some content, the path is
              not seen as a directory unless it contains a .s3keep file.
        """
        if not str(self):
            # Is a bucket, considered a directory unless we specifically want
            # .s3keep files (which are not created in the bucket itself)
            return not check_s3keep
        isdir = (
            self.client.list_objects_v2(
                Bucket=self.bucket, Prefix=f"{self}/", MaxKeys=1
            ).get("Contents")
            is not None
        )
        if not isdir:
            return False
        if check_s3keep and not (self / ".s3keep").is_file():
            return False
        return True

    def head(self, version_id: Union[str, None] = None) -> HeadResponse:
        """Retrieve information about the latest version of the object.

        If the latest version is a delete marker, NoSuchKey is raised.
        """
        response = (
            self.client.head_object(
                Bucket=self.bucket, Key=str(self), VersionId=version_id
            )
            if version_id
            else self.client.head_object(Bucket=self.bucket, Key=str(self))
        )
        response["Key"] = str(self)
        response["Bucket"] = self.bucket
        response["author"] = response.get("Metadata", {}).get("author", "")
        if not response["author"]:
            response["author"] = (
                response.get("Metadata", {})
                .get("ResponseMetadata", {})
                .get("HTTPHeaders", {})
                .get("x-amz-meta-author", "")
            )
        response["type"] = response["Metadata"].get("type")
        if not response["type"]:
            response["type"] = (
                response.get("Metadata", {})
                .get("ResponseMetadata", {})
                .get("HTTPHeaders", {})
                .get("x-amz-meta-type")
            )
        return HeadResponse(response)

    @typechecked
    def size(
        self,
        unit: str = "MB",
        binary_base: bool = True,
        version_id: Union[str, None] = None,
    ) -> float:
        """
        Get the file size in 'unit'.

        Args:
            unit: "B", "MB", "kB", "GB", "TB" or "PB".
                The unit in which you want the result.
            binary_base: If True (default), kB is kibibytes (1024 Bytes), MB is
                minibytes (1024^2 bytes), etc... this is the convention used on
                S3. If you would rather have it in base 10 (kB is kilobytes,
                1000 Bytes, etc...), set this argument to False.
            version_id: to get the size of a specific version of a file.
        """
        response = (
            self.client.head_object(
                Bucket=self.bucket, Key=str(self), VersionId=version_id
            )
            if version_id
            else self.client.head_object(Bucket=self.bucket, Key=str(self))
        )
        return convert_storage_unit(
            response["ContentLength"], to_unit=unit, binary_base=binary_base
        )

    @typechecked
    def content(
        self,
        show_files: bool = True,
        show_hidden: bool = False,
        show_directories: bool = False,
        recursive: bool = True,
    ) -> list[BotoPath]:
        """Lists the content of this directory.

        Depending on the given arguments, can also list subdirectories, only
        subdirectories, hidden files, do it recursively (default) or not.

        The result is not guaranteed to be in the same order as when using
        Minio.

        Args:
            show_hidden: show hidden objects (starting with '.')
            show_files: If :obj:`True` (default), list files
            show_directories: If :obj:`True` (not default) will list directories
            recursive: If :obj:`True` (default), list the content of
                subdirectories
        """
        found = []
        res_list_objs = list_by_thousands(
            "list_objects_v2",
            self.client,
            Bucket=self.bucket,
            Prefix=f"{self}/" if str(self) else "",
        )

        for key in res_list_objs.get("Contents", []):
            path = self.__class__(key["Key"], **self.kwargs)
            if path.name == ".s3keep":
                if path.parent == self or not show_directories:
                    continue
                path = path.parent
            elif not show_files:
                continue

            if (not path.hidden or show_hidden) and (
                recursive or path.parent == self
            ):
                found.append(path)

        return found

    # Methods creating/deleting stuff on S3

    @typechecked
    def rmdir(
        self,
        recursive: bool = False,
        permanently: bool = True,
    ) -> DeleteResponse:
        """Deletes a directory from the S3 bucket.

        Note that if the s3path points to the bucket, the function will refuse
        to execute. To delete the content of a bucket, loop over its content
        and delete each item individualy. This is done for security reasons.

        Args:
            recursive: recursively delete all files and subdirectories.
            permanently: If :obj:`False`, the object is only tagged
                as 'deleted'. It is not visible anymore, but still exists and
                could be restored. Otherwise (default), it is completely and
                definitely deleted along with all its versions. Useless if
                version_id is specified.
        """
        if errors := self._check_rmdir_inputs():
            return errors

        content = list_by_thousands(
            "list_objects_v2",
            self.client,
            Bucket=self.bucket,
            Prefix=f"{self}/",
        ).get("Contents")

        empty = len(content) == 1 and Path(content[0]["Key"]).name == ".s3keep"

        if not empty and not recursive:
            message = f"Directory '{self}' is not empty."
            if self.verbose:
                logger.error(message)
            return DeleteResponse(
                {
                    "Errors": [
                        {
                            "Key": str(self),
                            "VersionId": None,
                            "Code": "FileExistsError",
                            "Message": message,
                        }
                    ]
                }
            )

        delete_objects = []
        for obj in content:
            if permanently and self.versioned:
                versions = BotoPath(
                    obj["Key"], persistent=self.persistent
                ).versions()
                delete_objects += [
                    {"Key": obj["Key"], "VersionId": version}
                    for version in versions
                ]
            else:
                delete_objects.append({"Key": obj["Key"]})
        response = self.client.delete_objects(
            Bucket=self.bucket, Delete={"Objects": delete_objects}
        )
        if self.verbose:
            if not response.get("Errors"):
                logger.info(f"Deleted {self.str_persistent} directory {self}.")
            else:
                logger.error(
                    f"One or more error occured while deleting"
                    f" {self.str_persistent} directory {self}. Check the"
                    f" returned response for more details."
                )
        return DeleteResponse(response)
