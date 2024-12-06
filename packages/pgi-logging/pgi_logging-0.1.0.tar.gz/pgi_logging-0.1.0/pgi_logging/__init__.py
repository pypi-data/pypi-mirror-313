"""Logging module for the PGI project."""

import logging
import pathlib
import time
from typing import TYPE_CHECKING, Optional

from pgi_logging import pgi_handlers

if TYPE_CHECKING:
    from logging import Logger

    import cloudpathlib


def create_default_log_filename(logger_name: str | None = None) -> str:
    """Create a default log filename using the current time and logger name."""
    if logger_name:
        return f"{int(time.time())}_{logger_name}.log"
    else:
        return f"{int(time.time())}.log"


def create_default_log_dir() -> pathlib.Path:
    """Create a default log directory in the user's home directory."""
    directory = pathlib.Path("~/logs").expanduser()
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def shutdown_logger(logger: "Logger") -> None:
    """Shutdown the logger.

    Args:
    ----
        logger (Logger): The logger to shut down

    """
    logger.critical(f"Shutting down '{logger.name}' logger.")
    for handler in logger.handlers:
        handler.flush()
        handler.close()
        logger.removeHandler(handler)
    logging.shutdown()


"""         LOGGER CREATION FUNCTIONS         """


def base_default_logger(
    logger_name: str,
    log_dir: "pathlib.Path | cloudpathlib.S3Path | None" = None,
    log_filename: Optional[str] = None,
    log_level: pgi_handlers.LoggerLevel = pgi_handlers.LoggerLevel.DEBUG,
    include_file_handler: bool = True,
    verbose_console: bool = True,
    verbose_file: bool = True,
) -> "Logger":
    """Create a base logger using the PGI logger.

    Args:
    ----
        logger_name: str | None
            The name of the logger
        log_dir: pathlib.Path | cloudpathlib.S3Path | None
            The path to the directory where the log file will be saved
        log_filename: str; None
            The name of the log file to create
        log_level: pgi_handlers.LoggerLevel
            The level of logging to use
        include_file_handler: bool; True
            Whether to include the file handler
        verbose_console: bool; True
            Whether to log to the verbose console handler rather than the simple one
        verbose_file: bool; True
            Whether to log to the verbose file handler rather than the simple one

    Returns:
        PGILogger:
            The logger object

    """
    # Set the default log directory and filename if not provided, only if including the file handler
    if include_file_handler:
        if log_dir is None:
            log_dir = create_default_log_dir()
        if log_filename is None:
            log_filename = create_default_log_filename(logger_name)
        file_handler = pgi_handlers.get_file_handler(
            log_directory=log_dir,
            log_filename=log_filename,
            log_level=log_level,
            verbose=verbose_file,
        )
    else:
        if log_dir is not None or log_filename is not None:
            print(
                "Log directory and filename are ignored if not including the file handler to the logger."
            )

    # Get the console and file handlers
    console_handler = pgi_handlers.get_stream_handler(
        log_level=log_level, verbose=verbose_console
    )

    # First get the logger, if there are any handlers already attached, remove them
    logger = logging.getLogger(logger_name)
    for handler in logger.handlers:
        logger.removeHandler(handler)

    # Set the level and add the handlers
    logger.setLevel(log_level.value)
    logger.addHandler(console_handler)
    if include_file_handler:
        logger.addHandler(file_handler)
    return logger


def create_default_utils_logger(
    log_dir: "pathlib.Path | cloudpathlib.S3Path | None" = None,
    log_filename: str | None = None,
    log_level: pgi_handlers.LoggerLevel = pgi_handlers.LoggerLevel.DEBUG,
) -> "Logger":
    """Create a logger for a utils script."""
    return base_default_logger(
        logger_name="utils",
        log_dir=log_dir,
        log_filename=log_filename,
        log_level=log_level,
    )


def create_default_inference_logger(
    log_dir: "pathlib.Path | cloudpathlib.S3Path | None" = None,
    log_filename: str | None = None,
    log_level: pgi_handlers.LoggerLevel = pgi_handlers.LoggerLevel.DEBUG,
) -> "Logger":
    """Create a logger for an inference run."""
    return base_default_logger(
        logger_name="inference",
        log_dir=log_dir,
        log_filename=log_filename,
        log_level=log_level,
    )


def create_default_training_logger(
    log_dir: "pathlib.Path | cloudpathlib.S3Path | None" = None,
    log_filename: str | None = None,
    log_level: pgi_handlers.LoggerLevel = pgi_handlers.LoggerLevel.DEBUG,
) -> "Logger":
    """Create a logger for a training run."""
    return base_default_logger(
        logger_name="training",
        log_dir=log_dir,
        log_filename=log_filename,
        log_level=log_level,
    )
