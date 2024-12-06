import typing as t

from pydantic import BaseModel

RawDataType: t.TypeAlias = dict[
    str,  # url
    dict[str, t.Any] | None,  # response body, can be None with some responses
]
OptionalRawDataType = RawDataType | None


__all__ = ("PydanticModel", "RawDataType")


def _set_pydantic_model():
    models = [BaseModel]

    try:
        from pydantic.v1 import BaseModel as BaseModelV1

        models.append(BaseModelV1)
    except ImportError:
        pass

    return frozenset(models)


PydanticModel = _set_pydantic_model()
