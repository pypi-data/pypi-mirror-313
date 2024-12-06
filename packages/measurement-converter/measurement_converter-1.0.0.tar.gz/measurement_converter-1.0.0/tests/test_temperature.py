import pytest
from measurement_converter import MeasurementConverter

def test_celsius_to_fahrenheit():
    result = MeasurementConverter.convert(0, 'C', 'F')
    assert result.to_value == 32

def test_fahrenheit_to_celsius():
    result = MeasurementConverter.convert(32, 'F', 'C')
    assert result.to_value == 0

def test_celsius_to_kelvin():
    result = MeasurementConverter.convert(0, 'C', 'K')
    assert result.to_value == 273.15

def test_kelvin_to_celsius():
    result = MeasurementConverter.convert(273.15, 'K', 'C')
    assert result.to_value == 0

def test_temperature_case_insensitive():
    result1 = MeasurementConverter.convert(0, 'c', 'f')
    result2 = MeasurementConverter.convert(0, 'C', 'F')
    assert result1.to_value == result2.to_value