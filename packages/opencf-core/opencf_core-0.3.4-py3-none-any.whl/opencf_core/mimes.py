"""
MIME Type Guesser Module

This module provides a singleton class for guessing MIME types from file paths using the python-magic library.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

try:
    import magic  # pip install python-magic

    MIME_GUESSER: Optional[magic.Magic] = magic.Magic(mime=True)
except ImportError:
    MIME_GUESSER = None


def guess_mime_type_from_file(file_path: Union[str, Path]) -> str:
    """
    Guesses the MIME type from the file path.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The guessed MIME type.
    """
    if MIME_GUESSER is None:
        raise ImportError(
            "magic module is not imported. Please install it with 'pip install python-magic'"
        )

    file_path = Path(file_path)
    assert file_path.exists()

    return MIME_GUESSER.from_file(str(file_path))
