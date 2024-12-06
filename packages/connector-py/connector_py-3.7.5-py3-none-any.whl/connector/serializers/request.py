import typing as t
from enum import Enum

import pydantic


class FieldType(str, Enum):
    SECRET = "SECRET"
    HIDDEN = "HIDDEN"
    MULTI_LINES = "MULTI_LINES"


def _extract_json_schema_extra(**kwargs) -> dict[str, t.Any]:
    json_schema_extra = (
        kwargs.pop("json_schema_extra") if "json_schema_extra" in kwargs else {}
    ) or {}
    return json_schema_extra


def SecretField(*args, **kwargs):
    json_schema_extra = _extract_json_schema_extra(**kwargs)
    json_schema_extra["x-field_type"] = FieldType.SECRET
    return pydantic.Field(*args, json_schema_extra=json_schema_extra, **kwargs)


def HiddenField(*args, **kwargs):
    """
    A field we don't want a user to see + fill out, but not a secret.
    """
    json_schema_extra = _extract_json_schema_extra(**kwargs)
    json_schema_extra["x-field_type"] = FieldType.HIDDEN
    return pydantic.Field(*args, json_schema_extra=json_schema_extra, **kwargs)


def MultiLinesField(*args, **kwargs):
    json_schema_extra = _extract_json_schema_extra(**kwargs)
    json_schema_extra["x-field_type"] = FieldType.MULTI_LINES
    return pydantic.Field(*args, json_schema_extra=json_schema_extra, **kwargs)
