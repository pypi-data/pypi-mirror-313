from .enums import ObjectTypeEnum

DEFAULT_PART_SIZE = 5 * 1024 * 1024  # 5MiB
_JPLAB_FOLDER = "notebooks/"
ROOT_FOLDERS_RE = r"^\/?(notebooks|\.config|\.logs)\/?$"

DEFAULT_S3_TIMEOUT = 10
DEFAULT_S3_RETRIES = 4

_DEFAULT_DELETE_ERROR_RESPONSE = {
    "Key": "",
    "VersionId": None,
    "Code": "",
    "Message": "",
}

handle_type_error = (
    "The dependencies to handle data types automatically are not installed."
    "Please run `pip install allonias3[datatypehandler]` or use "
    "`handle_type=False` when creating a S3Path object or set"
    "`S3Path.HANDLE_TYPE = False`."
)


def convert_storage_unit(size, from_unit="B", to_unit="MB", binary_base=True):
    """Converts :inlinepython:`size` from the unit :inlinepython:`from_unit`
    to the unit :inlinepython:`to_unit`.

    If :inlinepython:`binary_base = True` (default), we use kiB, MiB, GiB...
    (with a factor of 1024 between those), otherwise we use  kB, mB, GB...
    (with a factor of 1000 between those).
    """
    per_unit = 1024 if binary_base else 1000
    units = {"B": 0, "kB": 1, "MB": 2, "GB": 3, "TB": 4, "PB": 5}
    if from_unit not in units:
        raise ValueError(
            f"Invalid unit {from_unit}. Can be one of {list(units.keys())}."
        )
    if to_unit not in units:
        raise ValueError(
            f"Invalid unit {to_unit}. Can be one of {list(units.keys())}."
        )
    diff = units[to_unit] - units[from_unit]
    return float(size) / (per_unit**diff)


def list_by_thousands(operation_name, s3client, **kwargs):
    """listing things in boto3 is limited to 1000 elements in the response.
    This function depaginates them."""
    to_update = {
        "list_objects_v2": ("Contents", "CommonPrefixes"),
        "list_object_versions": ("Versions", "DeleteMarkers"),
    }
    if operation_name not in to_update:
        raise ValueError(f"Unknown operation {operation_name}")
    prefix = kwargs.get("Prefix", "")
    kwargs["Prefix"] = prefix if prefix != "/" else ""
    to_update = to_update[operation_name]
    paginator = s3client.get_paginator(operation_name)
    page_iterator = paginator.paginate(**kwargs)
    resp = {}
    for item in page_iterator:
        if not resp:
            resp.update(item)
        else:
            for result_to_update in to_update:
                if (
                    result_to_update not in item
                    and result_to_update not in resp
                ):
                    continue
                if result_to_update in item and result_to_update not in resp:
                    resp[result_to_update] = item[result_to_update]
                else:
                    resp[result_to_update] += item.get(result_to_update, [])
    if operation_name == "list_object_versions":
        # Listing object versions with s3 is done with a prefix, not a s3key, so
        # we can end up with more than we need if, for example, we have
        # file1.txt and file1.txt.csv. Then listing versions for file1.txt will
        # include the versions of file1.txt.csv, since it shares the same prefix
        # The next two conditions prevent that.
        resp["Versions"] = [
            version
            for version in resp.get("Versions", [])
            if version["Key"] == kwargs["Prefix"]
        ]
        resp["DeleteMarkers"] = [
            version
            for version in resp.get("DeleteMarkers", [])
            if version["Key"] == kwargs["Prefix"]
        ]
    return resp


def find_object_type(name: str, parts: tuple[str], n_parts: int) -> str:
    if parts[0] == ObjectTypeEnum.workflows.value:
        obj_type = ObjectTypeEnum.workflows.value
    elif parts[0] == "applications":
        if name.startswith("module_"):
            obj_type = ObjectTypeEnum.job.value
        elif name.startswith("user-service"):
            obj_type = ObjectTypeEnum.service.value
        else:
            obj_type = ObjectTypeEnum.unknown.value
    elif parts[0] in ("jobs", ".logs"):
        obj_type = ObjectTypeEnum.log.value
    elif parts[0] == ".config":
        obj_type = ObjectTypeEnum.package.value
    elif (
        n_parts > 1
        and parts[1] in ObjectTypeEnum.list()
        and parts[1]
        in (
            ObjectTypeEnum.notebook.value,
            ObjectTypeEnum.dataset.value,
            ObjectTypeEnum.model.value,
        )
    ):
        obj_type = parts[1]
    else:
        obj_type = ObjectTypeEnum.unknown.value
    return obj_type
