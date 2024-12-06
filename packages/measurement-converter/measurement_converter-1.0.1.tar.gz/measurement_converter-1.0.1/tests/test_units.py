import pytest
from measurement_converter import MeasurementConverter

def test_get_available_units():
    length_units = MeasurementConverter.get_available_units('length')
    assert 'm' in length_units
    assert 'km' in length_units

def test_get_common_units():
    common_length = MeasurementConverter.get_common_units('length')
    assert 'm' in common_length
    assert 'km' in common_length

def test_get_supported_categories():
    categories = MeasurementConverter.get_supported_categories()
    assert 'length' in categories
    assert 'weight' in categories
    assert 'temperature' in categories