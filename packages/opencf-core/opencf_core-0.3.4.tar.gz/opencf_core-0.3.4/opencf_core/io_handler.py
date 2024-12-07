"""
Input/Output Handler Module

This module is designed to provide a structured approach to handling file input and output operations across various
formats such as plain text, CSV, JSON, and potentially XML. It introduces a set of abstract base classes and concrete
implementations for reading from and writing to files, ensuring type safety and format consistency through method
signatures and runtime checks.
"""

import csv
import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List


class Reader(ABC):
    """
    Abstract base class for file readers.
    """

    # input_format: type = None

    def check_input_format(self, content: Any) -> bool:
        return self._check_input_format(content=content)

    @abstractmethod
    def _check_input_format(self, content: Any) -> bool:
        """
        Checks if the provided content matches the expected input format.

        Args:
            content (Any): The content to be checked.

        Returns:
            bool: True if the content matches the expected input format, False otherwise.
        """
        raise NotImplementedError

    def read_content(self, input_path: Path) -> Any:
        return self._read_content(input_path=input_path)

    @abstractmethod
    def _read_content(self, input_path: Path) -> Any:
        """
        Reads and returns the content from the given input path.

        Args:
            input_path (Path): The path to the input file.

        Returns:
            Any: The content read from the input file.
        """
        raise NotImplementedError


class Writer(ABC):
    """
    Abstract base class for file writers.
    """

    # output_format = None

    def check_output_format(self, content: Any) -> bool:
        return self._check_output_format(content=content)

    @abstractmethod
    def _check_output_format(self, content: Any) -> bool:
        """
        Checks if the provided content matches the expected output format.

        Args:
            content (Any): The content to be checked.

        Returns:
            bool: True if the content matches the expected output format, False otherwise.
        """
        raise NotImplementedError

    def write_content(self, output_path: Path, output_content: Any):
        return self._write_content(
            output_path=output_path, output_content=output_content
        )

    @abstractmethod
    def _write_content(self, output_path: Path, output_content: Any):
        """
        Writes the provided content to the given output path.

        Args:
            output_path (Path): The path to the output file.
            output_content (Any): The content to be written to the output file.
        """
        raise NotImplementedError


class Converter(ABC):
    """
    Abstract base class for data converters.
    """

    def check_input_format(self, content: Any) -> bool:
        return self._check_input_format(content=content)

    @abstractmethod
    def _check_input_format(self, content: Any) -> bool:
        """
        Checks if the provided content matches the expected input format.

        Args:
            content (Any): The content to be checked.

        Returns:
            bool: True if the content matches the expected input format, False otherwise.
        """
        raise NotImplementedError

    def check_output_format(self, content: Any) -> bool:
        return self._check_output_format(content=content)

    @abstractmethod
    def _check_output_format(self, content: Any) -> bool:
        """
        Checks if the provided content matches the expected output format.

        Args:
            content (Any): The content to be checked.

        Returns:
            bool: True if the content matches the expected output format, False otherwise.
        """
        raise NotImplementedError

    def convert(self, content: Any) -> Any:
        return self._convert(content=content)

    @abstractmethod
    def _convert(self, content: Any) -> Any:
        """
        Converts the provided content from the input format to the output format.

        Args:
            content (Any): The content to be converted.

        Returns:
            Any: The converted content in the output format.
        """
        raise NotImplementedError


class SamePathReader(Reader):
    """
    A Reader that returns the input path itself, useful for operations where the file path is the desired output.
    """

    input_format = Path

    def _check_input_format(self, content: Path):
        return isinstance(content, Path)

    def _read_content(self, input_path: Path) -> Path:
        return input_path


class TxtToStrReader(Reader):
    """
    Reads content from a text file and returns it as a string.
    """

    input_format = str

    def _check_input_format(self, content: str):
        return isinstance(content, str)

    def _read_content(self, input_path: Path) -> str:
        return input_path.read_text()


class StrToTxtWriter(Writer):
    """
    Writes a string to a text file.
    """

    output_format = str

    def _check_output_format(self, content: str):
        return isinstance(content, str)

    def _write_content(self, output_path: Path, output_content: str):
        output_path.write_text(output_content)


class XmlToTreeReader(Reader):
    """
    Reads content from an XML file and returns it as an ElementTree element.
    """

    input_format = ET.Element

    def _check_input_format(self, content: ET.Element) -> bool:
        """
        Validates the input content to ensure it is an ElementTree element.

        Args:
            content (ET.Element): The content to validate.

        Returns:
            bool: True if the content is a valid ElementTree element, False otherwise.
        """
        return isinstance(content, ET.Element)

    def _read_content(self, input_path: Path) -> ET.Element:
        """
        Reads and parses the content from the XML file at the given path.

        Args:
            input_path (Path): The path to the XML file.

        Returns:
            ET.Element: The root element of the parsed XML tree.
        """
        text_content = input_path.read_text()
        return ET.fromstring(text_content)


class TreeToXmlWriter(Writer):
    """
    Writes content from a dictionary to an XML file.
    """

    output_format = ET.Element

    def _check_output_format(self, content: ET.Element) -> bool:
        """
        Validates the output content to ensure it is an ElementTree element.

        Args:
            content (ET.Element): The content to validate.

        Returns:
            bool: True if the content is a valid ElementTree element, False otherwise.
        """
        return isinstance(content, ET.Element)

    def _write_content(self, output_path: Path, output_content: ET.Element) -> None:
        """
        Writes the ElementTree element content to an XML file at the given path.

        Args:
            output_path (Path): The path to the XML file.
            content (ET.Element): The ElementTree element content to write.
        """
        tree = ET.ElementTree(output_content)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)


class CsvToDictReader(Reader):
    """
    Reads content from a CSV file and returns it as a list of dictionaries.

    Example:
        >>> reader = CsvToDictReader()
        >>> content = reader.read(Path('input.csv'))
        >>> print(content)
        [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]
    """

    input_format = List[Dict[str, Any]]

    def _check_input_format(self, content: List[Dict[str, Any]]) -> bool:
        """
        Validates the input content to ensure it is a list of dictionaries.

        Args:
            content (List[Dict[str, Any]]): The content to validate.

        Returns:
            bool: True if the content is a list of dictionaries, False otherwise.
        """
        return isinstance(content, list) and all(
            isinstance(row, dict) for row in content
        )

    def _read_content(self, input_path: Path) -> List[Dict[str, Any]]:
        """
        Reads and parses the content from the CSV file at the given path.

        Args:
            input_path (Path): The path to the CSV file.

        Returns:
            List[Dict[str, Any]]: The parsed content as a list of dictionaries.
        """
        with input_path.open(mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)
            return rows


class DictToCsvWriter(Writer):
    """
    Writes content from a dictionary to a CSV file.
    """

    output_format = List[Dict[str, Any]]

    def _check_output_format(self, content: List[Dict[str, Any]]) -> bool:
        """
        Validates the output content to ensure it is a list of dictionaries.

        Args:
            content (List[Dict[str, Any]]): The content to validate.

        Returns:
            bool: True if the content is a list of dictionaries, False otherwise.
        """
        return isinstance(content, list) and all(
            isinstance(row, dict) for row in content
        )

    def _write_content(
        self, output_path: Path, output_content: List[Dict[str, Any]]
    ) -> None:
        """
        Writes the list of dictionaries content to a CSV file at the given path.

        Args:
            output_path (Path): The path to the CSV file.
            content (List[Dict[str, Any]]): The list of dictionaries content to write.
        """
        with output_path.open(mode="w", encoding="utf-8", newline="") as csv_file:
            if output_content:
                writer = csv.DictWriter(csv_file, fieldnames=output_content[0].keys())
                writer.writeheader()
                writer.writerows(output_content)


class JsonToDictReader(Reader):
    """
    Reads content from a JSON file and returns it as a dictionary.
    """

    input_format = Dict[str, Any]

    def _check_input_format(self, content: Dict[str, Any]):
        return isinstance(content, dict)

    def _read_content(self, input_path: Path) -> Dict[str, Any]:
        return json.loads(input_path.read_text())


class DictToJsonWriter(Writer):
    """
    Writes content from a dictionary to a JSON file.
    """

    output_format = Dict[str, Any]

    def _check_output_format(self, content: Dict[str, Any]):
        return isinstance(content, dict)

    def _write_content(self, output_path: Path, output_content: Dict[str, Any]):
        return output_path.write_text(json.dumps(output_content, indent=4))


class XmlToStrReader(Reader):
    """
    Reads content from an XML file and returns it as a string.
    """

    input_format = str

    def _check_input_format(self, content: str):
        # Add your XML validation logic here
        return isinstance(content, str)

    def _read_content(self, input_path: Path) -> str:
        return input_path.read_text()


class StrToXmlWriter(Writer):
    """
    Writes content as a string to an XML file.
    """

    output_format = str

    def _check_output_format(self, content: str):
        # Add your XML validation logic here
        return isinstance(content, str)

    def _write_content(self, output_path: Path, output_content: str):
        output_path.write_text(output_content)
