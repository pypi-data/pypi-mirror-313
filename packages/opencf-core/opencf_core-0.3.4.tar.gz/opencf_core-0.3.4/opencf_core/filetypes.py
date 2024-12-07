"""
File Type Definitions Module

This module provides a comprehensive framework for handling various file types within a file conversion context.
It defines classes and enumerations for identifying, validating, and working with different file types, based on
file extensions, MIME types, and optionally, file content. It also includes custom exceptions for handling common
errors related to file type processing.

Classes:

- FileType: Enum class that encapsulates various file types supported by the system, providing methods for
                type determination from file attributes.

Dependencies:

- collections.namedtuple: For defining simple classes for storing MIME type information.
- pathlib.Path: For file path manipulations and checks.
- opencf_core.mimes.guess_mime_type_from_file: Utility function to guess MIME type from a file path.

Usage Examples:

```python
from pathlib import Path
from mymodule import FileType, EmptySuffixError, UnsupportedFileTypeError

# Example: Determine file type from suffix
try:
    file_type, _ = FileType.from_suffix('.txt')
    print(f'File type: {file_type.name}')
except (EmptySuffixError, UnsupportedFileTypeError) as e:
    print(f'Error: {e}')

# Example: Determine file type from MIME type
try:
    file_path = Path('/path/to/file.txt')
    file_type, _ = FileType.from_mimetype(file_path)
    print(f'File type: {file_type.name}')
except FileNotFoundError as e:
    print(f'Error: {e}')
except UnsupportedFileTypeError as e:
    print(f'Error: {e}')

# Example: Validate file type by path and content
file_path = Path('/path/to/file.txt')
is_valid = FileType.TEXT.is_valid_path(file_path, read_content=True)
print(f'Is valid: {is_valid}')
```
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Set, Tuple, Type, Union

from .enum import Enum, extend_enum_with_methods
from .exceptions import EmptySuffixError, MismatchedException, UnsupportedFileTypeError
from .mimes import guess_mime_type_from_file


@dataclass(eq=False, frozen=True)
class MimeType:
    """Class representing MIME type information.

    Attributes:
        extensions (Tuple[str, ...]): Tuple of file extensions associated with the MIME type.
        mime_types (Tuple[str, ...]): Tuple of MIME types.
        upper_mime_types (Tuple[str, ...]): Tuple of additional MIME types that can be considered equivalent.
    """

    extensions: Tuple[str, ...] = ()
    mime_types: Tuple[str, ...] = ()
    upper_mime_types: Tuple[str, ...] = ()
    children_mime_types: Tuple[MimeType, ...] = ()


def merge_mimetype(*mimetypes: MimeType) -> MimeType:
    """Merge multiple MimeType objects into one."""
    extensions = sum((m.extensions for m in mimetypes), ())
    mime_types = sum((m.mime_types for m in mimetypes), ())
    upper_mime_types = sum((m.upper_mime_types for m in mimetypes), ())
    children_mime_types = tuple(mimetypes)
    return MimeType(extensions, mime_types, upper_mime_types, children_mime_types)


class FileType(Enum):
    """Base enumeration for file types, providing methods for type determination and validation.

    Attributes:
        NOTYPE (MimeType): Represents an undefined file type (no extensions).
        TEXT (MimeType): Represents a text file type (.txt).
        UNHANDLED (MimeType): Represents an unhandled file type (no extensions).
        CSV (MimeType): Represents a CSV file type (.csv).
        MARKDOWN (MimeType): Represents a Markdown file type (.md).
        EXCEL (MimeType): Represents an Excel file type (.xls, .xlsx).
        MSWORD (MimeType): Represents a Microsoft Word file type (.doc, .docx).
        JSON (MimeType): Represents a JSON file type (.json).
        PDF (MimeType): Represents a PDF file type (.pdf).
        IMAGE (MimeType): Represents an image file type (.jpg, .jpeg, .png).
        GIF (MimeType): Represents a GIF file type (.gif).
        VIDEO (MimeType): Represents a video file type (.mp4, .avi).
        XML (MimeType): Represents a xml file type (.xml).
    """

    # required members
    NOTYPE: MimeType = MimeType()
    TEXT = MimeType(("txt",), ("text/plain",))
    UNHANDLED: MimeType = MimeType()

    # raster images
    PNG = MimeType(("png",), ("image/png",))
    JPEG = MimeType(("jpeg", "jpg"), ("image/jpeg",))
    TIFF = MimeType(("tiff",), ("image/tiff",))
    IMG_RASTER = merge_mimetype(PNG, JPEG, TIFF)

    # animated images
    GIF = MimeType(("gif",), ("image/gif",))
    APNG = MimeType(("apng",), ("image/apng",))
    WEBP = MimeType(("webp",), ("image/webp",))
    IMG_ANIM = merge_mimetype(GIF, APNG, WEBP)

    # vectoriel images
    SVG = MimeType(("svg",), ("image/svg+xml",))
    EPS = MimeType(("eps",), ("application/postscript",))
    IMG_VEC = merge_mimetype(SVG, EPS)

    # sequence of images
    EXR = MimeType(("exr",), ("image/aces-exr",))
    DPX = MimeType(("dpx",), ("image/dpx",))
    IMG_SEQ = merge_mimetype(EXR, DPX, TIFF)

    # video
    MP4 = MimeType(("mp4",), ("video/mp4",))
    MOV = MimeType(("mov",), ("video/quicktime", "video/wbm"))
    AVI = MimeType(("avi",), ("video/x-msvideo",))
    WMV = MimeType(("wmv",), ("video/x-ms-wmv",))
    VIDEO = merge_mimetype(MP4, MOV, AVI, WMV)

    # text document
    DOCX = MimeType(
        ("docx",),
        ("application/vnd.openxmlformats-officedocument.wordprocessingml.document",),
    )
    ODT = MimeType(("odt",), ("application/vnd.oasis.opendocument.text",))
    DOC = MimeType(("doc",), ("application/msword",))
    MD = MimeType(("md",), ("text/markdown",), ("text/plain",))
    DOC_TEXT = merge_mimetype(DOCX, ODT, DOC, MD)

    # spreadsheet document
    XLSX = MimeType(
        ("xlsx",),
        ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",),
    )
    ODS = MimeType(("ods",), ("application/vnd.oasis.opendocument.spreadsheet",))
    CSV = MimeType(("csv",), ("text/csv",), ("text/plain",))
    XLS = MimeType(("xls",), ("application/vnd.ms-excel",))
    DOC_SPREADSHEET = merge_mimetype(XLSX, ODS, CSV, XLS)

    # presentation documents
    PPTX = MimeType(
        ("pptx",),
        ("application/vnd.openxmlformats-officedocument.presentationml.presentation",),
    )
    ODP = MimeType(("odp",), ("application/vnd.oasis.opendocument.presentation",))
    PPT = MimeType(("ppt",), ("application/vnd.ms-powerpoint",))
    PDF = MimeType(("pdf",), ("application/pdf",))
    DOC_PRESENTATION = merge_mimetype(PPTX, ODP, PPT, PDF)

    # Other formats
    BIN = MimeType(("bin",), ("application/octet-stream",))
    JSON = MimeType(("json",), ("application/json",))
    HTML = MimeType(("html", "htm"), ("text/html",))

    def get_value(self) -> MimeType:
        """Returns the `MimeType` associated with the enumeration member.

        Returns:
            MimeType: The MIME type information.
        """
        return self.value  # type:ignore

    @classmethod
    def get_filetypes(cls):
        """Yields all valid file types in the enumeration."""
        for member in cls:
            if not isinstance(member.get_value(), MimeType):
                continue
            yield member

    @classmethod
    def clean_suffix(cls, suffix: str) -> str:
        return suffix.lower().lstrip(".")

    @classmethod
    def from_suffix(
        cls, suffix: str, raise_err: bool = False, return_matches: bool = False
    ) -> Tuple[FileType, Tuple[FileType, ...]]:
        """Determines a filetype from a file's suffix.

        Args:
            suffix (str): The file suffix (extension).
            raise_err (bool, optional): Whether to raise an exception if the type is unhandled. Defaults to False.
            return_matches (bool, optional): Whether to return a tuple with the first matching filetype and a list of all options. Defaults to False.

        Returns:
            FileType: The determined filetype enumeration member, or a tuple with the first matching filetype and a list of all options.

        Raises:
            EmptySuffixError: If the suffix is empty and raise_err is True.
            UnsupportedFileTypeError: If the file type is unhandled and raise_err is True.
        """
        suffix = cls.clean_suffix(suffix=suffix)
        if not suffix:
            if raise_err:
                raise EmptySuffixError()
            return (cls.NOTYPE, tuple())

        matches = []
        for member in cls.get_filetypes():
            member_value = member.get_value()
            if member_value.extensions and suffix in member_value.extensions:
                if not return_matches:
                    return (member, tuple())
                matches.append(member)

        if len(matches) == 0:
            if raise_err:
                raise UnsupportedFileTypeError(
                    f"Unhandled filetype from suffix={suffix}"
                )
            return (cls.UNHANDLED, tuple())

        return (
            (matches[0], tuple())
            if not return_matches
            else (matches[0], tuple(matches))
        )

    @classmethod
    def from_mimetype(
        cls,
        file_path: Union[str, Path],
        raise_err: bool = False,
        return_matches: bool = False,
    ) -> Tuple[FileType, Tuple[FileType, ...]]:
        """Determines a filetype from a file's MIME type.

        Args:
            file_path (str): The path to the file.
            raise_err (bool, optional): Whether to raise an exception if the type is unhandled. Defaults to False.
            return_matches (bool, optional): Whether to return a tuple with the first matching filetype and a list of all options. Defaults to False.

        Returns:
            FileType: The determined filetype enumeration member, or a tuple with the first matching filetype and a list of all options.

        Raises:
            FileNotFoundError: If the file does not exist.
            UnsupportedFileTypeError: If the file type is unhandled and raise_err is True.
        """
        file = Path(file_path)

        if not file.exists():
            raise FileNotFoundError(f"File '{file_path}' does not exist.")

        file_mimetype = guess_mime_type_from_file(str(file))

        matches = []
        for member in cls.get_filetypes():
            if (
                member.get_value().mime_types
                and file_mimetype in member.get_value().mime_types
            ):
                if not return_matches:
                    return (member, tuple())
                matches.append(member)

        if len(matches) == 0:
            if raise_err:
                raise UnsupportedFileTypeError(
                    f"Unhandled filetype from mimetype={file_mimetype}"
                )
            return (cls.UNHANDLED, tuple())

        return (
            (matches[0], tuple())
            if not return_matches
            else (matches[0], tuple(matches))
        )

    # @classmethod
    # def from_content(cls, path: Path, raise_err=False):
    #     file_path = Path(path)
    #     file_type = get_file_type(file_path)['f_type']
    #     # logger.info(file_type)
    #     return file_type #text/plain, application/json, text/xml, image/png, application/csv, image/gif, ...
    #     member = cls.UNHANDLED
    #     return member

    @classmethod
    def from_path(
        cls,
        path: Union[str, Path],
        read_content=False,
        raise_err=False,
        return_matches=False,
    ) -> Tuple[FileType, Tuple[FileType, ...]]:
        """Determines the filetype of a file based on its path. Optionally reads the file's content to verify its type.

        Args:
            path (Path): The path to the file.
            read_content (bool, optional): If True, the method also checks the file's content to determine its type.
                                           Defaults to False.
            raise_err (bool, optional): If True, raises exceptions for unsupported types or when file does not exist.
                                        Defaults to False.
            return_matches (bool, optional): Whether to return a tuple with the first matching filetype and a list of all options. Defaults to False.

        Returns:
            FileType: The determined filetype enumeration member based on the file's suffix and/or content, or a tuple with the first matching filetype and a list of all options.

        Raises:
            FileNotFoundError: If the file does not exist when attempting to read its content.
            UnsupportedFileTypeError: If the file type is unsupported and raise_err is True.
            AssertionError: If there is a mismatch between the file type determined from the file's suffix and its content.
        """
        file_path = Path(path)

        raise_err_suffix: bool = raise_err and (not read_content)
        raise_err_mimetype: bool = raise_err

        # get member from suffix
        filetype_from_suffix, suffix_matches = cls.from_suffix(
            file_path.suffix, raise_err=raise_err_suffix, return_matches=True
        )

        # if we're not checking the file content, return
        if not read_content:
            return filetype_from_suffix, suffix_matches

        # the file should exist for content reading
        if not file_path.exists():
            raise FileNotFoundError(f"File '{file_path}' does not exist.")

        # get member from content
        filetype_from_mimetype, mimetype_matches = cls.from_mimetype(
            file_path, raise_err=raise_err_mimetype, return_matches=True
        )

        # combine results from both methods

        # if suffix didn't give a filetype, use the one from content
        if filetype_from_suffix.is_true_filetype():
            return (
                (filetype_from_suffix, tuple())
                if not return_matches
                else (filetype_from_mimetype, mimetype_matches)
            )

        # if content mimetype didn't give a filetype, use the one from suffix
        if filetype_from_mimetype.is_true_filetype():
            return (
                (filetype_from_suffix, tuple())
                if not return_matches
                else (filetype_from_suffix, suffix_matches)
            )

        # find common matches
        common_members = tuple(m for m in suffix_matches if m in mimetype_matches)

        if len(common_members) == 0:
            if raise_err:
                raise AssertionError(
                    f"file type from suffix ({suffix_matches}) mismatch with file type from content ({mimetype_matches})"
                )
            return (cls.NOTYPE, tuple())

        return (
            (common_members[0], tuple())
            if not return_matches
            else (common_members[0], common_members)
        )

    def is_true_filetype(self) -> bool:
        """Determines if the filetype instance represents a supported file type based on the presence of defined extensions.

        Returns:
            bool: True if the filetype has at least one associated file extension, False otherwise.
        """
        return len(self.get_value().extensions) != 0

    def get_one_suffix(self) -> str:
        """
        Retrieves the primary file extension associated with the filetype.

        Returns:
            str: The primary file extension for the filetype, prefixed with a period.
                 Returns an empty string if the filetype does not have an associated extension.
        """
        if not self.is_true_filetype():
            return ""
        ext = self.get_value().extensions[0]
        return f".{ext}"

    def get_one_mimetype(self) -> str:
        """
        Retrieves the primary mimetype associated with the filetype.

        Returns:
            Mimetype: The primary mimetype for the filetype.
                 Returns an empty string if the filetype does not have an associated extension.
        """
        if not self.is_true_filetype():
            return ""
        return self.get_value().mime_types[0]

    def is_valid_suffix(self, suffix: str, raise_err=False) -> bool:
        """Validates whether a given file extension matches the filetype's expected extensions.

        Args:
            suffix (str): The file extension to validate, including the leading period (e.g., ".txt").
            raise_err (bool, optional): If True, raises a MismatchedException for invalid extensions.
                                        Defaults to False.

        Returns:
            bool: True if the suffix matches one of the filetype's extensions, False otherwise.

        Raises:
            MismatchedException: If the suffix does not match the filetype's extensions and raise_err is True.
        """
        _val, matches = self.from_suffix(suffix, return_matches=True)
        is_valid = (self == _val) if not self.is_true_filetype() else (self in matches)
        if is_valid:
            return True
        if raise_err:
            raise MismatchedException(
                f"filetype ({self.name}) mismatch with suffix ({suffix})",
                suffix,
                self.get_one_suffix(),
            )
        return False

    def is_valid_path(
        self, file_path: Union[str, Path], read_content=False, raise_err=False
    ) -> bool:
        """Validates the filetype of a given file path. Optionally reads the file's content to verify its type.

        Args:
            file_path (Union[str, Path]): The file path to validate.
            read_content (bool, optional): If True, the method also checks the file's content to validate its type.
                                           Defaults to False.
            raise_err (bool, optional): If True, raises exceptions for mismatched or unsupported types.
                                        Defaults to False.

        Returns:
            bool: True if the file path's type matches the filetype, False otherwise.

        Raises:
            AssertionError: If there is a mismatch between the file type determined from the file's suffix and its content.
            MismatchedException: If the file type determined from the file's suffix or content does not match the filetype.
        """
        _val, matches = self.from_path(
            file_path, read_content=read_content, return_matches=True
        )
        is_valid = (self == _val) if not self.is_true_filetype() else (self in matches)
        if is_valid:
            return True
        if raise_err:
            raise MismatchedException(
                f"suffix/mime-type ({file_path})",
                _val,
                self.get_value(),
            )
        return False

    def is_valid_mime_type(self, file_path: Path, raise_err=False) -> bool:
        """
        Validates whether the MIME type of the file at the specified path aligns with the filetype's expected MIME types.

        This method first determines the filetype based on the file's actual MIME type (determined by reading the file's content)
        and then checks if this determined filetype matches the instance calling this method. Special consideration is given to
        filetype.TEXT, where a broader compatibility check is performed due to the generic nature of text MIME types.

        Args:
            file_path (Path): The path to the file whose MIME type is to be validated.
            raise_err (bool, optional): If True, a MismatchedException is raised if the file's MIME type does not match
                                        the expected MIME types of the filetype instance. Defaults to False.

        Returns:
            bool: True if the file's MIME type matches the expected MIME types for this filetype instance or if special
                compatibility conditions are met (e.g., for filetype.TEXT with "text/plain"). Otherwise, False.

        Raises:
            MismatchedException: If raise_err is True and the file's MIME type does not match the expected MIME types
                                for this filetype instance, including detailed information about the mismatch.
        """
        _val, matches = self.from_mimetype(file_path, return_matches=True)
        is_valid = (self == _val) if not self.is_true_filetype() else (self in matches)
        if is_valid:
            return True
        if raise_err:
            raise MismatchedException(
                f"content-type({file_path})", _val, self.get_value().mime_types
            )
        return False


def extract_enum_members(enum_cls: Type) -> Dict[str, MimeType]:
    """Extracts MimeType instances from an enum class.

    Args:
        enum_cls (Type): The enum class.

    Returns:
        Dict[str, MimeType]: Dictionary of MimeType instances keyed by enum member names.
    """
    extracted_members: Dict[str, MimeType] = {}
    items: Iterable

    if issubclass(enum_cls, Enum):
        items = ((item.name, item.value) for item in enum_cls)
    else:
        assert hasattr(enum_cls, "__filetype_members__")
        filetype_members: Dict[str, MimeType] = enum_cls.__filetype_members__
        assert isinstance(filetype_members, dict)
        items = filetype_members.items()

    # Copy values from the added enum
    for item_name, item_value in items:
        # Make sure the value is of the inherited enum type
        assert isinstance(item_value, MimeType)
        extracted_members[item_name] = item_value

    return extracted_members


def extend_filetype_enum(added_enum: Type[Enum]) -> None:
    """Extends the BaseFileType enumeration with members from another enumeration.

    Args:
        added_enum (Type[Enum]): The enum class to extend BaseFileType with.
    """

    def is_member_mimetype(member: Enum):
        return isinstance(member.value, MimeType)

    return extend_enum_with_methods(
        FileType, added_enum, filter_func=is_member_mimetype
    )


class FileTypeExamples(Enum):
    """Enumeration of supported file types with methods for type determination and validation."""

    XML = MimeType(("xml",), ("application/xml", "text/xml"))


extend_filetype_enum(FileTypeExamples)


def get_mime_type_children(
    mime_type: MimeType, include_head: bool = False
) -> Set[MimeType]:
    """Recursively get all children MIME types in the subtree of the given MIME type.

    Args:
        mime_type (MimeType): The MIME type to get the subtree for.
        include_head (bool, optional): Controls whether to include the head node in the result. Defaults to False.

    Returns:
        Set[MimeType]: A set of all MIME types in the subtree.

    Example:
        >>> all_image_children = get_mime_type_children(MimeType(extensions=('png',), mime_types=('image/png',), upper_mime_types=(), children_mime_types=()))
        >>> print(all_image_children)
        {MimeType(extensions=('png',), mime_types=('image/png',), upper_mime_types=(), children_mime_types=()),
         MimeType(extensions=('jpeg', 'jpg'), mime_types=('image/jpeg',), upper_mime_types=(), children_mime_types=()),
         MimeType(extensions=('tiff',), mime_types=('image/tiff',), upper_mime_types=(), children_mime_types=())}
    """
    subtree = {mime_type} if include_head else set()

    def collect_children(node: MimeType):
        for child in node.children_mime_types:
            if child not in subtree:
                subtree.add(child)
                collect_children(child)

    collect_children(node=mime_type)
    return subtree


def get_equivalent_file_types(
    mime_types: Set[MimeType], raise_error: bool = True
) -> Set[FileType]:
    """Get the equivalent FileTypes for a given list of MimeTypes.

    Args:
        mime_types (Set[MimeType]): The list of MIME types to find the equivalent FileTypes for.
        raise_error (bool, optional): Controls whether to raise an error if no equivalent FileType is found. Defaults to True.

    Returns:
        List[FileType]: A list of equivalent FileTypes if found, otherwise None.
    """
    mime_types = set(mime_types)
    equivalents = set()
    for file_type in FileType:
        if file_type.value in mime_types:
            equivalents.add(file_type)
    if raise_error and len(equivalents) != len(mime_types):
        missing_mimetypes = mime_types - set(mt.value for mt in equivalents)
        raise ValueError(
            f"No equivalent FileType found the {len(mime_types) - len(equivalents)} following MIME types: {missing_mimetypes}"
        )
    return equivalents


def get_file_type_children(
    file_type: FileType, include_head: bool = False
) -> Set[FileType]:
    """Recursively get all children FileTypes as equivalent FileTypes of the MIME types in the subtree of the given FileType.

    Args:
        file_type (FileType): The FileType to get the subtree for.
        include_head (bool, optional): Controls whether to include the head node in the result. Defaults to False.

    Returns:
        Set[FileType]: A set of all equivalent FileTypes in the subtree.

    Example:
        >>> all_image_children = get_file_type_children(FileType.IMG_RASTER)
        >>> print(all_image_children)
        {FileType.PNG, FileType.JPEG, FileType.TIFF}
    """
    mime_type_children: Set[MimeType] = get_mime_type_children(
        file_type.value, include_head
    )
    file_type_equivalents: Set[FileType] = get_equivalent_file_types(mime_type_children)
    return file_type_equivalents


def get_file_types_clidren(
    file_types: Iterable[FileType], include_head: bool = False
) -> Set[FileType]:
    """Recursively get all children FileTypes as equivalent FileTypes of the MIME types
    in the subtree of the given list of FileType instances.

    Args:
        file_types (List[FileType]): The list of FileType instances to get the subtree for.
        include_head (bool, optional): Controls whether to include the head node in the result. Defaults to False.

    Returns:
        Set[FileType]: A set of all equivalent FileTypes in the subtree.

    Example:
        >>> all_image_children = get_file_types_from_list([FileType.IMG_RASTER])
        >>> print(all_image_children)
        {FileType.PNG, FileType.JPEG, FileType.TIFF}
    """
    children = set()
    for file_type in file_types:
        children |= get_file_type_children(file_type, include_head)
    return children
