"""Constants and utility functions for logging."""

import logging
from enum import Enum

# Different logging levels and their colors for colorlog
LEVEL_COLORS = {
    logging.NOTSET: "white",
    logging.DEBUG: "cyan",
    logging.INFO: "green",
    logging.WARNING: "yellow",
    logging.ERROR: "red",
    logging.CRITICAL: "red,bg_white",
}


# Level colors as an Enum
class LevelColors(Enum):
    """Enum class for level colors."""

    NOTSET = "white"
    DEBUG = "cyan"
    INFO = "green"
    WARNING = "yellow"
    ERROR = "red"
    CRITICAL = "red,bg_white"


# Dictionary of level colors for colorlog
LEVEL_COLORS = {i.name: i.value for i in LevelColors}


# Logger levels as an Enum
class LoggerLevel(Enum):
    """Enum class for logging levels."""

    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


# File logging constants
LOG_MAX_BYTES = 52428800  # 50 MB
LOG_BACKUP_COUNT = 20  # number of log files to keep before removing old ones
