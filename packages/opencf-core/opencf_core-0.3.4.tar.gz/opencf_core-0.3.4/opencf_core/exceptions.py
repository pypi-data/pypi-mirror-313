"""
Classes:

- UnsupportedFileTypeError: Custom exception for handling unsupported file types.
- EmptySuffixError: Specialized exception for cases where a file's suffix does not provide enough information
                    to determine its type.
- MismatchedException: Exception for handling cases where there's a mismatch between expected and actual file attributes.
"""


# Custom Exceptions
class UnsupportedFileTypeError(Exception):
    """Exception raised for handling cases of unsupported file types."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class EmptySuffixError(UnsupportedFileTypeError):
    """Exception raised when a file's suffix does not provide enough information to determine its type."""

    def __init__(self):
        self.message = "Filetype not parsed from empty suffix."
        super().__init__(self.message)


class MismatchedException(Exception):
    """Exception raised for mismatches between expected and actual file attributes."""

    def __init__(self, label, claimed_val, expected_vals):
        super().__init__(
            f"Mismatched {label}: Found '{claimed_val}', Expected one of '{expected_vals}'"
        )
