# OpenCF Core: The File Convertion Framework

The `opencf-core` package provides a robust framework for handling file conversion tasks in Python. It offers a set of classes and utilities designed to simplify the process of reading from and writing to different file formats efficiently.

## Features

- **Modular Input/Output Handlers**: Defines abstract base classes for file readers and writers, allowing for easy extension and customization.
- **Support for Various File Formats**: Provides built-in support for common file formats such as text, CSV, JSON, XML, Excel, and image files.
- **MIME Type Detection**: Includes a MIME type guesser utility to automatically detect the MIME type of files, facilitating seamless conversion based on file content.
- **File Type Enumeration**: Defines an enum for representing different file types, enabling easy validation and processing of input and output files.
- **Exception Handling**: Implements custom exceptions for handling errors related to unsupported file types, empty suffixes, file not found, and mismatches between file types.
- **Base Converter Class**: Offers an abstract base class for implementing specific file converters, providing a standardized interface for file conversion operations.
- **Resolved Input File Representation**: Introduces a class for representing input files with resolved file types, ensuring consistency and correctness in conversion tasks.

## Conversion Strategies

When using the `opencf-core`, you can adopt different strategies for file conversion based on your specific requirements:

### 1. Direct Conversion

In this approach, conversion is achieved without utilizing a dedicated writer. The reader module parses the input files into a list of objects. Subsequently, the `_convert` method orchestrates the writing process into a file or folder. This method is suitable for scenarios where direct manipulation of data structures suffices for conversion.

### 2. Indirect Conversion

Conversely, indirect conversion employs a converter that supports a dedicated writer. Here, the `convert` function's primary role is to transform the parsed list of objects into a format compatible with the writer. The actual conversion process may be executed by the writer, leveraging its capabilities. For instance, converting images to videos involves parsing images into a list of Pillow objects, which are then reformatted into a numpy array. This array, encapsulating frame dimensions and color channels, serves as input for the video writer.

## Component Instances

The file conversion process can be dissected into three distinct instances:

- **Reader**: Handles input-output (IO) operations, transforming files into objects. Readers are implementations of the abstract class `Reader` present in `io_handler.py`.
- **Converter**: Facilitates object-to-object conversion, acting as an intermediary for data transformation. Converters are implementations of the abstract class `BaseConverter` present in `base_converter.py`.

- **Writer (Optional)**: Reverses the IO process, converting objects back into files. Writers are implementations of the abstract class `Writer` present in `io_handler.py`.

## Modules

- **io_handler.py**: Contains classes for reading from and writing to files, including text, CSV, JSON, XML, and image files. It includes abstract classes for `Reader` and `Writer`.
- **mimes.py**: Provides a MIME type guesser utility for detecting file MIME types based on file content.
- **filetypes.py**: Defines enums and classes for representing different file types and handling file type validation.
- **base_converter.py**: Implements the base converter class and the resolved input file class for performing file conversion tasks. It includes the `BaseConverter` abstract class.

## Installation

```bash
pip install opencf-core
```

## Usage

The `opencf-core` package can be used independently to build custom file conversion utilities or integrated into larger projects for handling file format transformations efficiently.

```python
from opencf_core.io_handler import CsvToListReader, ListToCsvWriter
from opencf_core.base_converter import BaseConverter, ResolvedInputFile
from opencf_core.filetypes import FileType

class CSVToJSONConverter(BaseConverter):
    file_reader = CsvToListReader()
    file_writer = DictToJsonWriter()

    @classmethod
    def _get_supported_input_type(cls) -> FileType:
        return FileType.CSV

    @classmethod
    def _get_supported_output_type(cls) -> FileType:
        return FileType.JSON

    def _convert(self, input_path: Path, output_file: Path):
        # Implement conversion logic from CSV to JSON
        pass

# Usage
input_file_path = "input.csv"
output_file_path = "output.json"
input_file = ResolvedInputFile(input_file_path, is_dir=False, should_exist=True)
output_file = ResolvedInputFile(output_file_path, is_dir=False, should_exist=False, add_suffix=True)
converter = CSVToJSONConverter(input_file, output_file)
converter.convert()
```

## More Examples

The `examples` folder in this repository contains practical demonstrations of how to use the `opencf-core` package for file conversion tasks. Currently, it includes the following examples:

- **simple_converter.py**: Demonstrates a basic file converter that converts Excel (XLSX) files to CSV format. It utilizes the `XLXSToCSVConverter` class defined within the `opencf-core` package to perform the conversion.

- **cli_app_example.py**: Illustrates how to build a command-line interface (CLI) application using the `ConverterApp` class from the `opencf-core.converter_app` module. This CLI app allows users to specify input and output files, as well as input and output file types, for performing file conversions.

These examples serve as practical demonstrations of how to leverage the capabilities of the `opencf-core` package in real-world scenarios. Users can refer to these examples for guidance on building their own file conversion utilities or integrating file conversion functionality into existing projects.

You can have a more practical insight by reading the [support associated to the examples](./examples/readme.md)

## Todo

### Backend Support

- Introduce the concept of backend labeling for `Reader` and `Writer` implementations.
- Enable multiple file readers/writers to share common backends. For instance, if an `ImageOpenCVReader` utilizes both numpy and OpenCV, the `VideoWriter` can leverage the same dependencies.
- Allow users to specify preferred backend configurations, ensuring that conversion methods accommodate all selected backends seamlessly.

## Contributing

Contributions to the `opencf-core` package are welcome! Feel free to submit bug reports, feature requests, or pull requests via the GitHub repository.

## Disclaimer

Please note that while the `opencf-core` package aims to provide a versatile framework for file conversion tasks, it may not cover every possible use case or handle all edge cases. Users are encouraged to review and customize the code according to their specific requirements.
