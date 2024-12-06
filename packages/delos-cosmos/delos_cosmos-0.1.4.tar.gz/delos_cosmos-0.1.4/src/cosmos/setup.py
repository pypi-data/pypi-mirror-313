"""Logger and other default settings for the Cosmos client."""

import sys

from loguru import logger

logger.add(
    sys.stderr,
    format="{time} {level} {message}",
    level="INFO",
)
