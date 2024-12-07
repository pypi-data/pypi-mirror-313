from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

from quicksettings import BaseSettings


@dataclass(init=False)
class BasicSettings(BaseSettings):
    env_prefix = ""

    DEBUG: bool
    WEIGHT: float
    PORT: int
    DESCRIPTION: str


@dataclass(init=False)
class BoolSettings(BaseSettings):
    DEBUG: bool


@dataclass(init=False)
class BasicListSettings(BaseSettings):
    NOTHING_SCARY: list[int | float]


@dataclass(init=False)
class BasicDictSettings(BaseSettings):
    MAPPINGS: dict[str, str]


@dataclass(init=False)
class NestedDataSettings(BaseSettings):
    NESTED: list[dict[str, str]]


@dataclass(init=False)
class NestedMappingSettings(BaseSettings):
    STILL_NOT_SCARY: dict[str, list[str]]


@dataclass(init=False)
class NullableSettings(BaseSettings):
    DEBUG: bool | None


@dataclass(init=False)
class LiteralSettings(BaseSettings):
    ENVIRONMENT: Literal["dev", "qa", "prod"]


@dataclass(init=False)
class DefaultFactorySettings(BaseSettings):
    ONE_TWO_THREE: list[int] = field(default_factory=lambda: [1, 2, 3])


class EnvType(Enum):
    DEV = "dev"
    QA = "qa"
    PROD = "prod"


@dataclass(init=False)
class EnumSettings(BaseSettings):
    ENVIRONMENT: EnvType


@dataclass(init=False)
class ForwardRefSettings(BaseSettings):
    ENVIRONMENT: "EnvType"


@dataclass(init=False)
class UnionSettings(BaseSettings):
    NAME: str | None
    AGE: int | None


@dataclass(init=False)
class MultipleUnionSettings(BaseSettings):
    NUMBER: int | str | None  # unsupported


@dataclass
class Location:
    lat: float
    long: float


@dataclass
class District:
    name: str
    population: int
    location: Location


@dataclass(init=False)
class NestedDataclassSettings(BaseSettings):
    NAME: str
    DISTRICTS: list[District]
    HEAD_OFFICE_LOCATION: Location
