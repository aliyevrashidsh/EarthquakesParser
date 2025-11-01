"""
EarthquakesParser - A library for searching and parsing earthquakes.

This library provides tools for earthquake-related content search and parsing.
"""

__version__ = "0.1.0"

from earthquakes_parser.parser.content_parser import ContentParser
from earthquakes_parser.storage.csv_storage import CSVStorage
from earthquakes_parser.storage.supabase import SupabaseDB, SupabaseFileStorage

__all__ = [
    "ContentParser",
    "CSVStorage",
    "SupabaseDB",
    "SupabaseFileStorage",
]
