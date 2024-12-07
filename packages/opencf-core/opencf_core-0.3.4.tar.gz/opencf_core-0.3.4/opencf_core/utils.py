import glob
from collections.abc import Iterable
from pathlib import Path
from typing import List


def is_iterable(obj):
    return isinstance(obj, Iterable)


def ensure_iterable(obj, raise_err=True, return_single=False):
    if isinstance(obj, Iterable):
        return obj
    if raise_err:
        raise TypeError(f"{obj} is not iterable")
    if return_single:
        return (obj,)
    return tuple()


def get_filepaths_from_inputs(args: List[str]) -> List[str]:
    """
    Generate a list of file paths from a list of command-line arguments.

    Args:
        args (list of str): List of command-line arguments including file paths, directory paths, and glob patterns.

    Returns:
        list of str: List of file paths that match the input criteria.
    """
    filepaths: List[str] = []

    for arg in args:
        path = Path(arg)
        # If arg is a directory, add all files within the directory
        if path.is_dir():
            filepaths.extend(sorted([str(p) for p in path.rglob("*") if p.is_file()]))
        # If arg is a file, add the file path
        elif path.is_file():
            filepaths.append(str(path))
        # If arg is a glob pattern, add all matching file paths
        else:
            filepaths.extend(sorted(glob.glob(str(path))))

    return filepaths


def test():
    # Example usage:
    print(is_iterable([1, 2, 3]))  # Output: True
    print(is_iterable("hello"))  # Output: True
    print(is_iterable(123))  # Output: False
