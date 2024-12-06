import io
import json
import logging
import tempfile
from copy import copy
from datetime import date, datetime
from functools import cached_property
from io import BufferedReader
from pathlib import Path
from typing import Any, BinaryIO, ClassVar, Union

import h5py

# Not used directly, but if not explicitely imported, reading HDF5 files fails.
import hdf5plugin  # noqa: F401
import numpy as np
import pandas as pd
from dateutil import parser as dateparser

from .basic import (
    _BasicAppender,
    _BasicDecoder,
    _BasicEncoder,
    _BasicEncoderDecoder,
)

logger = logging.getLogger("allonias3.encoder_decoder.advanced")


class _EncoderDecoder(_BasicEncoderDecoder):
    """Abstract class to handle encoding, decoding and appending with several
    file extensions (**.csv**, **.xls**, **.xlsx**, **.xlsm**, **.xlsb**,
    **.odf**, **.ods**, **.odt****.parquet**, **.npy** and **.json**) and with
    several content types (:obj:`pandas.DataFrame`, :obj:`pandas.Series`,
    :obj:`numpy.ndarray`, :obj:`str`, :obj:`bytes` and :obj:`dict`).

    Other types and extensions are handled with a default method.

    An instance must be created, then called with a content to handle. Based
    on the s3key suffix or the content type, a specific method is called.

    The instance can be disabled, if the user wants to handle conversion
    him/herself, by setting :inlinepython:`deactivate=True`.

    You can add support for more extensions or content type by defining the
    :inlinepython:`_code_suffix_<extension>` method or
    :inlinepython:`_code_type_<classname>` method.
    """

    expected_suffix_types: ClassVar[dict[str, Union[tuple, type]]] = {
        ".csv": (pd.DataFrame, pd.Series),
        ".parquet": (pd.DataFrame, pd.Series),
        ".xls": (pd.DataFrame, pd.Series, bytes, io.BytesIO),
        ".xlsx": (pd.DataFrame, pd.Series, bytes, io.BytesIO),
        ".xlsm": (pd.DataFrame, pd.Series, bytes, io.BytesIO),
        ".xlsb": (pd.DataFrame, pd.Series, bytes, io.BytesIO),
        ".odf": (pd.DataFrame, pd.Series, bytes, io.BytesIO),
        ".ods": (pd.DataFrame, pd.Series, bytes, io.BytesIO),
        ".odt": (pd.DataFrame, pd.Series, bytes, io.BytesIO),
        ".json": dict,
        ".npy": np.ndarray,
        ".h5": (bytes, h5py.File, io.BufferedReader),
    }
    """Force the object type that some file extensions can handle."""

    expected_types_suffix: ClassVar[dict[type, Union[tuple, str]]] = {
        pd.DataFrame: (
            ".csv",
            ".parquet",
            ".xls",
            ".xlsx",
            ".xlsm",
            ".xlsb",
            ".odf",
            ".ods",
            ".odt",
        ),
        pd.Series: (
            ".csv",
            ".parquet",
            ".xls",
            ".xlsx",
            ".xlsm",
            ".xlsb",
            ".odf",
            ".ods",
            ".odt",
        ),
        dict: ".json",
        np.ndarray: ".npy",
        h5py.File: ".h5",
    }
    """Force the file extension in which some object types can be written."""

    _check_type: ClassVar[bool] = True

    def __init__(
        self, s3key: str, encoding: str = "utf-8", *, deactivate: bool = False
    ):
        super().__init__(s3key, encoding)
        self.suffix = Path(s3key).suffix
        self.force_pickle = deactivate

    def __call__(self, content, **kwargs):
        if self.force_pickle:
            return self._code_deactivated(content, **kwargs)

        self.check_type(content)

        if content is None:
            return self._code_none(**kwargs)

        suffix_encoder = f"_code_suffix_{self.suffix.lstrip('.')}"
        if hasattr(self, suffix_encoder):
            return getattr(self, suffix_encoder)(content, **kwargs)

        type_encoder = f"_code_type_{content.__class__.__name__}"
        if hasattr(self, type_encoder):
            return getattr(self, type_encoder)(content, **kwargs)

        return self.default(content, **kwargs)

    def check_type(self, content):
        """Not all content types can be written to all file extensions :
        Trying to write a :obj:`pandas.DataFrame` to a .txt will fail, and
        trying to write something that is not a :obj:`pandas.DataFrame` or
        :obj:`pandas.Series` to a **.csv** will fail too.
        """
        if not self._check_type:
            return

        if self.suffix in self.expected_suffix_types and not isinstance(
            content, self.expected_suffix_types[self.suffix]
        ):
            raise TypeError(
                f"Can only write objects of type "
                f"{self.expected_suffix_types[self.suffix]} to "
                f"{self.suffix} files, not a {type(content)}."
            )

        content_type = content.__class__
        if (
            content_type in self.expected_types_suffix
            and self.suffix not in self.expected_types_suffix[content_type]
        ):
            raise TypeError(
                f"Can only write objects of type "
                f"{content_type} to {self.expected_types_suffix[content_type]}"
                f" files, not to {self.suffix} files."
            )


class _Encoder(_EncoderDecoder, _BasicEncoder):
    """Encoder.
    Will encode :obj:`pandas.DataFrame` and :obj:`pandas.Series` to **.csv**,
    **.xls**, **.xlsx**, **.xlsm**, **.xlsb**, **.odf**,
    **.ods**, **.odt** or **.parquet** using :obj:`pandas.DataFrame.to_csv`,
    using :obj:`pandas.DataFrame.to_excel` or
    :obj:`pandas.DataFrame.to_parquet`, :obj:`dict` to **.json** using
    :obj:`json.dumps`, :obj:`numpy.ndarray` to **.npy** using
    `cloudpickle <https://github.com/cloudpipe/cloudpickle>`_
    dumps, :obj:`str` to any other extension using :obj:`str.encode` and
    any other type to any other extension using
    `cloudpickle <https://github.com/cloudpipe/cloudpickle>`_ dumps.
    Passing :inlinepython:`content = None`  will change it to an empty
    :obj:`str`, then encode it. If deactivated, just returns the input content
    (except for :inlinepython:`content = None`, that will still be changed to an
    empty :obj:`str`, but not encoded).
    """

    @staticmethod
    def _code_suffix_bst(content, **_) -> bytes:
        return content.get_booster().save_raw(raw_format="deprecated")

    def _code_suffix_json(self, content: dict, **kwargs) -> bytes:
        return json.dumps(content, cls=JSONEncoder, **kwargs).encode(
            self.encoding
        )

    @staticmethod
    def _code_suffix_parquet(content, **kwargs) -> io.BytesIO:
        as_file = io.BytesIO()
        content.to_parquet(as_file, **kwargs)
        as_file.seek(0)
        return as_file

    @staticmethod
    def _code_suffix_h5(content, **_) -> Union[BinaryIO, BufferedReader]:
        if isinstance(content, h5py.File):
            if content.name is None:
                raise ValueError("Can not save a closed HDF5 file.")
            with tempfile.NamedTemporaryFile() as tmp:
                with h5py.File(tmp, "w") as h5tmp:
                    for key in content:
                        content.copy(key, h5tmp)
                return Path(tmp.name).open("rb")  # noqa: SIM115
        return content

    def _code_suffix_csv(self, content, **kwargs) -> io.BytesIO:
        as_file = io.BytesIO()
        content.to_csv(as_file, encoding=self.encoding, **kwargs)
        as_file.seek(0)
        return as_file

    # jscpd:ignore-start

    def _code_suffix_xls(self, content, **kwargs) -> io.BytesIO:
        return self._code_excel(content, **kwargs)

    def _code_suffix_xlsx(self, content, **kwargs) -> io.BytesIO:
        return self._code_excel(content, **kwargs)

    def _code_suffix_xlsm(self, content, **kwargs) -> io.BytesIO:
        return self._code_excel(content, **kwargs)

    def _code_suffix_xlsb(self, content, **kwargs) -> io.BytesIO:
        return self._code_excel(content, **kwargs)

    def _code_suffix_odf(self, content, **kwargs) -> io.BytesIO:
        return self._code_excel(content, **kwargs)

    def _code_suffix_ods(self, content, **kwargs) -> io.BytesIO:
        return self._code_excel(content, **kwargs)

    def _code_suffix_odt(self, content, **kwargs) -> io.BytesIO:
        return self._code_excel(content, **kwargs)

    # jscpd:ignore-end

    @staticmethod
    def _code_excel(content, **kwargs) -> Union[bytes, io.BytesIO]:
        if isinstance(content, (bytes, io.BytesIO)):
            return content
        as_file = io.BytesIO()
        content.to_excel(as_file, **kwargs)
        as_file.seek(0)
        return as_file


class _Decoder(_EncoderDecoder, _BasicDecoder):
    """Decoder.
    Will decode :obj:`pandas.DataFrame` and :obj:`pandas.Series`
    from **.csv**, **.xls**, **.xlsx**, **.xlsm**, **.xlsb**, **.odf**,
    **.ods**, **.odt** or **.parquet** using :obj:`pandas.read_csv`,
    :obj:`pandas.read_excel` or
    :obj:`pandas.read_parquet`, :obj:`dict` from **.json** using
    :obj:`json.loads`, :obj:`numpy.ndarray` from **.npy** using
    :obj:`dill.loads`, and any other type assuming it is :obj:`bytes` using
    :obj:`bytes.decode`. If that fails, will try :obj:`dill.loads`. If it fails
    too, returns the content as-is, unless if
    :inlinepython:`raise_if_unpickle_fails=True` was passed when the object was
    created, in which case it raises the error. :obj:`str` does not need
    decoding. Passing :inlinepython:`content=None` will change it to an empty
    :obj:`str`. If deactivated, just returns the input content (except for
    :inlinepython:`content = None`, that will still be changed to an empty
    :obj:`str`).

    Special treatment for :obj:`dict` containing the key "Body": will
    decode the value associated to the key. If this value has the
    :inlinepython:`read` method, will call it before decoding.
    That remains true when deactivated.
    """

    _check_type = False

    def __init__(
        self,
        s3key: str,
        encoding: str = "utf-8",
        *,
        raise_if_unpickle_fails: bool = False,
        deactivate: bool = False,
    ):
        self.raise_if_unpickle_fails = raise_if_unpickle_fails
        self._opened_file = None
        super().__init__(s3key, encoding, deactivate=deactivate)

    def _code_suffix_parquet(self, content: dict, **kwargs):
        content = self._get_body(content)
        if not isinstance(content, bytes):
            content = content.read()
        result = pd.read_parquet(
            io.BytesIO(content),
            engine="pyarrow",
            **kwargs,
        )
        self.close()
        return result

    def _code_suffix_h5(self, content: dict, **_):
        if "LocalPath" in content:
            self._opened_file = Path(content["LocalPath"]).open("rb")  # noqa: SIM115
            return self._opened_file
        # HDF5 works a bit differently, needs a file path or a stream.
        # So do not call _get_body, which would open the file.
        return h5py.File(io.BytesIO(content["Body"].read()))

    # jscpd:ignore-start

    def _code_suffix_xls(self, content: dict, **kwargs):
        return self._code_excel(content, **kwargs)

    def _code_suffix_xlsx(self, content: dict, **kwargs):
        return self._code_excel(content, **kwargs)

    def _code_suffix_xlsm(self, content: dict, **kwargs):
        return self._code_excel(content, **kwargs)

    def _code_suffix_odf(self, content: dict, **kwargs):
        return self._code_excel(content, **kwargs)

    def _code_suffix_ods(self, content: dict, **kwargs):
        return self._code_excel(content, **kwargs)

    def _code_suffix_odt(self, content: dict, **kwargs):
        return self._code_excel(content, **kwargs)

    # jscpd:ignore-end

    def _code_suffix_csv(self, content: dict, **kwargs):
        content = self._get_body(content)
        if isinstance(content, bytes):
            content = io.BytesIO(content)
        if self.encoding and self.encoding != "utf-8":
            content = io.TextIOWrapper(content, encoding=self.encoding)
        result = pd.read_csv(content, **kwargs)
        self.close()
        return result

    def _code_suffix_json(self, content: dict, **kwargs) -> dict:
        body = self._get_body(content)
        if hasattr(body, "read"):
            body = body.read()
        result = json.loads(body, object_hook=json_obj_hook, **kwargs)
        self.close()
        return result

    def _code_excel(self, content: dict, **kwargs):
        content = self._get_body(content)
        if not isinstance(content, bytes):
            content = content.read()
        result = pd.read_excel(io.BytesIO(content), **kwargs)
        self.close()
        return result

    def _code_deactivated(self, content, **_):
        return self.default(content)

    def close(self):
        if self._opened_file:
            self._opened_file.close()


class _Appender(_EncoderDecoder, _BasicAppender):
    """Will handle:

     * **.json** files (existing content and new content must be :obj:`dict`),
       using :obj:`dict.update`.
     * **.csv**, **.xls**, **.xlsx**, **.xlsm**, **.xlsb**, **.odf**, **.ods**,
       **.odt** or **.parquet** (existing content and new content must be
       :obj:`pandas.DataFrame` or :obj:`pandas.Series`), using
       :obj:`pandas.concat`.
     * **.npy** file (existing content and new content must be
       :obj:`numpy.ndarray`), using :obj:`numpy.concatenate`.
     * Any other file type (existing content must be a :obj:`str`, new content
       must be a :obj:`str` or :inlinepython:`None`),
       appending with a new line between current and new data.

    Returns an encoded object ready to be sent to S3.
    """

    def __init__(
        self, s3key: str, encoding: str = "utf-8", *, deactivate: bool = False
    ):
        super().__init__(s3key, encoding, deactivate=deactivate)
        self.encoder = _Encoder(s3key, encoding, deactivate=deactivate)

    def __call__(self, existing_content, content=None, **kwargs):
        return super().__call__(
            content, existing_content=existing_content, **kwargs
        )

    def _code_suffix_json(
        self,
        content: dict,
        existing_content: dict,
        write_kwargs=None,
        **_,
    ) -> str:
        if write_kwargs is None:
            write_kwargs = {}
        existing_content = copy(existing_content)
        existing_content.update(content)
        return self.encoder(existing_content, **write_kwargs)

    # jscpd:ignore-start

    def _code_suffix_xls(
        self, content, existing_content, write_kwargs=None, append_kwargs=None
    ) -> io.BytesIO:
        return self._append_pandas(
            content, existing_content, write_kwargs, append_kwargs
        )

    def _code_suffix_xlsx(
        self, content, existing_content, write_kwargs=None, append_kwargs=None
    ) -> io.BytesIO:
        return self._append_pandas(
            content, existing_content, write_kwargs, append_kwargs
        )

    def _code_suffix_xlsm(
        self, content, existing_content, write_kwargs=None, append_kwargs=None
    ) -> io.BytesIO:
        return self._append_pandas(
            content, existing_content, write_kwargs, append_kwargs
        )

    def _code_suffix_odf(
        self, content, existing_content, write_kwargs=None, append_kwargs=None
    ) -> io.BytesIO:
        return self._append_pandas(
            content, existing_content, write_kwargs, append_kwargs
        )

    def _code_suffix_ods(
        self, content, existing_content, write_kwargs=None, append_kwargs=None
    ) -> io.BytesIO:
        return self._append_pandas(
            content, existing_content, write_kwargs, append_kwargs
        )

    def _code_suffix_odt(
        self, content, existing_content, write_kwargs=None, append_kwargs=None
    ) -> io.BytesIO:
        return self._append_pandas(
            content, existing_content, write_kwargs, append_kwargs
        )

    # jscpd:ignore-end

    def _code_suffix_csv(
        self, content, existing_content, write_kwargs=None, append_kwargs=None
    ) -> io.BytesIO:
        return self._append_pandas(
            content, existing_content, write_kwargs, append_kwargs
        )

    def _code_suffix_parquet(
        self, content, existing_content, write_kwargs=None, append_kwargs=None
    ) -> io.BytesIO:
        return self._append_pandas(
            content, existing_content, write_kwargs, append_kwargs
        )

    @staticmethod
    def _code_suffix_h5(_, __, **___):
        raise ValueError("Can not append to HDF5 file.")

    def _code_suffix_npy(
        self,
        content: np.ndarray,
        existing_content: np.ndarray,
        write_kwargs=None,
        append_kwargs=None,
    ) -> bytes:
        if write_kwargs is None:
            write_kwargs = {}
        if append_kwargs is None:
            append_kwargs = {}
        return self.encoder(
            np.concatenate((existing_content, content), **append_kwargs),
            **write_kwargs,
        )

    def _append_pandas(
        self, content, existing_content, write_kwargs=None, append_kwargs=None
    ) -> io.BytesIO:
        if write_kwargs is None:
            write_kwargs = {}
        if append_kwargs is None:
            append_kwargs = {}
        if self.suffix != ".parquet":
            content.columns = content.columns.astype(str)
        return self.encoder(
            pd.concat([existing_content, content], **append_kwargs),
            **write_kwargs,
        )


class JSONEncoder(json.JSONEncoder):
    """Extending the JSON encoder, so it knows how to serialise
    :obj:`~pandas.DataFrame` and :obj:`~numpy.ndarray` objects.

    To do that, dataframes and series are converted to dictionaries, with the
    dataframe or series's values stored using the "__pd.DataFrame__" or
    "__pd.Series__" key. The other relevant attributes are stored in the
    keys "index", "columns" ("name" for series), "dtypes" ("dtype" for series)
    and "datetimeindex" (a boolean indicating if the original index was a
    datetimeindex or not).

    Same idea applies to datetimes, dates, numpy arrays, pd.Timedelta and
    pd.Timestamp.

    Converts datetime and pd.Timestamp objects to string in the
    "%Y-%m-%dT%H:%M:%S" format, and date in the "%Y-%m-%d" format.

    np.integer and np.float objects are converted to regular int or float.

    If the given object is none of the types described above, and has the 'name'
    attribute, will store only the 'name' attribute.

    Decoding is done by looking for the presence of "__pd.DataFrame__",
    "__pd.Series__", "__np.ndarray__", "__pd.Timedelta__", "__datetime__" or
    "__date__" in the given dictionary's keys, using the appropriate methods
    to get the original object back.

    Note that not all caracteristics can be retrieved. For instance, a
    dataframe with a datetime index that has a specific value for 'freq':
    this value will be lost in translation.
    """

    dataframe = "__pd.DataFrame__"
    series = "__pd.Series__"
    array = "__np.ndarray__"
    timedelta = "__pd.Timedelta__"
    datetime = "__datetime__"
    date = "__date__"

    @cached_property
    def conversions(self):
        return {
            pd.DataFrame: self.encode_datafame,
            pd.Series: self.encode_series,
            np.ndarray: self.encode_numpy,
            datetime: lambda x: {self.datetime: x.isoformat()},
            pd.Timestamp: lambda x: {self.datetime: x.isoformat()},
            date: lambda x: {self.date: x.strftime("%Y-%m-%d")},
            pd.Timedelta: lambda x: {self.timedelta: str(x)},
            np.integer: lambda x: int(x),
            np.floating: lambda x: float(x),
        }

    @staticmethod
    def check_keys(keys, dictionary):
        if sorted(dictionary.keys()) != sorted(keys):
            return False
        return True

    def encode_datafame(self, obj: pd.DataFrame):
        return {
            self.dataframe: obj.to_numpy().tolist(),
            "index": tuple(obj.index),
            "columns": tuple(obj.columns),
            "dtypes": dict(obj.dtypes.astype(str)),
            "datetimeindex": isinstance(obj.index, pd.DatetimeIndex),
        }

    def encode_series(self, obj: pd.Series):
        return {
            self.series: obj.to_numpy().tolist(),
            "index": tuple(obj.index),
            "name": obj.name,
            "dtype": str(obj.dtype),
            "datetimeindex": isinstance(obj.index, pd.DatetimeIndex),
        }

    def encode_numpy(self, obj: np.ndarray):
        return {
            self.array: obj.tolist(),
            "dtype": str(obj.dtype),
            "shape": obj.shape,
        }

    @classmethod
    def decode_dataframe(cls, dictionary: dict):
        dataframe = pd.DataFrame(
            dictionary[cls.dataframe], columns=dictionary["columns"]
        )
        columns_are_ints = (
            isinstance(dataframe.columns, pd.Index)
            and dataframe.columns.dtype == "int64"
        )
        index = dictionary["index"]
        dataframe.index = (
            pd.MultiIndex.from_tuples(index)
            if len(index) != 0 and isinstance(index[0], (list, tuple))
            else index
        )
        for column in dictionary["dtypes"]:
            column_in_df = column
            if columns_are_ints:
                column_in_df = int(column)
            dataframe[column_in_df] = (
                pd.to_datetime(dataframe[column_in_df], unit="ms")
                if dictionary["dtypes"][column].startswith("datetime64")
                and np.issubdtype(dataframe[column_in_df].dtype, (int, float))
                else dataframe[column_in_df].astype(
                    dictionary["dtypes"][column]
                )
            )
        if dictionary["datetimeindex"] is True:
            dataframe.index = (
                pd.to_datetime(dataframe.index, unit="ms")
                if np.issubdtype(dataframe.index.dtype, (int, float))
                else pd.DatetimeIndex(dataframe.index)
            )
        return dataframe

    @classmethod
    def decode_series(cls, dictionary: dict):
        series = pd.Series(dictionary[cls.series])
        index = dictionary["index"]
        series.index = (
            pd.MultiIndex.from_tuples(index)
            if len(index) != 0 and isinstance(index[0], (list, tuple))
            else index
        )
        series = (
            pd.to_datetime(series, unit="ms")
            if dictionary["dtype"].startswith("datetime64")
            and np.issubdtype(series.dtype, (int, float))
            else series.astype(dictionary["dtype"])
        )
        series.name = dictionary["name"]
        if dictionary["datetimeindex"] is True:
            series.index = (
                pd.to_datetime(series.index, unit="ms")
                if np.issubdtype(series.index.dtype, (int, float))
                else pd.DatetimeIndex(series.index)
            )
        return series

    @classmethod
    def decode_numpy(cls, dictionary: dict):
        return np.array(dictionary[cls.array], dictionary["dtype"]).reshape(
            dictionary["shape"]
        )

    def default(self, obj: Any):
        type_ = type(obj)
        if type_ in self.conversions:
            return self.conversions[type_](obj)
        if hasattr(obj, "name"):
            return obj.name

        return json.JSONEncoder.default(self, obj)


keys_to_type = {
    (
        JSONEncoder.dataframe,
        "datetimeindex",
        "dtypes",
        "index",
        "columns",
    ): JSONEncoder.decode_dataframe,
    (
        JSONEncoder.series,
        "datetimeindex",
        "dtype",
        "index",
        "name",
    ): JSONEncoder.decode_series,
    (JSONEncoder.array, "dtype", "shape"): JSONEncoder.decode_numpy,
    (JSONEncoder.timedelta,): lambda x: pd.Timedelta(x[JSONEncoder.timedelta]),
    (JSONEncoder.date,): lambda x: datetime.strptime(
        x[JSONEncoder.date], "%Y-%m-%d"
    )
    .astimezone()
    .date(),
    (JSONEncoder.datetime,): lambda x: dateparser.parse(
        x[JSONEncoder.datetime]
    ),
}


def json_obj_hook(dct):
    for keys in keys_to_type:
        if JSONEncoder.check_keys(keys, dct):
            return keys_to_type[keys](dct)
    return dct
