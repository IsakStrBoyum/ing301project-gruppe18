import abc
from typing import Optional
from pydantic import BaseModel

from device import Device


class SensorMeasurement(BaseModel):

    value: str


class Sensor(Device):

    def is_sensor(self):
        return True

    def is_actuator(self):
        return False

    @abc.abstractmethod
    def get_current_value(self):
        pass

    @abc.abstractmethod
    def set_current_value(self, value: float):
        pass

    @abc.abstractmethod
    def get_current_values(self):
        pass

    @abc.abstractmethod
    def delete_oldest_value(self):
        pass

    @abc.abstractmethod
    def get_unit(self):
        pass


class TemperatureSensor(Sensor):

    temperature: list[float] | None = list()
    unit: str | None = "°C"

    def get_current_value(self) -> Optional[float]:
        return self.temperature[0]

    def get_current_values(self):
        return self.temperature

    def set_current_value(self, temperature: float):
        self.temperature.insert(0, temperature)

    def delete_oldest_value(self):
        self.temperature.pop()

    def get_unit(self):
        return self.unit

class HumiditySensor(Sensor):

    humidity: list[float] | None = list()
    unit: str | None = "%"

    def get_current_value(self) -> Optional[float]:
        return self.humidity[0]

    def get_current_values(self):
        return self.humidity

    def set_current_value(self, humidity: float):
        self.humidity.insert(0, humidity)

    def delete_oldest_value(self):
        self.humidity.pop()

    def get_unit(self):
        return self.unit


class SmartMeter(Sensor):

    energy_consumption: list[float] | None = list()
    unit: str | None = "kWh"

    def get_current_value(self) -> Optional[float]:
        return self.energy_consumption[0]

    def get_current_values(self):
        return self.energy_consumption

    def set_current_value(self, energy_consumption: float):
        self.energy_consumption.insert(0, energy_consumption)

    def delete_oldest_value(self):
        self.energy_consumption.pop()

    def get_unit(self):
        return self.unit

class AirQualitySensor(Sensor):

    air_quality: list[float] | None = list()
    unit: str | None = "g/m^2"

    def get_current_value(self) -> Optional[float]:
        return self.air_quality[0]

    def get_current_values(self):
        return self.air_quality

    def set_current_value(self, air_quality: float):
        self.air_quality.insert(0, air_quality)

    def delete_oldest_value(self):
        self.air_quality.pop()

    def get_unit(self):
        return self.unit
        