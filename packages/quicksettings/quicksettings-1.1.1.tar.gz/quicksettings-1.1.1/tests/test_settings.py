import pytest

from .conftest import (
    BasicSettings,
    BoolSettings,
    BasicListSettings,
    BasicDictSettings,
    DefaultFactorySettings,
    EnumSettings,
    EnvType,
    ForwardRefSettings,
    LiteralSettings,
    MultipleUnionSettings,
    NestedDataSettings,
    NestedMappingSettings,
    NullableSettings,
    UnionSettings,
)


def test_literal_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("WEIGHT", "0.085")
    monkeypatch.setenv("PORT", "8080")
    monkeypatch.setenv("DESCRIPTION", "This is a test")
    settings = BasicSettings()
    assert settings.DEBUG is True
    assert settings.WEIGHT == 0.085
    assert settings.PORT == 8080
    assert settings.DESCRIPTION == "This is a test"


def test_env_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_DEBUG", "true")
    monkeypatch.setenv("APP_WEIGHT", "0.085")
    monkeypatch.setenv("APP_PORT", "8080")
    monkeypatch.setenv("APP_DESCRIPTION", "This is a test")
    monkeypatch.setattr(BasicSettings, "env_prefix", "APP_")
    settings = BasicSettings()
    assert settings.DEBUG is True
    assert settings.WEIGHT == 0.085
    assert settings.PORT == 8080
    assert settings.DESCRIPTION == "This is a test"


def test_missing_required_str_field(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("WEIGHT", "0.085")
    monkeypatch.setenv("PORT", "8080")
    with pytest.raises(ValueError):
        BasicSettings()


@pytest.mark.parametrize(
    "value", ["true", "1", "yes", "y", "t", "TRUE", "YES", "Y", "T"]
)
def test_true_bool_values(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv("DEBUG", value)
    settings = BoolSettings()
    assert settings.DEBUG is True


@pytest.mark.parametrize(
    "value", ["false", "0", "no", "n", "f", "FALSE", "NO", "N", "F"]
)
def test_false_bool_values(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv("DEBUG", value)
    settings = BoolSettings()
    assert settings.DEBUG is False


@pytest.mark.parametrize("value", ["treu", "fasl", "production", "debug", "who"])
def test_invalid_bool_values(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv("DEBUG", value)
    with pytest.raises(ValueError):
        BoolSettings()


def test_basic_list_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTHING_SCARY", "[1,2,3,4.4,5]")
    settings = BasicListSettings()
    assert settings.NOTHING_SCARY == [1, 2, 3, 4.4, 5]


def test_invalid_list_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTHING_SCARY", "[1,2,3,4,5,'hello']")
    with pytest.raises(TypeError):
        BasicListSettings()


def test_basic_dict_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MAPPINGS", '{"follow": "me", "to": "face"}')
    settings = BasicDictSettings()
    assert settings.MAPPINGS == {"follow": "me", "to": "face"}


def test_nested_data_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "NESTED",
        '[{"wrecklessly": "swallow", "blunted": "knives"}, {"wrecklessly": "follow", "blunted": "minds"}]',
    )
    settings = NestedDataSettings()
    assert settings.NESTED == [
        {"wrecklessly": "swallow", "blunted": "knives"},
        {"wrecklessly": "follow", "blunted": "minds"},
    ]


def test_nested_mapping_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "STILL_NOT_SCARY",
        '{"wrecklessly": ["swallow", "follow"], "blunted": ["knives", "minds"]}',
    )
    settings = NestedMappingSettings()
    assert settings.STILL_NOT_SCARY == {
        "wrecklessly": ["swallow", "follow"],
        "blunted": ["knives", "minds"],
    }


def test_allow_nullable() -> None:
    settings = NullableSettings()
    assert settings.DEBUG is None


def test_literal_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "dev")
    settings = LiteralSettings()
    assert settings.ENVIRONMENT == "dev"


def test_invalid_literal_field(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "abrokenskyspills")
    with pytest.raises(ValueError):
        LiteralSettings()


def test_required_missing_literal_field() -> None:
    with pytest.raises(ValueError):
        LiteralSettings()


def test_default_factory() -> None:
    settings = DefaultFactorySettings()
    assert settings.ONE_TWO_THREE == [1, 2, 3]


def test_env_default_factory_priority(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ONE_TWO_THREE", "[4,5,6]")
    settings = DefaultFactorySettings()
    assert settings.ONE_TWO_THREE == [4, 5, 6]


def test_enum_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "qa")
    settings = EnumSettings()
    assert settings.ENVIRONMENT == EnvType.QA


def test_forward_ref_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "hello")
    with pytest.raises(ValueError):
        ForwardRefSettings()


def test_union_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NAME", "karl")
    monkeypatch.setenv("AGE", "999")
    settings = UnionSettings()
    assert settings.NAME == "karl"
    assert settings.AGE == 999


def test_multiple_union_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NAME", "karl")
    with pytest.raises(ValueError):
        MultipleUnionSettings()
