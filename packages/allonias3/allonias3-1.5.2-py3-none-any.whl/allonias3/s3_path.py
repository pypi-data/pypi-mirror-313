"""Class to handle a path on S3 just like if it was a local
 :obj:`~pathlib.Path`.

.. autosummary::

    S3Path
"""

from .configs import Configs

if Configs.instance.USE_BOTO is False:
    from .minio.minio_path import MinioPath as Path
else:
    try:
        from .boto.boto_path import BotoPath as Path
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            "The dependencies for Boto are not installed."
            " Please run `pip install allonias3[boto]` or stop specyfing "
            "USE_BOTO=True in your environment variables."
        ) from None


class S3Path(Path):
    """Use this class to interact with S3.

    An instance of this class represents a path on S3. There does not need to be
    anything at this location for the path to be valid.

    By default, the provider will be :obj:`~minio`. To use :obj:`~boto3` instead
    set the 'S3_PROVIDER="boto3"' environment variable before importing this
    class.

    Examples:
        .. code-block:: python

            from allonias3 import S3Path

            nb_path = S3Path("notebooks")
            # Check if the path corresponds to an existing folder or file
            nb_path.exists()
            # True ('notebooks' should always exist in your bucket)
            nb_path.is_dir()
            # False
            nb_path.is_file()
            # Shows the content of the 'notebooks' directory, if exists.
            # run help(S3Path.content) for more info.
            files = nb_path.content(recursive=...)  # default is resursive=True

            data_path = nb_path / "dataset" / "test.csv"
            # Could be true
            data_path.is_file()
            # Read from a file
            data = data_path.read()

            # Points to notebooks/dataset
            dataset_path = data_path.parent
            # Write to a file
            (dataset_path / "test2.csv").write(data)

    Two S3Path instances are equal if they point to the same path on S3 and on
    the same bucket.

    All S3Path instances are absolute, and the following statements would be
    true:

    .. code-block:: python

        from allonias3 import S3Path

        S3Path() == S3Path("")
        S3Path() == S3Path(None)
        S3Path() == S3Path(".")
        S3Path() == S3Path("/")

    All paths from the previous example point to the root of the bucket.

    Things you can not do:

      * Delete the 'notebooks', '.config' and '.logs' directories.
      * Create the 'notebooks', '.config' and '.logs' files (since they
        should be directories)
      * Create a file if there already is a directory at the same path
      * Create/delete/write to a '.s3keep' file yourself
      * Do anything to the bucket's root directly.

    Please read the documentation for
    :obj:`~allonias3.base_path.BasePath.object_type`,
    :obj:`~allonias3.base_path.BasePath.read` and
    :obj:`~allonias3.base_path.BasePath.write`.
    """
