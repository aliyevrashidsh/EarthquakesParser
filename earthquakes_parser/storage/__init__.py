"""Storage backends for saving parsed data."""

from earthquakes_parser.storage.base import StorageBackend
from earthquakes_parser.storage.csv_storage import CSVStorage

__all__ = ["StorageBackend", "CSVStorage"]
