"""Cosmos custom fields for API Requests."""

from enum import Enum


class FileTranslationReturnType(str, Enum):
    """Enumeration for type of possible request when translating a file."""

    RAW_TEXT = "raw_text"
    URL = "url"
    FILE = "file"


class ParserExtractType(str, Enum):
    """Enum for extract types in chunking operations."""

    SUBCHUNKS = "subchunks"
    CHUNKS = "chunks"
    PAGES = "pages"
    FILE = "file"
