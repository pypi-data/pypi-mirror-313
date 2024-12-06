import base64
from typing import Optional

from pydantic import BaseModel, field_validator, field_serializer


class BytesBase64Model(BaseModel):

    @field_validator("*", mode="before")
    def decode_base64_bytes(cls, v, info):
        if isinstance(v, str):
            field_name = info.field_name
            model_field = cls.model_fields.get(field_name)
            if model_field is None:
                return v

            # check if is bytes or optional bytes
            if (
                model_field.annotation == bytes
                or model_field.annotation == Optional[bytes]
            ):
                return base64.b64decode(v)
        return v

    @field_serializer("*")
    def serialize_field(self, v, field):
        if isinstance(v, bytes):
            return base64.b64encode(v).decode("utf-8")
        return v
