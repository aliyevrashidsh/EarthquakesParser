"""Search module for keyword-based web searches."""

from earthquakes_parser.search.search_manager import SearchManager
from earthquakes_parser.search.searcher import KeywordSearcher

__all__ = ["KeywordSearcher", "SearchManager"]
