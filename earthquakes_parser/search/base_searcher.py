from abc import ABC, abstractmethod
from typing import List, Optional, Iterator
import pandas as pd

from earthquakes_parser.search.search_result import SearchResult


class BaseSearcher(ABC):
    """Abstract base class for all searcher implementations."""

    @abstractmethod
    def search(
        self, query: str, max_results: int = 5, site_filter: Optional[str] = None
    ) -> List[SearchResult]:
        """Perform a search for a single query."""
        pass

    def search_keywords(
        self, keywords: List[str], max_results: int = 5, site_filter: Optional[str] = None
    ) -> Iterator[SearchResult]:
        """Search for multiple keywords."""
        for keyword in keywords:
            results = self.search(keyword, max_results, site_filter)
            for result in results:
                yield result

    def search_to_dataframe(
        self, keywords: List[str], max_results: int = 5, site_filter: Optional[str] = None
    ) -> pd.DataFrame:
        """Search keywords and return results as a DataFrame."""
        results = list(self.search_keywords(keywords, max_results, site_filter))
        return pd.DataFrame([r.to_dict() for r in results])

    @staticmethod
    def load_keywords_from_file(file_path: str) -> List[str]:
        """Load keywords from a text file (one per line)."""
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]