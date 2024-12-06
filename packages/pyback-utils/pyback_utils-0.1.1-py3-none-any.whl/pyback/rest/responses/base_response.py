from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


def to_camel(string: str) -> str:
    components = string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def convert_uuid_in_dict(data: dict) -> dict:
    """
    Itera sobre um dicionário e transforma todos os valores UUID em strings,
    incluindo valores dentro de listas.
    """

    def convert_value(value):
        if isinstance(value, UUID):
            return str(value)
        elif isinstance(value, dict):
            return convert_uuid_in_dict(value)
        elif isinstance(value, list):
            return [convert_value(item) for item in value]
        else:
            return value

    return {k: convert_value(v) for k, v in data.items()}


def convert_datetime_in_dict(data: dict) -> dict:
    """
    Itera sobre um dicionário e transforma todos os valores datetime em strings.
    """
    result = {}
    for k, v in data.items():
        if isinstance(v, datetime):
            result[k] = v.isoformat()
        elif isinstance(v, dict):
            result[k] = convert_datetime_in_dict(v)
        else:
            result[k] = v
    return result


class BaseResponse(BaseModel):
    model_config = ConfigDict(
        strict=False,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True,
    )

    def model_dump(self, **kwargs):
        result = super().model_dump(**kwargs)
        return convert_uuid_in_dict(convert_datetime_in_dict(result))
