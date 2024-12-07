"""
Main Module

This module contains the main application logic.
"""

import traceback
from collections import defaultdict
from itertools import product
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Type

from .base_converter import BaseConverter
from .file_handler import ResolvedInputFile
from .filetypes import FileType
from .logging_config import logger
from .utils import get_filepaths_from_inputs


class BaseConverterApp:
    """
    Main application class responsible for managing file conversions.
    """

    converters: List[Type[BaseConverter]] = []
    filetype_class: Type[FileType] = FileType

    def __init__(
        self,
        input_paths: List[str],
        input_file_type: Optional[str] = None,
        output_file_path: Optional[str] = None,
        output_file_type: Optional[str] = None,
    ):
        """
        Initializes the BaseConverterApp instance.

        Args:
            input_paths (List[str]): List of paths to the input files.
            input_file_type (FileType, optional): The type of the input file. Defaults to None.
            output_file_path (str, optional): The path to the output file. Defaults to None.
            output_file_type (FileType, optional): The type of the output file. Defaults to None.
        """

        self._converter_map: Dict[
            Tuple[FileType, FileType], List[Type[BaseConverter]]
        ] = defaultdict(list)

        if not isinstance(input_paths, list):
            raise TypeError("input_paths sould be a list")
        if len(input_paths) == 0:
            raise ValueError("input_paths should not be a empty list")

        input_file_paths: List[str] = get_filepaths_from_inputs(input_paths)
        logger.debug("input_file_paths = %s", input_file_paths)
        self.input_files: List[ResolvedInputFile] = [
            ResolvedInputFile(
                input_file_path,
                is_dir=False,
                should_exist=True,
                file_type=input_file_type,
                add_suffix=False,
                read_content=True,
                filetype_class=self.filetype_class,
            )
            for input_file_path in input_file_paths
        ]

        self.input_file_type: FileType = self.input_files[0].file_type
        assert self.input_file_type.is_true_filetype()

        if not output_file_path:
            output_file_path = str(Path(input_file_paths[0]).with_suffix(""))
            add_suffix_to_output_path = True
            assert (
                output_file_type is not None
            ), "either output_file_path or output_file_type should be set "
        else:
            add_suffix_to_output_path = False

        self.output_file: ResolvedInputFile = ResolvedInputFile(
            output_file_path,
            is_dir=None,
            should_exist=False,
            file_type=output_file_type,
            add_suffix=add_suffix_to_output_path,
            read_content=False,
            filetype_class=self.filetype_class,
        )
        self.output_file_type: FileType = self.output_file.file_type

        for _conv_class in self.converters:
            self.add_converter_pair(_conv_class)

    def add_converter_pair(self, converter_class) -> None:
        """
        Adds a converter pair to the application.

        Args:
            converter_class (Type[BaseConverter]): The converter class to add.

        Raises:
            ValueError: If the converter class is invalid.
        """
        # Check if the converter_class is a subclass of BaseConverter
        if not issubclass(converter_class, BaseConverter):
            raise ValueError(
                "Invalid converter class. Must be a subclass of BaseConverter."
            )

        # Extract supported input and output types from the converter class
        input_types: Tuple[FileType, ...] = converter_class.get_input_types(extend=True)
        output_types: Tuple[FileType, ...] = converter_class.get_output_types(
            extend=True
        )

        # Add the converter pair to the converter map
        for input_type, output_type in product(input_types, output_types):
            self._converter_map[(input_type, output_type)].append(converter_class)

    def get_converters_for_conversion(
        self, input_type: FileType, output_type: FileType
    ) -> List[Type[BaseConverter]]:
        """
        Returns a list of converter classes for a given input-output type pair.

        Args:
            input_type (str): The input type.
            output_type (str): The output type.

        Returns:
            List[Type[BaseConverter]]: List of converter classes if found, else an empty list.
        """
        return self._converter_map[(input_type, output_type)]

    def get_supported_conversions(
        self,
    ) -> Tuple[Tuple[FileType, FileType], ...]:
        """
        Retrieves the supported conversions.

        Returns:
            Tuple[Tuple[FileType, FileType]]: A tuple of tuples representing supported conversions.
        """
        return tuple(self._converter_map.keys())

    def run(self) -> None:
        """
        Runs the conversion process.
        """
        # get converter class
        converter_classes: List[
            type[BaseConverter]
        ] = self.get_converters_for_conversion(
            self.input_file_type, self.output_file_type
        )

        # make sure a converter class exists
        if len(converter_classes) == 0:
            _ = "\n " + "\n ".join(
                map(lambda x: f"* {x[0]} -> {x[1]}", self.get_supported_conversions())
            )
            logger.error(
                "Conversion from %s to %s not supported. Supported convertions are : {_}",
                self.input_file_type,
                self.output_file_type,
            )
            return

        # Initialize a flag to track if any converter succeeded
        conversion_successful = False

        # Try each converter class until one succeeds
        for converter_class in converter_classes:
            try:
                logger.info("Atempting conversion with %s", converter_class.__name__)

                # Instantiate the converter
                converter = converter_class(self.input_files, self.output_file)

                # Run the conversion pipeline
                converter.run_conversion()

                # Set the flag to indicate success
                conversion_successful = True

                # Break the loop if conversion succeeds
                break
            except Exception as exc:
                logger.error(
                    "Conversion with %s failed: %s", converter_class.__name__, exc
                )
                logger.error(traceback.format_exc())

        # If none of the converter classes succeeded, log an error
        if not conversion_successful:
            logger.error("%s conversion attempts failed.", len(converter_classes))
