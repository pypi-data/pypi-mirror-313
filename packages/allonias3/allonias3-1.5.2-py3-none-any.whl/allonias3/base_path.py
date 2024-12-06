from __future__ import annotations

import importlib
import logging
import re
import sys
import traceback
from collections.abc import Iterable
from copy import copy, deepcopy
from functools import cached_property
from pathlib import Path
from types import GeneratorType
from typing import TYPE_CHECKING, Any, ClassVar, Union

import cloudpickle

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from minio import Minio, S3Error
from typeguard import typechecked
from urllib3 import PoolManager

from .configs import Configs
from .helpers.class_property import classproperty
from .helpers.enums import ClientTypeEnum, ObjectTypeEnum
from .helpers.getattr_safe_property import getattr_safe_property
from .helpers.responses import (
    DeleteResponse,
    HeadResponse,
    VersionsResponse,
    WriteResponse,
)
from .helpers.utils import (
    ROOT_FOLDERS_RE,
    find_object_type,
    handle_type_error,
)

if TYPE_CHECKING:
    from minio.deleteobjects import DeleteResult
    from minio.helpers import ObjectWriteResult
    from pydantic import UUID4

try:
    import botocore
    from botocore.client import BaseClient
except ModuleNotFoundError:
    ClientType = Minio
    ConfigType = PoolManager
    S3ErrorType = S3Error
else:
    ClientType = Union[Minio, BaseClient]
    ConfigType = Union[PoolManager, dict]
    S3ErrorType = Union[S3Error, botocore.exceptions.ClientError]

try:
    from .encoder_decoder.advanced import _Appender, _Decoder, _Encoder
except ModuleNotFoundError:
    from .encoder_decoder.basic import (
        _BasicAppender as _Appender,
    )
    from .encoder_decoder.basic import (
        _BasicDecoder as _Decoder,
    )
    from .encoder_decoder.basic import (
        _BasicEncoder as _Encoder,
    )

    _can_handle_type = False
else:
    _can_handle_type = True


logger = logging.getLogger("allonias3.base_path")


class BasePath:
    _CLIENT: ClassVar[ClientType | None] = None
    _S3Error: ClassVar[S3ErrorType]
    _KEY: ClassVar[tuple[UUID4, UUID4] | None] = None
    _ATTRIBUTES: ClassVar[list[str]] = [
        "persistent",
        "verbose",
        "encoding",
        "handle_type",
    ]
    CONFIG: ClassVar[ConfigType]
    """Can be changed with :obj:`~BasePath.set_config`"""
    CLIENT_TYPE: ClassVar[ClientTypeEnum]
    """So you can check you are using the client you wanted."""

    _Appender: ClassVar[type] = _Appender
    _Decoder: ClassVar[type] = _Decoder
    _Encoder: ClassVar[type] = _Encoder

    _CAN_HANDLE_TYPE: ClassVar[bool] = _can_handle_type

    HANDLE_TYPE: ClassVar[bool] = _can_handle_type
    """Whether to handle object type properly when reading or writing data.

    This value is overloaded by the "handle_type" argument when creating a
    S3Path instance, is specified.

    You will have to have installed the optional dependencies "datatypehandler":
    `pip install allonias3[datatypehandler]`.
    """

    @classproperty
    @getattr_safe_property
    def client(cls) -> ClientType:  # noqa: N805
        # Call initialize every time in case the key (id, secret) changed in the
        # env vars. If it did not, the call will be very fast.
        cls._initialize()
        return cls._CLIENT

    # Class methods

    @classmethod
    @typechecked
    def __check_init_params(
        cls,
        path: Self | Path | Union[str, None] = "",
        persistent: bool = True,
        verbose: bool = True,
        encoding: str = "utf-8",
        handle_type: bool | None = None,
        object_type: Union[str, None] = None,
    ):
        pass

    @classmethod
    def set_config(cls, config: ConfigType):
        """To change the boto or minio config. Will force any existing
        :obj:`~BasePath.client` to be recreated next time it is called.

        Use None to reset the configuration to defaults.
        """
        cls.CONFIG = config
        cls._CLIENT = None
        cls._KEY = None

    # Private abstract class methods

    @classmethod
    def _initialize(cls) -> None:
        raise NotImplementedError

    # Abtract properties

    @cached_property
    @getattr_safe_property
    def versioned(self) -> bool:
        raise NotImplementedError

    # Private abstract methods

    def _check_existing_type(self) -> None:
        raise NotImplementedError

    def _get_object(self, version_id: Union[str, None]) -> dict:
        raise NotImplementedError

    def _close_response(self) -> None:
        raise NotImplementedError

    def _write_default(
        self, content, **write_kwargs
    ) -> dict | ObjectWriteResult:
        raise NotImplementedError

    def _append(
        self,
        content,
        read_kwargs: dict,
        write_kwargs: dict,
        append_kwargs: dict,
    ) -> dict | ObjectWriteResult:
        raise NotImplementedError

    def _write_pathlib(self, content: Path) -> dict | ObjectWriteResult:
        raise NotImplementedError

    def _write_url(
        self, content: str, timeout: int
    ) -> dict | ObjectWriteResult:
        raise NotImplementedError

    def _put_object(self, body: str) -> dict | ObjectWriteResult:
        raise NotImplementedError

    def _copy_object(
        self, destination: BasePath, version_id: Union[str, None] = None
    ) -> dict | ObjectWriteResult:
        raise NotImplementedError

    def _download(
        self,
        localpath: str | Path | None = None,
        version_id: Union[str, None] = None,
    ):
        raise NotImplementedError

    def _upload(self, localpath: Path) -> WriteResponse:
        raise NotImplementedError

    def _delete_one(self, version_id: Union[str, None]) -> dict | DeleteResult:
        raise NotImplementedError

    def _delete_all(self) -> dict | DeleteResult:
        raise NotImplementedError

    # Private methods

    def _pre_write_checks(self):
        if not self:
            raise ValueError(
                "You did not provide any path to write to, or you provided the"
                " bucket's root directory."
            )
        if self.name == ".s3keep":
            raise PermissionError("Can not create/write to a '.s3keep file'.")
        if re.search(ROOT_FOLDERS_RE, str(self)):
            raise PermissionError(f"Can not create/write to the file '{self}'.")
        if self.is_dir():
            raise IsADirectoryError(
                f"'{self}' is a directory, you can not write content to it."
                " Please write to a file instead."
            )

        # Will force the object type to 'unknown' if it is None at this point.
        self._check_existing_type()

    def _cast_generator(self, generator) -> GeneratorType:
        """Will use :obj:`~_cast` on every element of the input generator
        before yielding them.
        """
        for item in generator:
            yield self._cast(item)

    def _cast(self, iter_: Any):
        """Casts :inlinepython:`iter` into the appropriate type.

        * If it is a :obj:`~BasePath` or a :obj:`~pathlib.Path`, cast it into a
          :obj:`~BasePath.` using :obj:`~BasePath.kwargs` as arguments.
        * If it is a generator, uses :obj:`~_cast_generator`
        * If it is not an iterable, or if it is a string, returns it as-is
        * If it is an iterable, uses itself on every element of it to produce
          a list of cast objects and returns it.
        """
        klass = self.__class__
        if isinstance(iter_, GeneratorType):
            return self._cast_generator(iter_)
        if isinstance(iter_, (Path, klass)):
            return klass(iter_, **self.kwargs)
        # Strings are iterables, but we do not want to iterate over them here !
        if isinstance(iter_, str) or not isinstance(iter_, Iterable):
            return iter_
        return [self._cast(item) for item in iter_]

    def _get_version_from_revision(self, revision: int) -> str:
        """From a given revision of a given s3key, returns the corresponding
        version UUID.

        Args:
            revision: The revision number. Can not be 0. Can be negative: -1 is
                the latest revision, -2 the second latest, etc...

        Returns:
            :
                The version UUID corresopnding to the specified revision.

        Raises:
            ValueError:
                If :inlinepython:`revision` is 0, if the revision had no
                corresponding version in the metadata DB, or if a negative value
                was passed but not enough revisions were found.
        """
        if revision == 0:
            raise ValueError("Revision number can not be 0.")
        all_versions = self.versions(details=False)
        n_versions = len(all_versions)
        if revision < 0:
            revision = (len(all_versions) + revision) + 1
            if revision < 0:
                raise ValueError(
                    f"{self} only has {len(all_versions)} revisions."
                )
        if len(all_versions) < revision:
            raise ValueError(f"Revision {revision} does not exist for {self}.")
        return all_versions[n_versions - revision]

    def _check_rm_inputs(
        self,
        version_id: Union[str, None],
        permanently: bool,
    ) -> DeleteResponse | None:
        # Can happen if 'permanently' is True and a deleted marker exists for
        # this file, but a directory with the same name also exists
        if self.is_dir():
            message = f"Can not delete file '{self}': it is a directory."
            if self.verbose:
                logger.error(message)
            return DeleteResponse(
                {
                    "Errors": [
                        {
                            "Key": str(self),
                            "VersionId": version_id,
                            "Code": "IsADirectoryError",
                            "Message": message,
                        }
                    ]
                }
            )
        if self.name == ".s3keep":
            message = (
                "Can not delete .s3keep files: they serve to identify"
                " directories."
            )
            if self.verbose:
                logger.error(message)
            return DeleteResponse(
                {
                    "Errors": [
                        {
                            "Key": str(self),
                            "VersionId": version_id,
                            "Code": "IsADirectoryError",
                            "Message": message,
                        }
                    ]
                }
            )
        if not self.is_file(include_deleted=permanently):
            message = f"Can not delete file '{self}': not found."
            if self.verbose:
                logger.error(message)
            return DeleteResponse(
                {
                    "Errors": [
                        {
                            "Key": str(self),
                            "VersionId": version_id,
                            "Code": "NoSuchKey",
                            "Message": message,
                        }
                    ]
                }
            )
        if version_id and version_id not in self.versions(include_deleted=True):
            message = (
                f"Can not delete file '{self}' with "
                f"version {version_id}: not such version."
            )
            if self.verbose:
                logger.error(message)
            return DeleteResponse(
                {
                    "Errors": [
                        {
                            "Key": str(self),
                            "VersionId": version_id,
                            "Code": "NoSuchVersion",
                            "Message": message,
                        }
                    ]
                }
            )
        return None

    def _check_rmdir_inputs(self) -> DeleteResponse | None:
        if not str(self):
            message = (
                "You did not provide any path to delete, or you provided the"
                " root directory"
            )
            if self.verbose:
                logger.error(message)
            return DeleteResponse(
                {
                    "Errors": [
                        {
                            "Key": str(self),
                            "VersionId": None,
                            "Code": "ValueError",
                            "Message": message,
                        }
                    ]
                }
            )
        if re.search(ROOT_FOLDERS_RE, str(self)):
            message = f"You are not allowed to delete '{self}'"
            if self.verbose:
                logger.error(message)
            return DeleteResponse(
                {
                    "Errors": [
                        {
                            "Key": str(self),
                            "VersionId": None,
                            "Code": "PermissionError",
                            "Message": message,
                        }
                    ]
                }
            )
        if not self.is_dir():
            message = f"Cannot access '{self}': No such directory"
            if self.verbose:
                logger.error(message)
            return DeleteResponse(
                {
                    "Errors": [
                        {
                            "Key": str(self),
                            "VersionId": None,
                            "Code": "NotADirectoryError",
                            "Message": message,
                        }
                    ]
                }
            )
        return None

    def _log_write(self, append: bool, exists: bool) -> None:
        if self.verbose:
            created = (
                f"Created {self.object_type} object at"
                f" {self.str_persistent} location {self}."
            )

            messages = {
                True: {
                    True: f"Appended to {self.object_type} object at "
                    f"{self.str_persistent} location {self}.",
                    False: created,
                },
                False: {
                    True: f"Created a new revision for object {self}."
                    if self.persistent
                    else f"Overwrote {self.object_type} object at {self}.",
                    False: created,
                },
            }
            logger.info(messages[append][exists])

    # Abstract public methods

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
        raise NotImplementedError

    @typechecked
    def is_file(
        self, include_deleted: bool = False, version_id: Union[str, None] = None
    ) -> bool:
        raise NotImplementedError

    @typechecked
    def is_dir(self, check_s3keep: bool = False) -> bool:
        raise NotImplementedError

    @typechecked
    def head(self, version_id: Union[str, None] = None) -> HeadResponse:
        raise NotImplementedError

    @typechecked
    def size(
        self,
        unit: str = "MB",
        binary_base: bool = True,
        version_id: Union[str, None] = None,
    ) -> float:
        raise NotImplementedError

    def import_from_s3(self) -> None:
        """Used to import a Python file or module directory inside a notebook.

        In Jupyterlab, the user can create a Python file or module beside its
        notebooks and write code in it. Then, from the notebook, one can import
        this file like any other module.
        However, the created Python file would be on S3, while only local files
        or modules can be imported in the notebook. This function copies the
        imported file or directory locally then imports it as a Python module.

        Examples:
            .. code-block:: python

                # Inside a notebook
                from allonias3 import S3Path
                # Assuming there is a "functions.py" file beside the notebook
                S3Path("notebooks/notebook/functions.py").import_from_s3()
                # Can now import from "functions.py"
                from functions import ...
        """
        self.download(self.name.replace("-", "_"))
        name = self.stem.replace("-", "_")
        if Path(name).is_dir():
            if self.verbose:
                logger.info(
                    f"Imported module {name} from s3 you can now do"
                    f"\n>>> from {name} import ...\n or simply "
                    f"\n>>> import {name}",
                )
            module = __import__(name)
            cloudpickle.register_pickle_by_value(module)
            return
        spec = importlib.util.spec_from_file_location(
            name, self.name.replace("-", "_")
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        cloudpickle.register_pickle_by_value(module)
        if self.verbose:
            logger.info(
                f"Imported file {name} from s3 you can now do"
                f"\n>>> from {name} import ...\n or simply "
                f"\n>>> import {name}",
            )

    @typechecked
    def download(
        self,
        localpath: str | Path | None = None,
        version_id: Union[str, None] = None,
    ) -> None:
        if self.name == ".s3keep":
            return
        localpath = Path(localpath) if localpath else Path(self.name)
        if self.is_dir():
            if version_id:
                logger.warning(
                    "Specified version_id is ignored when downloading a "
                    "directory"
                )
            if not localpath.is_dir():
                localpath.mkdir(parents=True)
            for afile in self.content(
                show_directories=True, recursive=False, show_hidden=True
            ):
                afile.verbose = False
                afile.download(localpath / afile.name)
            if self.verbose:
                logger.info(
                    f"Copied content of {self.str_persistent} folder {self} to "
                    f"{localpath}/",
                )
            return

        if not localpath.parent.is_dir():
            localpath.parent.mkdir(parents=True)
        self._download(localpath, version_id)

    @typechecked
    def content(
        self,
        show_files: bool = True,
        show_hidden: bool = False,
        show_directories: bool = False,
        recursive: bool = True,
    ) -> list[BasePath]:
        raise NotImplementedError

    @typechecked
    def rmdir(
        self,
        recursive: bool = False,
        permanently: bool = True,
    ) -> DeleteResponse:
        raise NotImplementedError

    # Properties

    @cached_property
    @getattr_safe_property
    def bucket(self) -> str:
        """The bucket name containing this S3Path, depeding on
        :obj:`~persistent`.
        """
        return (
            Configs.instance.persistent_bucket_name
            if self.persistent
            else Configs.instance.non_persistent_bucket_name
        )

    @property
    @getattr_safe_property
    def handle_type(self) -> bool:
        """
        Is the path supposed to handle special types when reading and writing?
        """
        return self._handle_type

    @handle_type.setter
    @typechecked
    def handle_type(self, value: bool):
        if value and not self._CAN_HANDLE_TYPE:
            raise ModuleNotFoundError(handle_type_error)
        self._handle_type = value

    @property
    @getattr_safe_property
    def persistent(self) -> bool:
        """Is the path on the persistent or the non-persistent bucket?"""
        return self._persistent

    @property
    @getattr_safe_property
    def str_persistent(self) -> str:
        return "persistent" if self.persistent else "non-persistent"

    @property
    @getattr_safe_property
    def kwargs(self) -> dict:
        """Used when creating new S3Path instances from this one, which will
        inherite some attributes (verbosity, persistency, object type,
        whether the content type and file extensions should be handled
        or not and the encoding)"""
        return {
            attr.lstrip("_"): getattr(self, attr) for attr in self._ATTRIBUTES
        }

    @property
    @getattr_safe_property
    def path(self) -> Path:
        """The S3 path as a :obj:`~pathlib.Path` object. Never begins nor ends
        with '/'."""
        return Path(str(self._path).lstrip("/"))

    @path.setter
    @typechecked
    def path(self, path: Self | Path | Union[str, None]):
        if ".." in str(path):
            raise PermissionError(
                "Please do not use '..' in paths, only use absolute paths."
            )
        # force object_type to be recalculated as a change of path could
        # mean a change of type
        self._object_type = None
        if path is None or str(path) == "." or str(path) == "":
            path = "/"
        if isinstance(path, Path):
            path = str(path)
        if isinstance(path, self.__class__):
            self._path = copy(path._path)  # noqa: SLF001
        else:
            path = path.rstrip("/")
            if not path.startswith("/"):
                path = f"/{path}"
            self._path = Path(path)

    @property
    @getattr_safe_property
    def object_type(self) -> str:
        """The type of the object.

        The object type is set automatically depending on the location of the
        object on S3. If the type can not be deduced from the path, it will be
        "unknown". You can set it yourself to any value present in
        :obj:`~allonias3.helpers.enums.ObjectTypeEnum`.

        .. code-block:: python

            from allonias3 import S3Path

            path = S3Path("notebooks/myfolder/test.csv")
            path.object_type  # will return 'unknown'

            path = S3Path("notebooks/notebook/myfile.py")
            path.object_type  # will return 'notebook'

        Note that one existing file can only have one type: the following code
        will raise :obj:`TypeError`

        .. code-block:: python

            from allonias3 import S3Path

            path = S3Path("notebooks/myfolder/test.csv")  # type is None
            path.write(...)  # type becomes 'unknown'
            path.object_type = "dataset"
            path.write(...)  # will raise TypeError

        """
        if self._object_type is None:
            if self.name == ".s3keep":
                self._object_type = ObjectTypeEnum.s3keep.value
            else:
                parts = self.parts
                n_parts = len(parts)
                if n_parts > 0:
                    self._object_type = find_object_type(
                        self.name, parts, n_parts
                    )
                else:
                    self._object_type = ObjectTypeEnum.unknown.value
        return self._object_type

    @object_type.setter
    @typechecked
    def object_type(self, value: Union[str, None]):
        allowed_types = ObjectTypeEnum.list()
        allowed_types.append(None)

        if value not in allowed_types:
            raise TypeError(
                f"Invalid object type '{value}'. Value should be one of these"
                f" {'|'.join(ObjectTypeEnum.list())}"
            )
        self._object_type = value

    # Magic methods

    def __bool__(self):
        return bool(str(self))

    def __str__(self):
        as_str = str(self.path)
        return as_str if as_str != "." else ""

    def __repr__(self):
        return str(self)

    def __fspath__(self):
        return f"s3://{self.bucket}/{self}"

    @typechecked
    def __itruediv__(self, other: str) -> Self:
        if ".." in other:
            raise PermissionError(
                "Please do not use '..' in '/', use 'path.parent' instead."
            )
        self.path /= other
        return self

    @typechecked
    def __truediv__(self, other: str) -> Self:
        if ".." in other:
            raise PermissionError(
                "Please do not use '..' in 'path / \"..string\"', use "
                "'path.parent / \"string\"' instead."
            )
        return self.__class__(self._path / other, **self.kwargs)

    def __copy__(self):
        return self.__class__(copy(self._path), **self.kwargs)

    def __deepcopy__(self, memo):
        return self.__class__(deepcopy(self._path), **deepcopy(self.kwargs))

    def __getattr__(self, obj_name: str) -> Any:
        """Any attribute or property (not methods) valid for
        :obj:`~pathlib.Path` is also valid for S3Path. To achieve that, any
        attribute or property not defined in S3Path will be looked for in
        :obj:`~pathlib.Path`, and only if not found here will AttributeError be
        raised. Any instance of :obj:`~pathlib.Path` in the result will be
        converted into a S3Path instance, with the same attribute (beside the
        path itself of course) as the calling S3Path instance."""
        if isinstance(self, type):
            # Happens when doing 'S3Path.parent' instead of 'S3Path().parent',
            # for example.
            raise TypeError(
                f"type object '{self.__name__}' object has not attribute"
                f" '{obj_name}'"
            )

        path = self.path
        if obj_name in dir(path):
            obj = getattr(self.path, obj_name)
            if callable(obj):
                raise AttributeError(
                    f"'{self.__class__.__name__}' object has not attribute "
                    f"'{obj_name}'"
                )
            if isinstance(obj, Path):
                return self.__class__(obj, **self.kwargs)
            if isinstance(obj, Iterable):
                return self._cast(obj)
            return obj

        raise AttributeError(f"'S3Path' object has not attribute '{obj_name}'")

    def __eq__(self, other):
        if isinstance(other, BasePath):
            return self.__fspath__() == other.__fspath__()
        raise NotImplementedError

    def __lt__(self, other):
        if isinstance(other, BasePath):
            return self.__fspath__() < other.__fspath__()
        raise NotImplementedError

    def __le__(self, other):
        if isinstance(other, BasePath):
            return self.__fspath__() <= other.__fspath__()
        raise NotImplementedError

    def __gt__(self, other):
        if isinstance(other, BasePath):
            return self.__fspath__() > other.__fspath__()
        raise NotImplementedError

    def __ge__(self, other):
        if isinstance(other, BasePath):
            return self.__fspath__() >= other.__fspath__()
        raise NotImplementedError

    def __hash__(self):
        return hash(self.__fspath__())

    # Public methods

    def __init__(
        self,
        path: Self | Path | Union[str, None] = "",
        persistent: bool = True,
        verbose: bool = True,
        encoding: str = "utf-8",
        handle_type: bool | None = None,
        object_type: Union[str, None] = None,
    ):
        # Stupid hack to please Sphinx
        self.__check_init_params(
            path,
            persistent,
            verbose,
            encoding,
            handle_type,
            object_type,
        )
        self._path = None
        self._persistent = None
        self.verbose = None
        self.encoding = None
        self._handle_type = None
        self._object_type = None
        self.__define(
            path=path,
            persistent=persistent,
            verbose=verbose,
            encoding=encoding,
            handle_type=handle_type,
            object_type=object_type,
        )

    # Pickle/Unpickle methods

    def __define(
        self,
        path: Self | Path | Union[str, None],
        persistent: bool,
        verbose: bool,
        encoding: str,
        handle_type: bool | None,
        object_type: Union[str, None],
    ):
        self.path: Path = path
        self._persistent: bool = persistent
        self.verbose: bool = verbose
        """Prints informations to stdout when methods are called."""
        self.hidden: bool = self.name.startswith(".")
        """True if the name of the object starts with '.'"""
        self.encoding: str = encoding
        """Used to encode/decode the S3Path content. See :obj:`~read` and
        :obj:`~write`. 'utf-8' by default."""
        self.handle_type: bool = (
            handle_type if handle_type is not None else self.HANDLE_TYPE
        )
        if self.handle_type and not self._CAN_HANDLE_TYPE:
            raise ModuleNotFoundError(handle_type_error)
        """Used to handle special data formats and file extensions.
        See :obj:`~read` and :obj:`~write`. True by default."""
        self._object_type: Union[str, None] = None
        self.object_type: Union[str, None] = object_type

    def __getstate__(self):
        return (
            self.path,
            self.persistent,
            self.verbose,
            self.encoding,
            self.handle_type,
            self.object_type,
        )

    def __setstate__(self, state):
        self.__define(*state)

    @typechecked
    def change_suffix(self, suffix: str):
        """To change the extension of this path in-place."""
        if not suffix.startswith("."):
            suffix = f".{suffix}"
        self._path = self._path.with_suffix(suffix)

    @typechecked
    def with_suffix(self, suffix: str) -> Self:
        """Returns a S3Path with a different extension"""
        if not suffix.startswith("."):
            suffix = f".{suffix}"
        return self.__class__(self._path.with_suffix(suffix), **self.kwargs)

    @typechecked
    def exists(
        self, include_deleted: bool = False, version_id: Union[str, None] = None
    ) -> bool:
        """
        Checks that this S3Path is a file or a directory on S3.

        Args:
            include_deleted: If False (default), deleted versioned objects
                appear not to exist. Else, they do.
            version_id: to check the existence of a specific version
        """
        return (self.is_dir() and not version_id) or self.is_file(
            include_deleted, version_id
        )

    @typechecked
    def read(
        self,
        version_id: None | str = None,
        revision: None | int = None,
        raise_if_unpickle_fails: bool = False,
        **kwargs,
    ):
        """Reads the content of this S3Path if it is a file.

        If :obj:`~handle_type` is :obj:`True` (default) and this S3Path is a:

          * **.csv**, **.xls**, **.xlsx**, **.xlsm**, **.xlsb**, **.odf**,
            **.ods** or **.odt**: will return a :obj:`~pandas.DataFrame`, using
            the first column as index, unless `kwargs` specifies another column
            or :inlinepython:`None` in :inlinepython:`index_col`.
            :inlinepython:`**kwargs` are passed to :obj:`~pandas.read_csv` or
            :obj:`~pandas.read_excel`.
          * **.parquet** : will return a :obj:`~pandas.DataFrame`.
            :inlinepython:`**kwargs` are passed to :obj:`~pandas.read_parquet`.
          * **.json** : will return a :obj:`dict`.
            :inlinepython:`**kwargs` are passed to :obj:`json.loads`
          * **.npy** : will return a :obj:`~numpy.ndarray`.
            :inlinepython:`**kwargs` will be ignored.
          * **.h5** : will return an open :obj:`h5py.File` object. ALWAYS use
            :inlinepython:`handle_type=True` when reading HDF5 files, they can
            not be (un)pickled. :inlinepython:`**kwargs` will be ignored.

        Any other file extension can return any other type, which will be
        unpickled if it is not a b-string, decoded with :obj:`~encoding`
        if it is a b-string.

        If :obj:`~handle_type` is :obj:`False`, will use pickle if the input is
        not a :obj:`str`, else will decode the :obj:`str` using
        :obj:`~encoding`.

        Args:
            version_id: uuid of the object version to load. Incompatible with
                :inlinepython:`revision`.
            revision: revision number to use. Incompatible with
                :inlinepython:`version_id`.
            raise_if_unpickle_fails: If :obj:`True`, and if the content is at
                some point unpickled and the operation fails, raises the error.
                Else, returns the content before the unpickling attempt.
            kwargs:
                Any keyword argument valid for :obj:`~pandas.read_csv`,
                :obj:`~pandas.read_parquet` or :obj:`json.loads`.
                Only used if this S3Path is a **.csv**, **.parquet**
                or **.json** file.

        Returns:
            :
                The (possibly decoded) file's Body, or a special type based on
                the file extension.

        Raises:
            IsADirectoryError:
                If this S3Path is a directory instead of a file.
            ValueError:
                If both :inlinepython:`version_id` and :inlinepython:`revision`
                are specified.
        """
        if version_id is not None and revision is not None:
            raise ValueError("Can not specify both revision and version_id")
        if self.is_dir():
            raise IsADirectoryError(
                f"'{self}' is a directory, you can not write content to it."
                " Please write to a file instead."
            )
        if revision is not None:
            version_id = self._get_version_from_revision(revision)

        decoder = None
        try:
            if self.verbose:
                logger.info(f"Reading {self.str_persistent} {self}...")
            response = self._get_object(
                version_id if version_id and self.persistent else None
            )
            decoder = self._Decoder(
                str(self),
                self.encoding,
                deactivate=not self.handle_type,
                raise_if_unpickle_fails=raise_if_unpickle_fails,
            )
            content = decoder(response, **kwargs)
        finally:
            self._close_response()
            if decoder:
                decoder.close()
        if self.verbose:
            logger.info("...success")
        return content

    @typechecked
    def copy(
        self,
        destination: BasePath,
        version_id: Union[str, None] = None,
    ) -> WriteResponse:
        """Copy this file to 'destination'

        Args:
            destination: the new file
            version_id: to copy a specific version

        The maximum size of copied objects is 5GB.
        """
        exists = destination.is_file()
        response = self._copy_object(destination, version_id)
        if not exists and not destination.parent.is_dir(check_s3keep=True):
            destination.parent.mkdir()
        if self.verbose:
            logger.info(
                f"Copied to {self.object_type} object at {self.str_persistent}"
                f" {self} to {destination.str_persistent} {destination}.",
            )
        return WriteResponse(response)

    @typechecked
    def write(
        self,
        content,
        append: bool = False,
        timeout: int = 60,
        read_kwargs: None | dict = None,
        write_kwargs: None | dict = None,
        append_kwargs: None | dict = None,
    ) -> WriteResponse:
        """Save content in this S3Path.

        If :inlinepython:`content` starts with "http", it is assumed to be an
        URL and its content is downloaded to the specified path.

        Else, if :inlinepython:`content` is a :obj:`~pathlib.Path` object, will
        upload its content.

        Else, if :obj:`~BasePath.handle_type` is :obj:`True`
        and the self is a:

            * **.csv**, **.xls**, **.xlsx**, **.xlsm**, **.xlsb**, **.odf**,
              **.ods**, **.odt** or **.parquet**: :inlinepython:`content` must
              be a :obj:`~pandas.DataFrame` or :obj:`~pandas.Series`,
              :inlinepython:`**write_kwargs` are passed to
              :obj:`~pandas.DataFrame.to_csv`, :obj:`~pandas.DataFrame.to_excel`
              or :obj:`~pandas.DataFrame.to_parquet`
            * **.json**: :inlinepython:`content` must be a :obj:`dict`,
              :inlinepython:`**write_kwargs` are passed to :obj:`json.dumps`.
            * **.npy**: :inlinepython:`content` must be a :obj:`~numpy.ndarray`,
              which will be pickled, `write_kwargs` will be ignored.
            * **.h5**: :inlinepython:`content` must be an open :obj:`h5py.File`
              object. ALWAYS set
              :obj:`~BasePath.handle_type` to :obj:`True`
              when saving HDF5 files, as they can not be pickled.
              :inlinepython:`**write_kwargs` will be ignored.

        Any other file extension can support any other type, which will be
        pickled if it is not a :obj:`str`, or encoded with :obj:`~encoding` if
        it is.

        If :obj:`~BasePath.handle_type` is :obj:`False`,
        will pickle the content if it is not a :obj:`str`, or encode it using
        :obj:`~encoding` if it is.

        :inlinepython:`content=None` will be the same as
        :inlinepython:`content=""` and :inlinepython:`content=b""`

        :obj:`str`, :obj:`~pandas.DataFrame`, :obj:`~pandas.Series`, :obj:`dict`
        and :obj:`~numpy.ndarray` can be appended to files containing the same
        type of objects (respecting the above file extensions). A line break,
        :obj:`pandas.concat`, :obj:`numpy.concatenate` or :obj:`dict.update` is
        used to append.

        Args:
            content: the file content to save
            append: instead of overwriting the file, append to it
            timeout: if "content" is an URL to download from, the timeout of
                the download request.
            read_kwargs:
                Keyword argument valid for :obj:`~pandas.read_csv`,
                :obj:`~pandas.read_parquet` or :obj:`json.loads`. Only used if
                appending and if the S3Path is a **.csv**,
                **.parquet** or **.json** file.
            write_kwargs: Keyword arguments valid for
                :obj:`~pandas.DataFrame.to_csv`,
                :obj:`~pandas.DataFrame.to_parquet` or :obj:`json.dumps`. Only
                used if the S3Path is a **.csv**, **.parquet** or **.json**
                file.
            append_kwargs: Keyword arguments valid for
                :obj:`~pandas.concat` or :obj:`~numpy.concatenate`

        Raises:
            ValueError:
                If the current S3Path is empty
            TypeError:
                If trying to write a file of a certain type when the same file
                    already exists with another type.
            IsADirectoryError:
                If this S3Path is an existing directory.
            PermissionError:
                If the current S3Path is "notebooks", ".config" or ".logs"
                or if it is a '.s3keep' file.
        """
        self._pre_write_checks()
        exists = self.is_file()
        if read_kwargs is None:
            read_kwargs = {}
        if write_kwargs is None:
            write_kwargs = {}

        if content is None:
            content = b""

        if isinstance(content, Path):
            response = self._write_pathlib(content)
        elif isinstance(content, str) and content.startswith("http"):
            if self.verbose:
                logger.info(
                    f"Downloading file {content} to "
                    f"{self.str_persistent}{self}...",
                )
            response = self._write_url(content, timeout)
        elif append and self.is_file:
            response = self._append(
                content, read_kwargs, write_kwargs, append_kwargs
            )
        else:
            response = self._write_default(content, **write_kwargs)

        if not exists and not self.parent.is_dir(check_s3keep=True):
            self.parent.mkdir()

        self._log_write(append, exists)

        return WriteResponse(response)

    @typechecked
    def upload(
        self, localpath: str | Path, verbose: bool = False
    ) -> WriteResponse | list[WriteResponse]:
        """Upload a local file or directory to this location.

        Upload the file located in localpath to this S3Path. If the S3Path file
        already exists, it is overwritten.

        If localpath is a directory, uploads it and its content to this S3Path.
        If the S3Path directory already exists, its content will be overwritten.

        Args:
            localpath: the key of the local file or directory to copy.
            verbose: to make the process verbose.

        Raises:
            NotADirectoryError:
                If the localpath points to a directory but the S3Path exists
                and is a file
            IsADirectoryError:
                If the localpath points to a file but the S3Path exists
                and is a directory
        """
        if not isinstance(localpath, Path):
            localpath = Path(localpath)

        if self.is_dir() and localpath.is_file():
            raise IsADirectoryError(
                "S3Path points to an existing directory but the localpath is a"
                " file. S3Path must either not exist or be a file."
            )
        if self.is_file() and localpath.is_dir():
            raise NotADirectoryError(
                "S3Path points to an existing file but the localpath is a"
                " directory. S3Path must either not exist or be a directory."
            )
        upload_to = copy(self)
        upload_to.verbose = verbose

        if localpath.is_dir():
            responses = []
            for subpath in localpath.glob("*"):
                upload_to_ = upload_to / subpath.name
                response = upload_to_.upload(subpath)
                if isinstance(response, list):
                    responses += response
                else:
                    responses.append(response)
            return responses

        response = upload_to._upload(localpath)  # noqa: SLF001
        if self.verbose:
            logger.info(
                f"Copied local file {localpath} to S3 on {upload_to}.",
            )
        return response

    def touch(self) -> WriteResponse:
        """Creates an empty file at this location."""
        previous_handle_type = self.handle_type
        self.handle_type = False
        response = self.write(None)
        self.handle_type = previous_handle_type
        return response

    def mkdir(self) -> WriteResponse | list[WriteResponse]:
        """Creates an empty directory at this location by creating .s3keep
        files in the directory and its parents.

        The user should not have to do that, since calling :obj:`write`
        will call this function for all the parent directories.

        Raises:
            PermissionError:
                If the directory name contains '.s3keep'
        """
        if not str(self):
            if self.verbose:
                logger.error("Skipping mkdir: S3Path is a bucket")
            return WriteResponse(False)
        if re.search(r"\.s3keep$", str(self)):
            raise PermissionError(
                "Illegal directory name. Can not end by '.s3keep'"
            )
        if self.is_dir(check_s3keep=True):
            if self.verbose:
                logger.error(
                    f"{self.str_persistent}"
                    f" directory {self} already exists.",
                )
            return WriteResponse(False)
        subdirectory = self.__class__()

        response = []

        for dirname in self.parts:
            if dirname == "/":
                continue
            subdirectory /= dirname
            s3keep = subdirectory / ".s3keep"
            if not s3keep.is_file():
                # Do not use touch, as it would call mkdir in an infinite
                # recursion
                response.append(WriteResponse(s3keep._put_object("")))  # noqa: SLF001
        if self.verbose:
            logger.info(f"Created {self.str_persistent} directory {self}.")
        return response

    @typechecked
    def rm(
        self,
        version_id: Union[str, None] = None,
        permanently: bool = True,
    ) -> DeleteResponse:
        """Deletes this path if it is a file.

        To delete a folder, use :obj:`~rmdir` instead.

        Args:
            version_id: uuid of the object version, if you want to remove a
                specific version. Note that this is irreversible.
            permanently: If :obj:`False`, the object is only turned into
                a deleted marker. It is not visible anymore, but still exists
                and could be restored. Otherwise, it is completely and
                definitely deleted along with all its versions. Useless if
                version_id is specified.
        """
        if errors := self._check_rm_inputs(
            version_id if self.versioned else None, permanently
        ):
            return errors

        try:
            if version_id and self.versioned:
                response = self._delete_one(version_id)
                message = (
                    f"Deleted {self.str_persistent}{self}"
                    f" file (version {version_id})."
                )
            elif permanently and self.versioned:
                response = self._delete_all()
                message = (
                    f"Deleted {self.str_persistent} file {self} permanently."
                )
            else:
                response = self._delete_one(None)
                message = f"Deleted {self.str_persistent} file {self}."
        except self._S3Error:
            message = (
                f"Error while deleting {self.str_persistent}{self},"
                f" version={version_id}: {traceback.format_exc()}"
            )
            if self.verbose:
                logger.exception(message)
            return DeleteResponse(
                {
                    "Errors": [
                        {
                            "Key": str(self),
                            "VersionId": version_id,
                            "Code": "IsADirectoryError",
                            "Message": message,
                        }
                    ]
                }
            )
        if self.verbose:
            logger.info(message)
        return DeleteResponse(response)
