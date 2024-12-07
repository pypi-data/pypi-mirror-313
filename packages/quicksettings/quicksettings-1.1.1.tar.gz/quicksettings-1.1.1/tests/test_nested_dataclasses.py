from datetime import date
from dataclasses import dataclass

import pytest

from quicksettings.utils import instantiate_dataclass


@dataclass
class LineItem:
    name: str
    description: str
    price: float
    number: int
    cas_number: str | None


@dataclass
class Invoice:
    number: str
    date: date
    line_items: list[LineItem]


raw_data = {
    "number": "001",
    "date": "2021-01-01",
    "line_items": [
        {
            "name": "item1",
            "description": "item1 description",
            "price": 10.0,
            "number": 1,
        },
        {
            "name": "item2",
            "description": "item2 description",
            "price": "20.0",
            "number": "2",
        },
    ],
}


def test_instantiate_dataclass() -> None:
    invoice = instantiate_dataclass(Invoice, raw_data)
    assert invoice.number == "001"
    assert invoice.date == date(2021, 1, 1)
    assert invoice.line_items[0].name == "item1"
    assert invoice.line_items[0].description == "item1 description"
    assert invoice.line_items[0].price == 10.0
    assert invoice.line_items[0].number == 1
    assert invoice.line_items[0].cas_number is None
    assert invoice.line_items[1].name == "item2"
    assert invoice.line_items[1].description == "item2 description"
    assert invoice.line_items[1].price == 20.0
    assert invoice.line_items[1].number == 2
    assert all(isinstance(item, LineItem) for item in invoice.line_items)


@dataclass
class Location:
    lat: float
    long: float


@dataclass
class Host:
    ip_addresses: list[str]
    nodes: list[Location]


@dataclass
class ServerFarm:
    name: str
    hosts: list[Host]


def test_mixed_dataclasses() -> None:
    server_farm = instantiate_dataclass(
        ServerFarm,
        data={
            "name": "farm1",
            "hosts": [
                {
                    "ip_addresses": ["192.168.0.1", "127.0.0.1"],
                    "nodes": [{"lat": 0.0, "long": 0.0}, {"lat": 1.0, "long": 1.0}],
                }
            ],
        },
    )
    assert server_farm.name == "farm1"
    assert server_farm.hosts[0].ip_addresses == ["192.168.0.1", "127.0.0.1"]
    assert server_farm.hosts[0].nodes[0].lat == 0.0
    assert server_farm.hosts[0].nodes[0].long == 0.0


def test_missing_dataclass_fields_raises() -> None:
    with pytest.raises(ValueError):
        instantiate_dataclass(
            Invoice,
            data={
                "number": "001",
                "date": "2021-01-01",
                "line_items": [
                    {
                        "name": "item1",
                        "description": "item1 description",
                        "number": 1,
                    },
                    {
                        "name": "item2",
                        "description": "item2 description",
                        "number": "2",
                    },
                ],
            },
        )

    with pytest.raises(ValueError):
        instantiate_dataclass(
            Invoice,
            data={
                "number": "001",
                "date": "2021-01-01",
            },
        )
