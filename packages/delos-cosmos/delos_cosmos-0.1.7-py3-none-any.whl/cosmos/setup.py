"""Logger and other default settings for the Cosmos client."""

from enum import Enum

from loguru import logger


class VerboseLevel(int, Enum):
    """Verbose level for the logger."""

    SILENT = 0
    INFO = 1
    DEBUG = 2


__all__ = ["logger"]
