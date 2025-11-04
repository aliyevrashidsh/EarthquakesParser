"""
EarthquakesParser - A library for searching and parsing earthquakes.

This library provides tools for earthquake-related content search and parsing.
"""

__version__ = "0.1.0"

from earthquakes_parser.search.search_manager import SearchManager
from earthquakes_parser.search.searcher import KeywordSearcher
from earthquakes_parser.storage.csv_storage import CSVStorage

# Optional Supabase imports - don't fail if dependencies not installed
try:
    from earthquakes_parser.storage.supabase import SupabaseDB, SupabaseFileStorage

    __all__ = [
        "KeywordSearcher",
        "SearchManager",
        "CSVStorage",
        "SupabaseDB",
        "SupabaseFileStorage",
    ]
except ImportError:
    __all__ = [
        "KeywordSearcher",
        "SearchManager",
        "CSVStorage",
    ]
