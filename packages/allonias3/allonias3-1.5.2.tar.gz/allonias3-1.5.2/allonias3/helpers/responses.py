from collections.abc import Generator
from typing import Any, ClassVar, Union

from minio.datatypes import Object
from minio.deleteobjects import DeleteResult
from minio.helpers import ObjectWriteResult


def _dummygen():
    yield 0


class BaseResponse:
    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        if not isinstance(other, BaseResponse):
            raise NotImplementedError
        return self.to_dict() == other.to_dict()

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError


class BaseSingleResponse(BaseResponse):
    _params: ClassVar[list[tuple[str, str]]]

    def __init__(
        self, response: Union[Object, ObjectWriteResult, dict, bool] = None
    ):
        self.params_not_found: list[str] = []
        self.success = True
        """List of parameters that were not found in the response"""
        if isinstance(response, (Object, ObjectWriteResult)):
            response = {
                key: getattr(response, key)
                for key in dir(response)
                if not key.startswith("_")
            }
        if isinstance(response, dict):
            self.read_response(response)
        if isinstance(response, bool) and response is False:
            self.success = False

    def to_dict(self) -> dict[str, Any]:
        thedict = {key[0]: getattr(self, key[0]) for key in self._params}
        thedict["params_not_found"] = self.params_not_found
        return thedict

    def read_response(self, response: dict):
        """Try to find params in the response. For a param like
        ('object_name', 'Key') for instance, will first look for 'object_name'
        in the response, then if not found for 'Key'.

        New attributes are defined using the found values, the attribute names
        in the above example would be 'object_name', because it is the first
        element in the tuple.
        """
        for param in self._params:
            param_name = param[0]
            try:
                value = response[param_name]
            except KeyError:
                try:
                    value = response[param[1]]
                except KeyError:
                    value = None
                    self.params_not_found.append(param_name)
            setattr(self, param_name, value)


class WriteResponse(BaseSingleResponse):
    """Response returned by all write operations.

    Attributes:
      object_name (str)
      bucket_name (str)
      version_id (str)
      last_modified (datetime.datetime)
    """

    _params: ClassVar = [
        ("object_name", "Key"),
        ("bucket_name", "Bucket"),
        ("version_id", "VersionId"),
        ("last_modified", "LastModified"),
    ]


class HeadResponse(BaseSingleResponse):
    """Response returned by all head operations.

    Attributes:
      object_name (str)
      bucket_name (str)
      version_id (str)
      size (int)
      last_modified (datetime.datetime)
      type (str)
      author (uuid4)
    """

    _params: ClassVar = [
        ("object_name", "Key"),
        ("bucket_name", "Bucket"),
        ("version_id", "VersionId"),
        ("size", "ContentLength"),
        ("last_modified", "LastModified"),
        ("type", ""),
        ("author", ""),
    ]


class BaseManyResponse(BaseResponse):
    _success: ClassVar[
        dict[Union[type, None], tuple[str, tuple[tuple[str, str, Any], ...]]]
    ]
    _error: ClassVar[dict[type, tuple[str, tuple[tuple[str, str, Any], ...]]]]
    _exclude_condition: ClassVar[Union[tuple[str, str], None]] = None

    def __init__(
        self, response: Union[DeleteResult, Generator[Object], dict], **kwargs
    ):
        self._handle_success(response, **kwargs)
        self._handle_errors(response)

    @staticmethod
    def _get_one_param(
        obj: Union[dict, Any], param: tuple[str, str, Any]
    ) -> Union[dict[str, Any], Any]:
        name = param[0]
        default = param[2]
        if isinstance(obj, dict):
            value = obj.get(name, default)
        else:
            try:
                value = getattr(obj, name)
            except AttributeError:
                try:
                    value = getattr(obj, param[1])
                except AttributeError:
                    value = default
        return value

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.successes,
            "errors": self.errors,
        }

    def _handle_success(self, response, **kwargs):
        """I wish I needed this method in my life"""
        should_exclude, on_param = (
            (
                kwargs.get(self._exclude_condition[0], False),
                self._exclude_condition[1],
            )
            if self._exclude_condition
            else (False, None)
        )
        params = self._success[response.__class__][1]
        if isinstance(response, dict):
            objects = response.get(self._success[dict][0], [])
        elif self._success[response.__class__][0] is None:
            objects = response
        else:
            objects = getattr(response, self._success[response.__class__][0])
        self.successes = [
            {
                param[1] or param[0]: self._get_one_param(obj, param)
                for param in params
            }
            for obj in objects
            if not (should_exclude and self._get_one_param(obj, on_param))
        ]

    def _handle_errors(self, response):
        """I wish I DID NOT need this method in my life"""
        if not self._error:
            self.errors = []
            return
        params = self._error[response.__class__][1]
        if isinstance(response, dict):
            objects = response.get(self._error[dict][0], [])
        else:
            objects = getattr(response, self._error[response.__class__][0])
        self.errors = [
            {
                param[1] if param[1] else param[0]: self._get_one_param(
                    obj, param
                )
                for param in params
            }
            for obj in objects
        ]


class VersionsResponse(BaseManyResponse):
    """Response returned by all verions-listing operations.

    Attributes:
      successes (list[dict]):
        Each item is a dict containing the following keys:
          * object_name (str)
          * version_id (str)
          * is_delete_marker (bool)
          * is_latest (bool)
          * last_modified (datetime.datetime)
      errors (list): always empty for this object
    """

    _success: ClassVar = {
        dict: (
            "Versions",
            (
                ("Key", "object_name", None),
                ("VersionId", "version_id", None),
                ("IsDeleted", "is_delete_marker", False),
                ("IsLatest", "is_latest", None),
                ("LastModified", "last_modified", None),
            ),
        ),
        type(_dummygen()): (
            None,
            (
                ("object_name", "", None),
                ("last_modified", "", None),
                ("version_id", "", False),
                ("is_latest", "", None),
                ("is_delete_marker", "", None),
            ),
        ),
    }
    _error: ClassVar = {}
    _exclude_condition = (
        "exclude_deleted",
        ("IsDeleted", "is_delete_marker", False),
    )

    def __init__(
        self, response: Union[Generator[Object], dict], exclude_deleted: bool
    ):
        if isinstance(response, dict):
            for obj in response.get("Versions", []):
                obj["IsDeleted"] = False
            if not exclude_deleted:
                for obj in response.get("DeleteMarkers", []):
                    obj["IsDeleted"] = True
                if deleted := response.get("DeleteMarkers", []):
                    if "Versions" not in response:
                        response["Versions"] = []
                    response["Versions"] += deleted

        super().__init__(response, exclude_deleted=exclude_deleted)
        self.successes = sorted(
            self.successes,
            key=lambda x: x["last_modified"],
            reverse=True,
        )

    @property
    def simple(self) -> list[str]:
        return [
            obj["version_id"] for obj in self.successes if obj["version_id"]
        ]


class DeleteResponse(BaseManyResponse):
    """Response returned by all delete operations.

    Attributes:
      successes (list[dict]):
        Each item is a dict containing the following keys:
          * name (str)
          * version_id (str)
          * delete_marker (bool)
          * delete_marker_version_id (str)
      errors (list[dict]):
        Each item is a dict containing the following keys:
          * name (str)
          * version_id (str)
          * code (int)
          * message (str)
    """

    _success: ClassVar = {
        DeleteResult: (
            "object_list",
            (
                ("name", "object_name", None),
                ("version_id", "", None),
                ("delete_marker", "", False),
                ("delete_marker_version_id", "", None),
            ),
        ),
        dict: (
            "Deleted",
            (
                ("Key", "object_name", None),
                ("DeleteMarker", "delete_marker", False),
                ("DeleteMarkerVersionId", "delete_marker_version_id", None),
                ("VersionId", "version_id", None),
            ),
        ),
    }
    _error: ClassVar = {
        DeleteResult: (
            "error_list",
            (
                ("name", "object_name", None),
                ("version_id", "", None),
                ("code", "", None),
                ("message", "", None),
            ),
        ),
        dict: (
            "Errors",
            (
                ("Key", "object_name", None),
                ("VersionId", "version_id", None),
                ("Code", "code", None),
                ("Message", "message", None),
            ),
        ),
    }
