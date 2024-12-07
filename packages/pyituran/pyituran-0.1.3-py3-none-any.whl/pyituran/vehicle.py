"""Class representing an Ituran vehicle."""

from datetime import datetime
import logging
from typing import Tuple
import xml.etree.ElementTree as ElementTree

from pyituran.const import (
    XML_VEHICLE_BATTERY_VOLTAGE,
    XML_VEHICLE_MODEL,
    XML_VEHICLE_MAKE,
    XML_VEHICLE_PLATE,
    XML_VEHICLE_LATITUTE,
    XML_VEHICLE_LONGITUDE,
    XML_VEHICLE_ADDRESS,
    XML_VEHICLE_SPEED,
    XML_VEHICLE_HEADING,
    XML_VEHICLE_LAST_MILEAGE,
    XML_VEHICLE_UPDATE_DATE,
)


logger = logging.getLogger(__package__)


class Vehicle:
    def __init__(self, xml: ElementTree.Element) -> None:
        self.__make: str = self.__xml_get_field(xml, XML_VEHICLE_MAKE)
        self.__model: str = self.__xml_get_field(xml, XML_VEHICLE_MODEL)
        self.__license_plate: str = self.__xml_get_field(
            xml, XML_VEHICLE_PLATE
        )
        self.__latitue: float = float(
            self.__xml_get_field(xml, XML_VEHICLE_LATITUTE)
        )
        self.__longitude: float = float(
            self.__xml_get_field(xml, XML_VEHICLE_LONGITUDE)
        )
        self.__address: str = self.__xml_get_field(xml, XML_VEHICLE_ADDRESS)
        self.__speed: int = int(self.__xml_get_field(xml, XML_VEHICLE_SPEED))
        self.__heading: int = int(
            self.__xml_get_field(xml, XML_VEHICLE_HEADING)
        )
        self.__mileage: float = float(
            self.__xml_get_field(xml, XML_VEHICLE_LAST_MILEAGE)
        )
        self.__battery_voltage: float = float(
            self.__xml_get_field(xml, XML_VEHICLE_BATTERY_VOLTAGE)
        )
        self.__last_update: datetime = datetime.fromisoformat(
            self.__xml_get_field(xml, XML_VEHICLE_UPDATE_DATE)
        )

    @property
    def make(self) -> str:
        return self.__make

    @property
    def model(self) -> str:
        return self.__model

    @property
    def license_plate(self) -> str:
        return self.__license_plate

    @property
    def gps_coordinates(self) -> Tuple[float, float]:
        return (self.__latitue, self.__longitude)

    @property
    def address(self) -> str:
        return self.__address

    @property
    def heading(self) -> int:
        return self.__heading

    @property
    def speed(self) -> int:
        return self.__speed

    @property
    def mileage(self) -> float:
        return self.__mileage

    @property
    def battery_voltage(self) -> float:
        return self.__battery_voltage

    @property
    def last_update(self) -> datetime:
        return self.__last_update

    def __str__(self) -> str:
        return f"{self.make} {self.model} @ {self.gps_coordinates}"

    def __xml_get_field(self, xml: ElementTree.Element, path: str) -> str:
        element = xml.find(path)
        assert element is not None
        text = element.text
        assert text is not None
        return text
