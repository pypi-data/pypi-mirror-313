class MeasurementError(Exception):
    """Base class for measurement converter exceptions."""
    pass

class InvalidUnitError(MeasurementError):
    """Raised when an invalid unit is provided."""
    pass

class ConversionError(MeasurementError):
    """Raised when conversion fails."""
    pass

class CategoryError(MeasurementError):
    """Raised when an invalid category is provided."""
    pass