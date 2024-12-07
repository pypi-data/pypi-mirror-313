from dataclasses import fields, is_dataclass
from datetime import date
from enum import Enum
from inspect import isclass
from types import UnionType
from typing import get_args, get_origin, Any
from uuid import UUID


def cast_value(value: Any, target_type: Any, field_name: str | None = None) -> Any:
    origin = get_origin(target_type)
    origin_args = get_args(target_type)

    if origin is None and isinstance(value, target_type):
        return value
    if type(value) in origin_args:
        return value

    # of course union types are a special case
    if origin is UnionType and type(None) in origin_args:
        if value is None:
            return None
        target_type = [arg for arg in origin_args if arg is not type(None)][0]
    if value is None:
        raise ValueError(f"Missing required value for field `{field_name}`")
    if target_type == date and isinstance(value, str):
        return date.fromisoformat(value)
    if target_type in (int, float, str, UUID):
        return target_type(value)
    if is_dataclass(target_type):
        return instantiate_dataclass(target_type, value)  # type: ignore[arg-type]
    if isclass(target_type) and issubclass(target_type, Enum):
        return target_type(value)
    if origin is list:
        item_type = get_args(target_type)[0]
        return [cast_value(item, item_type) for item in value]
    if origin is dict:
        key_type, value_type = get_args(target_type)
        return {
            cast_value(k, key_type): cast_value(v, value_type) for k, v in value.items()
        }
    raise TypeError(f"Cannot cast {value} to {target_type}")


def instantiate_dataclass(cls: type[Any], data: dict[Any, Any]) -> Any:
    if not is_dataclass(cls) or not isclass(cls):
        raise ValueError(f"{cls} is not a dataclass")

    try:
        init_values = {
            field.name: cast_value(data.get(field.name), field.type, field.name)
            for field in fields(cls)
        }
    except (ValueError, TypeError) as e:
        raise ValueError(f"Error instantiating {cls.__name__}:\n\t{e}") from e
    return cls(**init_values)
