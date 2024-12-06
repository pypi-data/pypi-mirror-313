from enum import Enum, unique


class ExtendedEnum(Enum):
    @classmethod
    def list(cls, exclude=None):
        if exclude is None:
            exclude = []
        return [
            enumeration.value
            for enumeration in cls
            if enumeration.value not in exclude
        ]

    def __str__(self):
        return self.value


@unique
class ObjectTypeEnum(ExtendedEnum):
    """Possible object types."""

    dataset = "dataset"
    """"""
    notebook = "notebook"
    """"""
    workflows = "workflows"
    """"""
    service = "service"
    """"""
    job = "job"
    """"""
    model = "model"
    """"""
    script = "script"
    """"""
    package = "package"
    """"""
    log = "log"
    """"""
    unknown = "unknown"
    """"""
    s3keep = "s3keep"
    """"""


@unique
class ClientTypeEnum(ExtendedEnum):
    boto = "boto"
    minio = "minio"
