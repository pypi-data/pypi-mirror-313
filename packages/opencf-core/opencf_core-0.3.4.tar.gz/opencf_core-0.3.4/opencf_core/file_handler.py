"""
Resolved Input File Module

This module provides the ResolvedInputFile class, which manages file paths and types, resolving them as needed.
It supports resolving file types based on paths, optional content reading, and handling both files and directories.

Classes:
- ResolvedInputFile: Manages file paths and types, resolving them as needed.

Exceptions:
- ValueError: Raised when file paths or types are incompatible or unsupported.
"""

from pathlib import Path
from typing import Optional, Type, Union

from .enum import Enum
from .filetypes import EmptySuffixError, FileType
from .logging_config import logger


class ResolvedInputFile:
    """
    Handles resolving the file type of a given file or folder, managing path adjustments and optional content reading.
    """

    def __init__(
        self,
        path: Union[str, Path],
        is_dir: Optional[bool] = None,
        should_exist: bool = True,
        file_type: Optional[str] = None,
        add_suffix: bool = False,
        read_content: bool = False,
        filetype_class: Optional[Type[FileType]] = FileType,
    ):
        """
        Initializes an instance of ResolvedInputFile with options for type resolution and path modification.

        Args:
            path (str): The path to the file or folder.
            is_dir (bool, optional): Specifies if the path is a directory. If None, inferred using pathlib. Defaults to None.
            should_exist (bool, optional): Specifies if the existence of the path is required. Defaults to True.
            file_type (str, optional): The explicit type of the file. If None, attempts to resolve to a filetype object based on the path or content.
            add_suffix (bool, optional): Whether to append the resolved file type's suffix to the file path. Defaults to False.
            read_content (bool, optional): Whether to read the file's content to assist in type resolution. Defaults to False.
        """
        # Convert path to Path object
        self.path = Path(path)

        # Parse boolean args
        add_suffix = bool(add_suffix)
        read_content = bool(read_content)
        should_exist = bool(should_exist)

        if filetype_class is None:
            filetype_class = FileType
        assert issubclass(filetype_class, Enum)
        self.filetype_class = filetype_class

        self._check_existence(should_exist)

        # Infer if the path is a directory
        if is_dir is None and add_suffix is False:
            is_dir = self._resolve_path_type(file_type=file_type)

        # Resolve the file type
        if is_dir:
            assert file_type, "file_type must be set when is_dir is activated"
            self.file_type, self.suffix = self._resolve_directory_type(file_type)
            self.is_dir = True
        else:
            logger.debug("file_type set by user = %s", file_type)
            self.file_type, self.suffix = self._resolve_file_type(
                file_type, read_content, add_suffix
            )
            self.is_dir = False

    def _resolve_path_type(self, file_type: Optional[str] = None) -> bool:
        """
        Determines if the provided path refers to a directory or a file, based on its existence, suffix, and file_type.

        Args:
            file_type (str, optional): The type of file expected at the path. Influences directory creation and type resolution.

        Returns:
            bool: True if the path is determined to be a directory, False if it is a file.
        """
        is_filesuffix_set = self.path.suffix != ""
        is_filetype_set = file_type is not None

        if self.path.exists():
            # Check if the existing path is a directory
            is_dir = self.path.is_dir()
            logger.debug("Path %s exists. Setting is_dir to %s.", self.path, is_dir)
        elif is_filesuffix_set:
            # If a suffix is present, assume it's a file
            is_dir = False
            logger.debug("Suffix found. Assuming file. Setting is_dir to False.")
        elif is_filetype_set:
            # If there's no suffix and a file_type is specified, assume it's a directory and create it
            self.path.mkdir(parents=False, exist_ok=True)
            is_dir = True
            logger.debug(
                "No suffix found and file_type is specified. Assuming directory and creating it. Setting is_dir to True."
            )
        else:
            # If the method cannot determine whether the path is for a file or directory, raise an error
            raise ValueError(
                f"Failed to resolve if the path '{self.path}' is a directory or a file. Ensure correct path and file_type are provided."
            )

        return is_dir

    def _check_existence(self, should_exist: bool):
        if should_exist and not self.path.exists():
            raise ValueError(
                f"The specified file or folder '{self.path}' does not exist, but existence is required."
            )

        if not should_exist and self.path.exists():
            logger.warning(
                "The specified file or folder '%s' already exist, but existence is not required.",
                self.path,
            )

    def _resolve_directory_type(self, file_type: str):
        """
        Handles the case when the specified path is a directory.
        """
        if self.path.is_file():
            raise ValueError(
                f"The specified path '{self.path}' is a file, not a directory."
            )
        # Create directory if it doesn't exist
        self.path.mkdir(exist_ok=True)
        resolved_file_type, _ = self.filetype_class.from_suffix(
            file_type, raise_err=True
        )
        assert resolved_file_type.is_true_filetype()
        suffix = resolved_file_type.get_one_suffix()
        return resolved_file_type, suffix

    def _resolve_file_type(
        self, file_type: Optional[str], read_content: bool, add_suffix: bool
    ):
        """
        Resolves the file type based on given parameters.

        Args:
            file_type (FileType or str, optional): An explicit file type or extension.
            read_content (bool): Indicates if file content should be used to help resolve the file type.
            add_suffix (bool): Whether to append the resolved file type's suffix to the file path.
        """
        resolved_file_type = self.__resolve_filetype__(
            file_type, self.path, read_content
        )
        logger.debug("resolved_file_type %s", resolved_file_type)
        assert (
            resolved_file_type.is_true_filetype()
        ), f"unable to resolve filetype for path={self.path.name} file_type={file_type},read_content={read_content}"

        # Get the suffix corresponding to the resolved file type
        suffix = resolved_file_type.get_one_suffix()

        # Optionally add suffix to the file path
        if add_suffix:
            self.path = self.path.with_suffix(suffix)

        return resolved_file_type, suffix

    def __resolve_filetype__(
        self, file_type: Optional[str], file_path: Path, read_content: bool
    ) -> FileType:
        """
        Determines the file type, utilizing the provided type, file path, or content as needed.

        Args:
            file_type (FileType or str, optional): An explicit file type or extension.
            file_path (str): The path to the file, used if file_type is not provided.
            read_content (bool): Indicates if file content should be used to help resolve the file type.

        Returns:
            FileType: The resolved file type.
        """
        if not file_type:
            try:
                return self.filetype_class.from_path(
                    file_path, read_content=read_content, raise_err=True
                )[0]
            except EmptySuffixError as exc:
                raise ValueError(
                    "filepath suffix is emtpy but file_type not set"
                ) from exc

        resolved_file_type, _ = self.filetype_class.from_suffix(
            file_type, raise_err=True
        )

        file_type_from_path, _ = self.filetype_class.from_path(
            file_path, read_content=read_content, raise_err=False
        )

        if file_type_from_path.is_true_filetype():
            assert file_type_from_path == resolved_file_type

        return resolved_file_type

    def __str__(self):
        """
        Returns the absolute file path as a string.

        Returns:
            str: The resolved file path.
        """
        return str(Path(self.path).resolve())

    def __repr__(self):
        """
        Returns the absolute file path as a string.

        Returns:
            str: The resolved file path.
        """
        return f"{self.__class__.__name__}: {self.path.name}"
