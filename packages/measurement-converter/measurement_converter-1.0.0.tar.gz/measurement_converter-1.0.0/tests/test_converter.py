import pytest
from measurement_converter import MeasurementConverter, InvalidUnitError, ConversionError

def test_length_conversion():
    result = MeasurementConverter.convert(1, 'km', 'm')
    assert result.to_value == 1000
    assert result.from_unit == 'km'
    assert result.to_unit == 'm'

def test_weight_conversion():
    result = MeasurementConverter.convert(1, 'kg', 'g')
    assert result.to_value == 1000
    assert result.from_unit == 'kg'
    assert result.to_unit == 'g'

def test_temperature_conversion():
    result = MeasurementConverter.convert(32, 'F', 'C')
    assert result.to_value == 0
    assert result.from_unit == 'F'
    assert result.to_unit == 'C'

def test_invalid_unit():
    with pytest.raises(InvalidUnitError):
        MeasurementConverter.convert(1, 'invalid', 'm')

def test_batch_conversion():
    conversions = [
        {'value': 1, 'from_unit': 'km', 'to_unit': 'm'},
        {'value': 1, 'from_unit': 'kg', 'to_unit': 'g'}
    ]
    results = MeasurementConverter.batch_convert(conversions)
    assert len(results) == 2
    assert results[0].to_value == 1000
    assert results[1].to_value == 1000

def test_precision():
    result = MeasurementConverter.convert(1, 'km', 'm', precision=2)
    assert result.precision == 2
    assert len(str(result.to_value).split('.')[-1]) <= 2

def test_validation():
    valid = MeasurementConverter.validate_unit('km')
    invalid = MeasurementConverter.validate_unit('invalid')
    assert valid.is_valid
    assert not invalid.is_valid
    assert invalid.suggestions is not None

def test_format_result():
    result = MeasurementConverter.convert(1, 'km', 'm')
    short_format = MeasurementConverter.format_result(result)
    long_format = MeasurementConverter.format_result(result, 'long')
    assert '=' in short_format
    assert 'is equal to' in long_format