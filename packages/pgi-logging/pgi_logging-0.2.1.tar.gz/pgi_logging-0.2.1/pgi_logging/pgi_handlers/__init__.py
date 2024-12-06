"""Custom default handlers for logging."""

import os
import pathlib
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler

from colorlog import ColoredFormatter

from pgi_logging.utils import (
    LEVEL_COLORS,
    LOG_BACKUP_COUNT,
    LOG_MAX_BYTES,
    LoggerLevel,
)

# Flag to check if tkinter is available, can override with environment variable
SKIP_TKINTER_CHECK = os.getenv("SKIP_TKINTER_CHECK", False)

# try and get as an environment variable. If it doesn't exist, check if tkinter is available
NO_TKINTER = os.getenv("NO_TKINTER", None)
if not SKIP_TKINTER_CHECK and NO_TKINTER is None:
    try:
        import tkinter  # noqa

        NO_TKINTER = False
    except ImportError:
        NO_TKINTER = True

if not NO_TKINTER:
    # If tkinter exists, import the TkinterTextHandler and get_tkinter_handler
    from .tk import TkinterTextHandler, get_tkinter_handler

    __all__ = ["TkinterTextHandler", "get_tkinter_handler"]


"""         CUSTOM FORMATTERS         """
# For the 'fmt' parameter, refer to the link below
# LINK: https://docs.python.org/3/library/logging.html#logrecord-attributes
SimpleConsoleFormatter = ColoredFormatter(
    fmt="%(name)-10s %(log_color)s%(levelname)-8s %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S",
    reset=True,
    log_colors=LEVEL_COLORS,
    secondary_log_colors={},
    style="%",
)

VerboseConsoleFormatter = ColoredFormatter(
    fmt="%(name)-10s %(log_color)s%(levelname)-8s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S",
    reset=True,
    log_colors=LEVEL_COLORS,
    secondary_log_colors={},
    style="%",
)

SimpleFileFormatter = Formatter(
    fmt="%(levelname)-8s %(message)s", datefmt="%d/%b/%Y %H:%M:%S", style="%"
)

VerboseFileFormatter = Formatter(
    fmt="[%(asctime)s] %(levelname)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S",
    style="%",
)


"""         GET HANDLER FUNCTIONS         """


def get_stream_handler(
    log_level: LoggerLevel = LoggerLevel.DEBUG, verbose: bool = False
) -> StreamHandler:
    """Create a StreamHandler with a custom formatter."""
    if verbose:
        formatter = VerboseConsoleFormatter
    else:
        formatter = SimpleConsoleFormatter

    # Create the handler and set the formatter and the level
    handler = StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(log_level.value)
    return handler


def get_file_handler(
    log_directory: str,
    log_filename: str,
    log_level: LoggerLevel = LoggerLevel.DEBUG,
    verbose: bool = False,
) -> RotatingFileHandler:
    """Create a RotatingFileHandler with a custom formatter."""
    if verbose:
        formatter = VerboseFileFormatter
    else:
        formatter = SimpleFileFormatter

    # Create the directory if it doesn't exist and make the filename
    log_dir = pathlib.Path(log_directory)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / log_filename
    if log_file.suffix != ".log":
        raise ValueError("Log file must have a .log extension")

    # Create the handler and set the formatter and the level
    handler = RotatingFileHandler(
        log_file, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT
    )
    handler.setFormatter(formatter)
    handler.setLevel(log_level.value)
    return handler
