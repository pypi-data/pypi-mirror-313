import logging
import traceback
from pathlib import Path
from typing import Any

import cloudpickle
import dill  # nosec

logger = logging.getLogger("allonias3.encoder_decoder.basic")


class _BasicEncoderDecoder:
    """Astract class to handle encoding, decoding and appending.

    Used when the dependencies for
    :obj:`~allonias3.encoder_decoder.advanced._EncoderDecoder` have not been
    installed (can be done with `pip install allonias3[datatypehandler]`).
    """

    def __init__(self, s3key: str, encoding: str = "utf-8", *_, **__):
        self.s3key = s3key
        self.encoding = encoding

    def __call__(self, content, **kwargs):
        if content is None:
            return self._code_none(**kwargs)

        type_encoder = f"_code_type_{content.__class__.__name__}"
        if hasattr(self, type_encoder):
            return getattr(self, type_encoder)(content, **kwargs)

        return self.default(content, **kwargs)

    def default(self, content, **kwargs) -> Any:
        """When neither the file extension nor the content type match
        a home-made method, this method is used.
        """

    def _code_deactivated(self, content, **_):
        raise NotImplementedError

    def _code_none(self, **kwargs):
        """How to handle :inlinepython:`content = None`."""


class _BasicEncoder(_BasicEncoderDecoder):
    """Basic encoder that will endode strings into a specified encoding
    and pickle all other data types.
    """

    def _code_type_str(self, content: str, **_) -> bytes:
        return content.encode(self.encoding)

    def _code_deactivated(self, content, **_) -> bytes:
        if isinstance(content, str):
            return self._code_type_str(content)
        return self.default(content)

    def _code_none(self, **_) -> bytes:
        return self._code_type_str("")

    def default(self, content, **_) -> bytes:
        return cloudpickle.dumps(content)


class _BasicDecoder(_BasicEncoderDecoder):
    """Basic encoder that will decode strings with a specified encoding
    and unpickle all other data types.
    """

    def __init__(
        self,
        s3key: str,
        encoding: str = "utf-8",
        *,
        raise_if_unpickle_fails: bool = False,
        **_,
    ):
        self.raise_if_unpickle_fails = raise_if_unpickle_fails
        self._opened_file = None
        super().__init__(s3key, encoding)

    def _get_body(self, content: dict):
        if "Body" in content:
            return content["Body"]
        if "LocalPath" in content:
            self._opened_file = Path(content["LocalPath"]).open("rb")  # noqa: SIM115
            return self._opened_file
        raise ValueError(
            "Invalid content passed to '_get_body'. Must contain the key"
            "'Body' or 'LocalPath'."
        )

    @staticmethod
    def _code_type_str(content: str, **_) -> str:
        return content

    def _code_type_bytes(self, content: bytes, **_) -> Any:
        try:
            return content.decode(self.encoding)
        except Exception:
            try:
                return dill.loads(content)  # nosec
            except Exception as error:
                if self.raise_if_unpickle_fails:
                    raise error
                logger.warning(
                    f"Could not properly decode {self.s3key}: "
                    f"{traceback.format_exc()}"
                )
                return content

    def _code_deactivated(self, content, **_) -> Any:
        return self.default(content)

    def _code_none(self, **_) -> str:
        return ""

    def default(self, content, **_) -> Any:
        if hasattr(content, "__getitem__") and (
            "Body" in content or "LocalPath" in content
        ):
            content = self._get_body(content)
            if hasattr(content, "read"):
                content = content.read()
            if isinstance(content, str):
                return self._code_type_str(content)
            return self._code_type_bytes(content)
        return str(content)

    def close(self):
        pass


class _BasicAppender(_BasicEncoderDecoder):
    """Basic appender that will only append strings to strings."""

    def __init__(self, s3key: str, encoding: str = "utf-8", *_, **__):
        self.encoder = _BasicEncoder(s3key, encoding)
        super().__init__(s3key, encoding)

    def __call__(self, existing_content, content=None, **kwargs):
        return super().__call__(
            content, existing_content=existing_content, **kwargs
        )

    def default(self, content: str, existing_content: str = "", **_) -> bytes:
        if not isinstance(existing_content, str):
            raise TypeError(
                f"Cannot append to {self.s3key} because the existing content "
                f"is not a string but a {type(existing_content)}."
            )
        if not isinstance(content, str):
            raise TypeError(
                f"Cannot append to {self.s3key} because the content to append "
                f"is not a string but a {type(content)}."
            )
        return self.encoder(f"{existing_content}{content}")

    def _code_deactivated(self, content, **kwargs) -> bytes:
        return self.default(content, **kwargs)

    def _code_none(self, existing_content, **kwargs):
        return self.encoder(existing_content, **kwargs)
