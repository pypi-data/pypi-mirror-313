from types import FunctionType

from pydantic import BaseModel

from connector.shared_types import PydanticModel


def collect_methods(obj: object) -> list[FunctionType]:
    """
    Collect all methods from an object.
    """
    return [
        getattr(obj, method)
        for method in dir(obj)
        if not method.startswith("_")
        and callable(getattr(obj, method))
        and method not in ("validate",)
    ]


def is_pydantic_model(cls: type | None) -> bool:
    if cls is None:
        return False
    for _base_model in PydanticModel:
        if issubclass(cls, _base_model):
            return True
    return False


def get_pydantic_model(annotations: dict[str, type]) -> type[BaseModel]:
    for key, val in annotations.items():
        if key in ("return",):
            continue
        if is_pydantic_model(val):
            return val  # type: ignore
    raise ValueError("No Pydantic model found in annotations.")
