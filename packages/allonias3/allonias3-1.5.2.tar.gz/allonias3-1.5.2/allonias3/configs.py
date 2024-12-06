from typing import Union

from alloniaconfigs import Configs as BaseConfigs
from pydantic import UUID4, BaseModel, Field, HttpUrl


class ConfigSchema(BaseModel):
    USER_TOKEN_ID: Union[str, None] = Field(None, min_length=16, max_length=16)
    USER_TOKEN_SECRET: Union[str, None] = Field(
        None, min_length=32, max_length=32
    )
    TRACK_ID: Union[UUID4, None] = Field(None)
    PROJECT_ID: Union[UUID4, None] = Field(None)
    USER_ID: Union[UUID4, None] = Field(None)
    USER_ARN: Union[str, None] = Field(None)
    BUCKET_NAME: Union[str, None] = Field(None, min_length=1)
    S3_PROXY_URL: Union[HttpUrl, None] = Field(None)
    USE_BOTO: bool = Field(False)
    REGION_NAME: str = Field("XXXX", min_length=1)


class Configs(BaseConfigs):
    schema = ConfigSchema

    @property
    def user_id(self) -> Union[UUID4, None]:
        if not (user_id := self.USER_ID):
            user_id = self.USER_ARN.split("/")[-1] if self.USER_ARN else None
        return user_id

    @property
    def s3_proxy_url(self) -> Union[str, None]:
        return (
            str(self.S3_PROXY_URL) if self.S3_PROXY_URL else self.S3_PROXY_URL
        )

    @property
    def bucket_name(self) -> Union[str, None]:
        """Holds the env var BUCKET_NAME, or constructs the persistent bucket
        name from the track id, or None."""
        return (
            self.BUCKET_NAME
            if self.BUCKET_NAME
            else (
                f"track--{self.TRACK_ID}--persistent" if self.TRACK_ID else None
            )
        )

    @property
    def persistent_bucket_name(self) -> Union[str, None]:
        """From :obj:`~Envs.bucket_name`, will construct the persistent bucket
        name (if different) and return it. Returns None if neither the bucket
        name nor the track ID were defined in the env vars."""
        return (
            self.bucket_name.replace("non-persistent", "persistent")
            if self.bucket_name is not None
            and self.bucket_name.endswith("non-persistent")
            else self.bucket_name
        )

    @property
    def non_persistent_bucket_name(self) -> Union[str, None]:
        """From :obj:`~Envs.bucket_name`, will construct the non-persistent
        bucket name (if different) and return it. Returns None if neither the
        bucket name nor the track ID were defined in the env vars."""
        return (
            self.bucket_name.replace("persistent", "non-persistent")
            if self.bucket_name is not None
            and not self.bucket_name.endswith("non-persistent")
            else self.bucket_name
        )
