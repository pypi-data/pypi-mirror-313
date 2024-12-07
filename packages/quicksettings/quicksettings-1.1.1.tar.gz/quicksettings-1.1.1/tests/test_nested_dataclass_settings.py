import pytest

from .conftest import NestedDataclassSettings, District, Location


def test_nested_dataclass_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NAME", "Force the issue")
    monkeypatch.setenv(
        "DISTRICTS",
        "[{'name': 'Numineer Blas', 'population': 123, 'location': {'lat': 1.0, 'long': 2.0}}]",
    )
    monkeypatch.setenv("HEAD_OFFICE_LOCATION", '{"lat": 3.0, "long": 4.0}')
    settings = NestedDataclassSettings()
    assert settings.NAME == "Force the issue"
    district = settings.DISTRICTS[0]
    assert isinstance(district, District)
    assert district.name == "Numineer Blas"
    assert district.population == 123
    assert isinstance(district.location, Location)
    assert district.location.lat == 1.0
    assert isinstance(settings.HEAD_OFFICE_LOCATION, Location)
    assert settings.HEAD_OFFICE_LOCATION.lat == 3.0
