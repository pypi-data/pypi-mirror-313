import itertools
import sys
from collections.abc import Generator

from minio import Minio as _Minio
from minio.datatypes import Object
from minio.deleteobjects import DeleteObject, DeleteResult
from minio.helpers import check_bucket_name

_MINIO_MAX_KEYS = 2147483647


class Minio(_Minio):
    def custom_remove_object(
        self, bucket_name, object_name, version_id=None
    ) -> DeleteResult:
        return self.custom_remove_objects(
            bucket_name, [DeleteObject(object_name, version_id)]
        )

    def custom_remove_objects(
        self, bucket_name, delete_object_list, bypass_governance_mode=False
    ) -> DeleteResult:
        # copied from
        # https://github.com/minio/minio-py/blob/2067045ccad998831414647b9cb23e506d1c3e1a/minio/api.py#L1915
        # The default minio's remove_objects only returns errors, we also
        # return successes.
        # The other difference is that we do not return a generator, but the
        # full response.
        check_bucket_name(bucket_name)

        # turn list like objects into an iterator.
        delete_object_list = itertools.chain(delete_object_list)
        succeses = []
        errors = []

        while True:
            # get 1000 entries or whatever available.
            kwargs = {"strict": False} if sys.version_info.minor != 9 else {}
            objects = [
                delete_object
                for _, delete_object in zip(
                    range(1000), delete_object_list, **kwargs
                )
            ]

            if not objects:
                break

            result = self._delete_objects(
                bucket_name,
                objects,
                quiet=True,
                bypass_governance_mode=bypass_governance_mode,
            )

            succeses += result.object_list
            errors += result.error_list

        return DeleteResult(succeses, errors)

    def custom_list_objects(
        self,
        bucket_name,
        prefix,
        restrict_to_prefix=False,
        **kwargs,
    ) -> Generator[Object]:
        for element in self._list_objects(
            bucket_name,
            prefix=prefix,
            max_keys=_MINIO_MAX_KEYS,
            **kwargs,
        ):
            if element.is_dir:
                continue
            if restrict_to_prefix and element.object_name != prefix:
                continue
            if element.is_latest:
                element._is_latest = element.is_latest == "true"  # noqa: SLF001
            yield element
