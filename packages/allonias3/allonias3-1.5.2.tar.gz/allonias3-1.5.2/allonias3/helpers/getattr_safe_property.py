from functools import wraps


class PropertyAttributeError(Exception):
    pass


def getattr_safe_property(func):
    """The :obj:`~allonias3.base_path.BasePath` uses 'property', and overloads
    :obj:`__getattr__`. This is not a good idea, because if an AttributeError is
    raised during the evaluation of a property, then the error message will
    look like the property itself is not found.

    To avoid those misleading errors, all properties of
    :obj:`~allonias3.base_path.BasePath`, :obj:`~allonias3.s3_path.S3Path`,
    :obj:`~allonias3.boto.boto_path.BotoPath` and
    :obj:`~allonias3.minio.minio_path.MinioPath` must be written as such:


    .. code-block:: python

        @property
        @getattr_safe_property
        def some_property(self):
            ...

    Since the new :obj:`~PropertyAttributeError` is raised from the original
    :obj:`AttributeError`, the error stack will contain the actual problematic
    line, but it will not be silently caught by :obj:`__getattr__`.
    """

    @wraps(func)
    def wrapper(self):
        try:
            return func(self)
        except AttributeError as error:
            raise PropertyAttributeError(
                "An AttributeError was raised while evaluating the property "
                f"'{func.__name__}' of a {self.__class__.__name__} instance:"
                f" {error}"
            ) from error

    return wrapper
