from typing import Dict, Callable

# Length units (base: meters)
LENGTH_UNITS: Dict[str, float] = {
    'm': 1,
    'km': 1000,
    'cm': 0.01,
    'mm': 0.001,
    'mile': 1609.344,
    'yard': 0.9144,
    'foot': 0.3048,
    'inch': 0.0254,
    'nm': 1852,  # nautical mile
    'μm': 0.000001,
    'pm': 1e-12
}

# Weight units (base: kilograms)
WEIGHT_UNITS: Dict[str, float] = {
    'kg': 1,
    'g': 0.001,
    'mg': 0.000001,
    'lb': 0.45359237,
    'oz': 0.028349523125,
    'ton': 1000,
    'stone': 6.35029318,
    'grain': 0.00006479891
}

# Volume units (base: liters)
VOLUME_UNITS: Dict[str, float] = {
    'l': 1,
    'ml': 0.001,
    'gal': 3.78541,
    'qt': 0.946353,
    'cup': 0.236588,
    'floz': 0.0295735,
    'tbsp': 0.0147868,
    'tsp': 0.00492892
}

# Area units (base: square meters)
AREA_UNITS: Dict[str, float] = {
    'm2': 1,
    'km2': 1_000_000,
    'cm2': 0.0001,
    'mm2': 0.000001,
    'ha': 10_000,
    'acre': 4046.86,
    'sqft': 0.092903,
    'sqin': 0.00064516
}

# Temperature conversion functions
def c_to_f(c: float) -> float:
    return c * 9/5 + 32

def f_to_c(f: float) -> float:
    return (f - 32) * 5/9

def k_to_c(k: float) -> float:
    return k - 273.15

def c_to_k(c: float) -> float:
    return c + 273.15

TEMPERATURE_UNITS: Dict[str, Dict[str, Callable]] = {
    'C': {'F': c_to_f, 'K': c_to_k, 'C': lambda x: x},
    'F': {'C': f_to_c, 'K': lambda f: c_to_k(f_to_c(f)), 'F': lambda x: x},
    'K': {'C': k_to_c, 'F': lambda k: c_to_f(k_to_c(k)), 'K': lambda x: x}
}

# Common units for quick access
COMMON_UNITS = {
    'length': ['m', 'km', 'cm', 'mm', 'mile', 'foot', 'inch'],
    'weight': ['kg', 'g', 'lb', 'oz'],
    'volume': ['l', 'ml', 'gal', 'cup'],
    'temperature': ['C', 'F', 'K'],
    'area': ['m2', 'km2', 'ha', 'acre']
}

# All unit categories
UNIT_CATEGORIES = [
    'length',
    'weight',
    'volume',
    'temperature',
    'area'
]

# Unit validation templates
UNIT_FORMATS = {
    'temperature': ['C', 'F', 'K'],
    'length': list(LENGTH_UNITS.keys()),
    'weight': list(WEIGHT_UNITS.keys()),
    'volume': list(VOLUME_UNITS.keys()),
    'area': list(AREA_UNITS.keys())
}