from typing import List, Dict, Union, Optional
from decimal import Decimal
from .types import ConversionResult, ValidationResult
from .errors import InvalidUnitError, ConversionError, CategoryError
from .utils import calculate_similarity, round_decimal
from .constants import (
    LENGTH_UNITS,
    WEIGHT_UNITS,
    VOLUME_UNITS,
    AREA_UNITS,
    TEMPERATURE_UNITS,
    COMMON_UNITS,
    UNIT_CATEGORIES,
    UNIT_FORMATS
)


class MeasurementConverter:
    """Main class for handling unit conversions."""

    unit_factors = {
        'length': LENGTH_UNITS,
        'weight': WEIGHT_UNITS,
        'volume': VOLUME_UNITS,
        'area': AREA_UNITS
    }

    @classmethod
    def convert(
            cls,
            value: float,
            from_unit: str,
            to_unit: str,
            precision: int = 4
    ) -> ConversionResult:
        """
        Convert a value from one unit to another.

        Args:
            value: The value to convert
            from_unit: The unit to convert from
            to_unit: The unit to convert to
            precision: Number of decimal places for the result

        Returns:
            ConversionResult object containing conversion details

        Raises:
            InvalidUnitError: If either unit is invalid
            ConversionError: If conversion fails
        """
        try:
            # Handle temperature conversion separately
            if cls._is_temperature_unit(from_unit) or cls._is_temperature_unit(to_unit):
                return cls._convert_temperature(value, from_unit, to_unit, precision)

            # Get category and validate units
            category = cls._get_unit_category(from_unit)
            if not category:
                raise InvalidUnitError(f"Unsupported unit: {from_unit}")

            # Get conversion factors
            factors = cls.unit_factors.get(category)
            if not factors:
                raise InvalidUnitError(f"No conversion factors for category: {category}")

            # Normalize units to lowercase
            from_unit_lower = from_unit.lower()
            to_unit_lower = to_unit.lower()

            # Validate both units exist in the category
            if from_unit_lower not in factors or to_unit_lower not in factors:
                raise InvalidUnitError("Invalid unit combination")

            # Get conversion factors
            from_factor = factors[from_unit_lower]
            to_factor = factors[to_unit_lower]

            # Perform conversion
            base_value = value * from_factor
            result = base_value / to_factor

            # Round result
            rounded_result = round_decimal(result, precision)

            return ConversionResult(
                from_value=value,
                from_unit=from_unit,
                to_value=rounded_result,
                to_unit=to_unit,
                formula=f"({value} {from_unit}) * ({from_factor}) / ({to_factor})",
                precision=precision
            )

        except KeyError as e:
            raise InvalidUnitError(f"Invalid unit: {str(e)}")
        except Exception as e:
            raise ConversionError(f"Conversion failed: {str(e)}")

    @classmethod
    def batch_convert(
            cls,
            conversions: List[Dict[str, Union[float, str]]],
            global_precision: int = 4
    ) -> List[ConversionResult]:
        """
        Convert multiple values at once.

        Args:
            conversions: List of conversion requests
            global_precision: Default precision for all conversions

        Returns:
            List of ConversionResult objects
        """
        results = []
        for conv in conversions:
            precision = conv.get('precision', global_precision)
            result = cls.convert(
                value=conv['value'],
                from_unit=conv['from_unit'],
                to_unit=conv['to_unit'],
                precision=precision
            )
            results.append(result)
        return results

    @classmethod
    def validate_unit(cls, unit: str) -> ValidationResult:
        """
        Validate a unit and provide suggestions if invalid.

        Args:
            unit: Unit to validate

        Returns:
            ValidationResult object containing validation details
        """
        if cls._is_temperature_unit(unit):
            return ValidationResult(is_valid=True)

        category = cls._get_unit_category(unit)
        if not category:
            suggestions = cls._find_similar_units(unit)
            return ValidationResult(
                is_valid=False,
                errors=[f"Unknown unit: {unit}"],
                suggestions=suggestions if suggestions else None
            )
        return ValidationResult(is_valid=True)

    @classmethod
    def get_supported_categories(cls) -> List[str]:
        """
        Get all supported measurement categories.

        Returns:
            List of category names
        """
        return UNIT_CATEGORIES

    @classmethod
    def get_available_units(cls, category: Optional[str] = None) -> List[str]:
        """
        Get available units for a category or all units.

        Args:
            category: Optional category name

        Returns:
            List of unit symbols
        """
        if category:
            if category not in UNIT_CATEGORIES:
                raise CategoryError(f"Invalid category: {category}")
            return UNIT_FORMATS[category]

        all_units = []
        for cat in UNIT_CATEGORIES:
            all_units.extend(UNIT_FORMATS[cat])
        return all_units

    @classmethod
    def get_common_units(cls, category: str) -> List[str]:
        """
        Get commonly used units for a category.

        Args:
            category: Category name

        Returns:
            List of common unit symbols
        """
        return COMMON_UNITS.get(category, [])

    @staticmethod
    def format_result(
            result: ConversionResult,
            format_type: str = 'short'
    ) -> str:
        """
        Format a conversion result as a string.

        Args:
            result: ConversionResult to format
            format_type: 'short' or 'long' format

        Returns:
            Formatted string
        """
        if format_type == 'long':
            return (
                f"{result.from_value} {result.from_unit} "
                f"is equal to {result.to_value} {result.to_unit}"
            )
        return f"{result.from_value} {result.from_unit} = {result.to_value} {result.to_unit}"

    @staticmethod
    def _is_temperature_unit(unit: str) -> bool:
        """Check if a unit is a temperature unit."""
        return unit.upper() in ['C', 'F', 'K']

    @classmethod
    def _convert_temperature(
            cls,
            value: float,
            from_unit: str,
            to_unit: str,
            precision: int
    ) -> ConversionResult:
        """Handle temperature conversion."""
        from_unit = from_unit.upper()
        to_unit = to_unit.upper()

        if from_unit not in TEMPERATURE_UNITS or to_unit not in TEMPERATURE_UNITS:
            raise InvalidUnitError("Invalid temperature unit")

        try:
            conversion_func = TEMPERATURE_UNITS[from_unit][to_unit]
            result = conversion_func(value)
            rounded_result = round_decimal(result, precision)

            formula = (
                "Direct conversion" if from_unit == to_unit else
                f"Temperature conversion from {from_unit} to {to_unit}"
            )

            return ConversionResult(
                from_value=value,
                from_unit=from_unit,
                to_value=rounded_result,
                to_unit=to_unit,
                formula=formula,
                precision=precision
            )
        except Exception as e:
            raise ConversionError(f"Temperature conversion failed: {str(e)}")

    @classmethod
    def _get_unit_category(cls, unit: str) -> Optional[str]:
        """Get the category for a unit."""
        unit_lower = unit.lower()
        for category, factors in cls.unit_factors.items():
            if unit_lower in factors:
                return category
        return None

    @classmethod
    def _find_similar_units(cls, unit: str, max_suggestions: int = 3) -> List[str]:
        """Find similar units for suggestions."""
        all_units = cls.get_available_units()
        similarities = [
            (u, calculate_similarity(unit, u))
            for u in all_units
        ]
        sorted_units = sorted(similarities, key=lambda x: x[1], reverse=True)
        return [u for u, _ in sorted_units[:max_suggestions]]