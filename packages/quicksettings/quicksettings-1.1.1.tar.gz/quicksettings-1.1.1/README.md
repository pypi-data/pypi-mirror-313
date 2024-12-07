# quicksettings
A zero dependency package to manage python application configuration.

## Installation

`pip install quicksettings`

## Getting started

```py
from dataclasses import InitVar, dataclass

from quicksettings import BaseSettings


@dataclass(init=False)
class Settings(BaseSettings):
    env_prefix: InitVar[str] = "FOO_"

    USERNAME: str
    PASSWORD: str = "slightly-secret"


settings = Settings()
```

The snippet above will set the value of `settings.USERNAME` to the value of the `FOO_USERNAME` environment variable.
`settings.PASSWORD` will default to the supplied value if the related environment variable is not set. Thus, environment variables take precedence over defaults.

If fields with no defaults are declared without corresponding environment variables, an exception will be raised.

## Supported field types

* `str`
* `int`
* `float`
* `bool`
* `Enum`
* `list`
* `dict`

## New in v1.1.0

* Other dataclasses

Example environment:
```bash
export POWER_SOURCES='[{"name":"coal","output": 20},{"name":"nuclear","output": 10000}]'
```
```py
from dataclasses import dataclass, is_dataclass

from quicksettings import BaseSettings


@dataclass
class PowerSource:
    name: str
    output: int


@dataclass(init=False)
class Settings(BaseSettings):
    POWER_SOURCES: list[PowerSource]


settings = Settings()
assert is_dataclass(settings.POWER_SOURCES[0])  # True
assert settings.POWER_SOURCES[1].name == "nuclear"  # True
```

## Known limitations

* Since we're working with vanilla dataclasses, values with defaults cannot be defined before values without defaults. If your application is running python >= 3.10, the dataclass `kw_only` arg can be supplied.
* No dotenv support - it's up to you to set up the environment.
* Field names are case sensitive by default
* Union field types other than `<type> | None` will raise an exception 
