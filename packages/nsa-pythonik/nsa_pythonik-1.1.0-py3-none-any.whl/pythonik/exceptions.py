class PythonikException(Exception):
    """Base class for exceptions for Pythonik."""


class UnexpectedStorageMethodForProxy(PythonikException):
    """Raised when an unexpected storage method is called for a proxy."""
    pass
