from __future__ import annotations

import logging
from functools import cached_property
from io import BytesIO
from mimetypes import guess_type
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Union

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
from urllib.request import urlopen

from minio.commonconfig import CopySource
from minio.deleteobjects import DeleteError, DeleteObject, DeleteResult
from minio.error import S3Error
from typeguard import typechecked
from urllib3 import PoolManager, Retry

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
    DEFAULT_PART_SIZE,
    DEFAULT_S3_RETRIES,
    DEFAULT_S3_TIMEOUT,
    convert_storage_unit,
)
from .helpers import Minio

if TYPE_CHECKING:
    from minio.helpers import ObjectWriteResult

    from ..helpers.enums import ClientTypeEnum

logger = logging.getLogger("allonias3.minio_path")


class MinioPath(BasePath):
    """Use this class to interact with S3 using Minio."""

    CONFIG: ClassVar[PoolManager] = PoolManager(
        # 0 to turn off retries
        retries=Retry(
            total=DEFAULT_S3_RETRIES,
            backoff_factor=0.2,
            status_forcelist=[500, 502, 503, 504],
        ),
        timeout=DEFAULT_S3_TIMEOUT,
    )
    CLIENT_TYPE: ClassVar[ClientTypeEnum] = "minio"
    """So you can check you are using the client you wanted"""
    _S3Error = S3Error

    def __init__(
        self,
        path: Self | Path | Union[str, None] = "",
        persistent: bool = True,
        verbose: bool = True,
        encoding: str = "utf-8",
        handle_type: bool | None = None,
        object_type: Union[str, None] = None,
    ):
        super().__init__(
            path=path,
            persistent=persistent,
            verbose=verbose,
            encoding=encoding,
            handle_type=handle_type,
            object_type=object_type,
        )
        self.__response = None

    # Class methods

    @classmethod
    def _initialize(cls) -> None:
        key = (
            Configs.instance.USER_TOKEN_ID,
            Configs.instance.USER_TOKEN_SECRET,
        )
        if cls._KEY is None or key != cls._KEY:
            # Remove clients corresponding to old creds
            s3_proxy_url = (
                (
                    Configs.instance.s3_proxy_url.replace("https://", "")
                    .replace("http://", "")
                    .rstrip("/")
                )
                if Configs.instance.s3_proxy_url
                else ""
            )

            cls._CLIENT = Minio(
                s3_proxy_url,
                secure=False,
                access_key=key[0],
                secret_key=key[1],
                region=Configs.instance.REGION_NAME,
                http_client=cls.CONFIG,
            )
            bucket = Configs.instance.persistent_bucket_name
            if not cls._CLIENT.bucket_exists(bucket_name=bucket):
                raise NotADirectoryError(f"Bucket {bucket} does not exist.")
            cls._KEY = key

    # Properties

    @cached_property
    @getattr_safe_property
    def versioned(self) -> bool:
        """Is the bucket the file is in versioned?"""
        return (
            self.client.get_bucket_versioning(bucket_name=self.bucket).status
            == "Enabled"
        )

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
        except S3Error as error:
            if error.code == "NoSuchKey":
                # File does not exist, so no type conflict
                return
            raise error

    def _get_object(self, version_id: Union[str, None]) -> dict:
        self.__response = (
            self.client.get_object(
                bucket_name=self.bucket,
                object_name=str(self),
                version_id=version_id,
            )
            if version_id
            else self.client.get_object(
                bucket_name=self.bucket,
                object_name=str(self),
            )
        )
        return {"Body": self.__response.data}

    def _close_response(self) -> None:
        if self.__response:
            self.__response.close()
            self.__response.release_conn()

    def _write_default(self, content, **write_kwargs) -> ObjectWriteResult:
        content = self._Encoder(
            str(self), self.encoding, deactivate=not self.handle_type
        )(content, **write_kwargs)
        return self.client.put_object(
            bucket_name=self.bucket,
            object_name=str(self),
            data=BytesIO(content)
            if not isinstance(content, BytesIO)
            else content,
            length=-1,
            part_size=DEFAULT_PART_SIZE,
            metadata={
                "type": self.object_type,
                "author": str(Configs.instance.user_id)
                if Configs.instance.user_id
                else "",
            },
        )

    def _append(
        self, content, read_kwargs, write_kwargs, append_kwargs
    ) -> ObjectWriteResult:
        existing_content = self.read(**read_kwargs)
        content = self._Appender(
            str(self), self.encoding, deactivate=not self.handle_type
        )(
            existing_content,
            content,
            write_kwargs=write_kwargs,
            append_kwargs=append_kwargs,
        )
        # Do not use compose object to allow the use of pd.concat with specified
        # kwargs
        return self.client.put_object(
            bucket_name=self.bucket,
            object_name=str(self),
            data=BytesIO(content)
            if not isinstance(content, BytesIO)
            else content,
            length=-1,
            part_size=DEFAULT_PART_SIZE,
            metadata={"type": self.object_type},
        )

    def _write_pathlib(self, content: Path) -> ObjectWriteResult:
        return self.client.fput_object(
            bucket_name=self.bucket,
            object_name=str(self),
            file_path=content,
            metadata={
                "type": self.object_type,
                "author": str(Configs.instance.user_id)
                if Configs.instance.user_id
                else "",
            },
        )

    def _write_url(self, content: str, timeout: int) -> ObjectWriteResult:
        mime = guess_type(content)
        return self.client.put_object(
            bucket_name=self.bucket,
            object_name=str(self),
            data=urlopen(content, timeout=timeout).read(),  # nosec
            content_type=mime[0],
            length=-1,
            part_size=DEFAULT_PART_SIZE,
            metadata={
                "type": self.object_type,
                "content-encoding": mime[1],
                "author": str(Configs.instance.user_id)
                if Configs.instance.user_id
                else "",
            },
        )

    def _put_object(self, body: str) -> ObjectWriteResult:
        return self.client.put_object(
            bucket_name=self.bucket,
            object_name=str(self),
            data=BytesIO(body.encode(self.encoding)),
            length=len(body),
        )

    def _copy_object(
        self, destination: BasePath, version_id: Union[str, None] = None
    ) -> ObjectWriteResult:
        return self.client.copy_object(
            destination.bucket,
            str(destination),
            CopySource(self.bucket, str(self), version_id=version_id)
            if version_id
            else CopySource(self.bucket, str(self)),
        )

    def _download(
        self,
        localpath: str | Path | None = None,
        version_id: Union[str, None] = None,
    ) -> None:
        self.client.fget_object(
            bucket_name=self.bucket,
            object_name=str(self),
            file_path=localpath,
            version_id=version_id,
        ) if version_id else self.client.fget_object(
            bucket_name=self.bucket,
            object_name=str(self),
            file_path=localpath,
        )
        if self.verbose:
            logger.info(
                f"Copied {self.str_persistent} {self} to {localpath}.",
            )

    def _upload(self, localpath: Path) -> WriteResponse:
        return self.write(localpath)

    def _delete_one(self, version_id: Union[str, None]) -> DeleteResult:
        return (
            self.client.custom_remove_object(
                bucket_name=self.bucket,
                object_name=str(self),
                version_id=version_id,
            )
            if version_id
            else self.client.custom_remove_object(
                bucket_name=self.bucket, object_name=str(self)
            )
        )

    def _delete_all(self) -> DeleteResult:
        delete_objects = (
            DeleteObject(obj.object_name, obj.version_id)
            for obj in self.client.custom_list_objects(
                bucket_name=self.bucket,
                prefix=str(self),
                delimiter="/",
                restrict_to_prefix=True,
                include_version=True,
            )
        )
        return self.client.custom_remove_objects(
            bucket_name=self.bucket,
            delete_object_list=delete_objects,
        )

    @typechecked
    def versions(
        self,
        include_deleted: bool = False,
        details: bool = False,
    ) -> VersionsResponse | list[str]:
        """list all the versions of this S3Path.

        The most recent appears first.

        Args:
            include_deleted: If False (default), ignores delete markers. Else,
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
        response = self.client.custom_list_objects(
            bucket_name=self.bucket,
            prefix=str(self),
            delimiter="/",
            restrict_to_prefix=True,
            include_version=True,
        )
        response = VersionsResponse(response, not include_deleted)
        return response if details else response.simple

    @typechecked
    def is_file(
        self, include_deleted: bool = False, version_id: Union[str, None] = None
    ) -> bool:
        """
        Checks that this S3Path is a file on S3.

        Args:
            include_deleted: If False (default), deleted versioned objects
                appear not to exist. Else, they do.
            version_id: to check the existence of a specific version
        """
        try:
            obj = (
                self.client.stat_object(
                    bucket_name=self.bucket,
                    object_name=str(self),
                    version_id=version_id,
                )
                if version_id
                else self.client.stat_object(
                    bucket_name=self.bucket,
                    object_name=str(self),
                )
            )
        except S3Error as error:
            # the specified version is a delete marker
            if error.code in "MethodNotAllowed":
                return include_deleted
            if (
                error.response.headers.get("x-amz-delete-marker", "false")
                == "true"
            ):
                return include_deleted
            if error.code in (
                "NoSuchKey",
                "NoSuchVersion",  # file exists but version not found
                "InvalidArgument",  # version is not valid (not a UUID-like str)
            ):
                return False
            raise error
        else:
            return not (obj.is_delete_marker and not include_deleted)

    @typechecked
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
        try:
            # No need for the custom _list_objects generator here
            next(
                self.client._list_objects(  # noqa: SLF001
                    bucket_name=self.bucket, prefix=f"{self}/", delimiter="/"
                )
            )
        except StopIteration:
            return False
        if check_s3keep and not (self / ".s3keep").is_file():
            return False
        return True

    def head(self, version_id: Union[str, None] = None) -> HeadResponse:
        response = (
            self.client.stat_object(
                bucket_name=self.bucket,
                object_name=str(self),
                version_id=version_id,
            )
            if version_id
            else self.client.stat_object(
                bucket_name=self.bucket, object_name=str(self)
            )
        )
        response.type = response.metadata.get("type")
        if not response.type:
            response.type = response.metadata.get("x-amz-meta-type")
        response.author = response.metadata.get("author", "")
        if not response.author:
            response.author = response.metadata.get("x-amz-meta-author", "")
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
        obj = (
            self.client.stat_object(
                bucket_name=self.bucket,
                object_name=str(self),
                version_id=version_id,
            )
            if version_id
            else self.client.stat_object(
                bucket_name=self.bucket, object_name=str(self)
            )
        )
        return convert_storage_unit(
            obj.size, to_unit=unit, binary_base=binary_base
        )

    @typechecked
    def content(
        self,
        show_files: bool = True,
        show_hidden: bool = False,
        show_directories: bool = False,
        recursive: bool = True,
    ) -> list[MinioPath]:
        """Lists the content of this directory.

        Depending on the given arguments, can also list subdirectories, only
        subdirectories, hidden files, do it recursively (default) or not.

        The result is not guaranteed to be in the same order as when using
        Boto.

        Args:
            show_hidden: show hidden objects (starting with '.')
            show_files: If :obj:`True` (default), list files
            show_directories: If :obj:`True` (not default) will list directories
            recursive: If :obj:`True` (default), list the content of
                subdirectories
        """
        found = []
        res_list_objs = self.client.custom_list_objects(
            bucket_name=self.bucket,
            prefix=f"{self}/" if str(self) else "",
            delimiter=None,
        )

        for key in res_list_objs:
            path = self.__class__(key.object_name, **self.kwargs)
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
                could be restored. Otherwise, it is completely and
                definitely deleted along with all its versions. Useless if
                version_id is specified.
        """
        if errors := self._check_rmdir_inputs():
            return errors

        content = self.client.custom_list_objects(
            bucket_name=self.bucket,
            prefix=f"{self}/",
            delimiter=None,
        )

        try:
            first_item = next(content)
            try:
                second_item = next(content)
            except StopIteration:
                second_item = None
        except StopIteration:
            first_item = None
            second_item = None

        empty = first_item is None or (
            Path(first_item.object_name).name == ".s3keep"
            and second_item is None
        )

        if not empty and not recursive:
            message = f"Directory '{self}' is not empty."
            logger.error(message)
            return DeleteResponse(
                DeleteResult(
                    [],
                    [
                        DeleteError(
                            code="FileExistsError",
                            message=message,
                            name=str(self),
                            version_id=None,
                        )
                    ],
                )
            )

        delete_objects = (
            DeleteObject(obj.object_name, obj.version_id)
            if permanently
            else DeleteObject(obj.object_name)
            for obj in self.client.custom_list_objects(
                bucket_name=self.bucket,
                prefix=str(self),
                delimiter=None,
                include_version=permanently,
            )
        )
        response = self.client.custom_remove_objects(
            bucket_name=self.bucket, delete_object_list=delete_objects
        )
        if self.verbose:
            if not response.error_list:
                logger.info(f"Deleted {self.str_persistent} directory {self}.")
            else:
                logger.error(
                    f"One or more error occured while deleting"
                    f" {self.str_persistent} directory {self}. Check the"
                    f" returned response for more details."
                )
        return DeleteResponse(response)
