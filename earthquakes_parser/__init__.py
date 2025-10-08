"""EarthquakesParser - A library for searching and parsing earthquake-related content."""

__version__ = "0.1.0"

from earthquakes_parser.search.searcher import KeywordSearcher
from earthquakes_parser.parser.content_parser import ContentParser
from earthquakes_parser.storage.base import StorageBackend
from earthquakes_parser.storage.csv_storage import CSVStorage

__all__ = [
    "KeywordSearcher",
    "ContentParser",
    "StorageBackend",
    "CSVStorage",
]
