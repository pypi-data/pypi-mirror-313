from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from decimal import Decimal

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

UnitType = str
CategoryType = str
ConversionFactors = Dict[str, float]
TemperatureConversion = Dict[str, Dict[str, Any]]