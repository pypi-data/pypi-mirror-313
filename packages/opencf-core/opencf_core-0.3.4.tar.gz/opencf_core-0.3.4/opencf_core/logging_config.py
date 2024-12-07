import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

logging_nameToLevel = logging._nameToLevel  # pylint: disable=protected-access


class ColoredFormatter(logging.Formatter):
    """
    - original code from [Sergey Pleshakov, stackoverflow](https://stackoverflow.com/a/56944256/16668046)
    """

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + log_format + reset,
        logging.INFO: grey + log_format + reset,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(fmt=log_fmt)
        return formatter.format(record=record)


class LoggerConfig:
    def __init__(self) -> None:
        self.logger: logging.Logger = logging.Logger("_")
        self.log_file: Optional[Path] = None
        self.log_level: int = logging.INFO

    def setup_logger(
        self, name: str, log_file: Optional[str] = None, level: int = logging.INFO
    ) -> None:
        """Set up logger.

        Args:
            name (str): Name of the logger.
            log_file (str, optional): Path to the log file. Defaults to None.
            level (int, optional): Logging level. Defaults to logging.INFO.
        """
        self.logger = logging.getLogger(name=name)
        self.logger.setLevel(level=level)

        formatter = ColoredFormatter()

        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(hdlr=handler)

        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(fmt=formatter)
        self.logger.addHandler(hdlr=console_handler)

        # Add file handler if log_file is provided
        if log_file:
            self.set_log_file(log_file=log_file)

    def set_log_file(self, log_file: str) -> None:
        """Set log file.

        Args:
            log_file (str): Path to the log file.
        """
        if log_file == "default":
            # Save log file in user's home directory with a timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_directory = Path.home() / ".cache" / "openconv-core"
            # Create directory if it doesn't exist
            log_directory.mkdir(parents=True, exist_ok=True)
            self.log_file = log_directory / f"{timestamp}.log"
        else:
            # Use the provided log file path
            self.log_file = Path(log_file).expanduser()

        file_handler = logging.FileHandler(filename=self.log_file)
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(fmt=formatter)
        self.logger.addHandler(hdlr=file_handler)

    def set_log_level(self, level: int) -> None:
        """Set log level.

        Args:
            level (int): Logging level.
        """
        self.log_level = level
        if self.logger:
            self.logger.setLevel(level=level)

    def set_log_level_str(self, level: str) -> None:
        """Set log level.

        Args:
            level (str): Logging level.
        """
        parsed_level: int = logging_nameToLevel[level.upper()]
        self.set_log_level(level=parsed_level)


# Create an instance of LoggerConfig
logger_config: LoggerConfig = LoggerConfig()

# Set up logger with default log file location and level
logger_config.setup_logger(name="openconv-core", log_file="default", level=logging.INFO)

# Define the logger to log messages
logger: logging.Logger = logger_config.logger
