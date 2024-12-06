# Measurement Converter
![Python Version](https://img.shields.io/pypi/pyversions/measurement_converter)
![PyPI Version](https://img.shields.io/pypi/v/measurement_converter)
![License](https://img.shields.io/pypi/l/measurement_converter)
![Downloads](https://img.shields.io/pypi/dm/measurement_converter)

A powerful Python library for handling various unit conversions with high precision and type safety. Perfect for applications requiring measurement conversions, scientific calculations, and engineering tools.

## 🌟 Key Features

- 📐 **Multiple Measurement Types**: Support for length, weight, volume, temperature, and more
- 🎯 **High Precision Calculations**: Configurable precision for all conversions
- 🔍 **Type Hints**: Full typing support for better development experience
- 🌐 **Locale Support**: Format results according to different locales
- ⚡ **Batch Conversions**: Convert multiple values at once
- 🧮 **Formula Tracking**: See the conversion formulas used
- 🛠️ **Extensible**: Easy to customize and extend

## 📦 Installation

```bash
pip install measurement_converter
```

## 🚀 Quick Start

```python
from measurement_converter import MeasurementConverter
from measurement_converter.types import ConversionResult

# Simple length conversion
result = MeasurementConverter.convert(100, 'km', 'm')
print(f"Result: {MeasurementConverter.format_result(result)}")
# Output: Result: 100 km = 100000 m

# Temperature conversion
temp = MeasurementConverter.convert(32, 'F', 'C')
print(f"Temperature: {MeasurementConverter.format_result(temp)}")
# Output: Temperature: 32 F = 0 C
```

## 💡 Advanced Usage

### 🔄 Batch Conversion

```python
# Convert multiple values at once
conversions = [
    {'value': 1, 'from_unit': 'km', 'to_unit': 'm'},
    {'value': 2.5, 'from_unit': 'kg', 'to_unit': 'lb'},
    {'value': 30, 'from_unit': 'C', 'to_unit': 'F'}
]

results = MeasurementConverter.batch_convert(conversions)
for result in results:
    print(MeasurementConverter.format_result(result))
```

### 🔍 Unit Validation

```python
# Validate units with suggestions
validation = MeasurementConverter.validate_unit('kmh')
if not validation.is_valid:
    print(f"Did you mean: {', '.join(validation.suggestions)}?")
```

### 🌐 Formatting Options

```python
# Format results with different options
result = MeasurementConverter.convert(1, 'km', 'm')
formatted = MeasurementConverter.format_result(result, format_type='long')
print(formatted)
# Output: 1 kilometre is equal to 1000 metres
```

## 📋 Supported Units

### Length
- Meters (m)
- Kilometers (km)
- Centimeters (cm)
- Millimeters (mm)
- Miles (mile)
- Yards (yard)
- Feet (foot)
- Inches (inch)
- Nautical Miles (nm)
- Micrometers (μm)
- Picometers (pm)

### Weight
- Kilograms (kg)
- Grams (g)
- Milligrams (mg)
- Pounds (lb)
- Ounces (oz)
- Tons (ton)
- Stones (stone)
- Grains (grain)

### Volume
- Liters (l)
- Milliliters (ml)
- Gallons (gal)
- Quarts (qt)
- Cups (cup)
- Fluid Ounces (floz)
- Tablespoons (tbsp)
- Teaspoons (tsp)

### Temperature
- Celsius (C)
- Fahrenheit (F)
- Kelvin (K)

### Area
- Square Meters (m2)
- Square Kilometers (km2)
- Hectares (ha)
- Acres (acre)
- Square Feet (sqft)
- Square Inches (sqin)

## 📋 Type Definitions

```python
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class ConversionResult:
    from_value: float
    from_unit: str
    to_value: float
    to_unit: str
    formula: str
    precision: int

@dataclass
class ValidationResult:
    is_valid: bool
    errors: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None
```

## 🔍 Error Handling

```python
from measurement_converter import MeasurementConverter
from measurement_converter.errors import InvalidUnitError, ConversionError

try:
    result = MeasurementConverter.convert(100, 'invalid', 'm')
except InvalidUnitError as e:
    print(f"Invalid unit: {e}")
except ConversionError as e:
    print(f"Conversion error: {e}")
```

## 🚀 Best Practices

1. Always validate units before conversion
2. Use proper unit symbols from the supported units list
3. Handle errors appropriately
4. Consider precision requirements for your specific use case
5. Use batch conversions for multiple operations
6. Cache common conversion results if needed

## 🛠️ Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=measurement_converter

# Run type checking
mypy src/measurement_converter
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
