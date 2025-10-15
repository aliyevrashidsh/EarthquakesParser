"""Keyword-based web search functionality."""

import time
from typing import Iterator, List, Optional

import pandas as pd
from ddgs import DDGS


class SearchResult:
    """Represents a single search result."""

    def __init__(self, query: str, link: str, title: Optional[str] = None):
        """Initialize a search result.

        Args:
            query: The search query used.
            link: URL of the search result.
            title: Title of the search result page.
        """
        self.query = query
        self.link = link
        self.title = title

    def to_dict(self) -> dict:
        """Convert to dictionary format."""
        return {"query": self.query, "link": self.link, "title": self.title}


class KeywordSearcher:
    """Performs keyword-based searches using DuckDuckGo."""

    def __init__(self, delay: float = 1.0):
        """Initialize the searcher.

        Args:
            delay: Delay between searches in seconds to avoid rate limiting.
        """
        self.ddgs = DDGS()
        self.delay = delay

    def search(
        self,
        query: str,
        max_results: int = 5,
        site_filter: Optional[str] = None,
    ) -> List[SearchResult]:
        """Perform a search for a given query.

        Args:
            query: The search query.
            max_results: Maximum number of results to return.
            site_filter: Optional site filter (e.g., "instagram.com").

        Returns:
            List of SearchResult objects.
        """
        if site_filter:
            search_query = f"site:{site_filter} {query}"
        else:
            search_query = query

        results = []
        try:
            search_results = self.ddgs.text(search_query)
            count = 0

            for result in search_results:
                link = result.get("href", "")
                title = result.get("title", "")

                if site_filter and site_filter not in link:
                    continue

                results.append(SearchResult(query=query, link=link, title=title))
                count += 1

                if count >= max_results:
                    break

        except Exception as e:
            print(f"Error searching for '{query}': {e}")

        return results

    def search_keywords(
        self,
        keywords: List[str],
        max_results: int = 5,
        site_filter: Optional[str] = None,
    ) -> Iterator[SearchResult]:
        """Search for multiple keywords.

        Args:
            keywords: List of keywords to search for.
            max_results: Maximum results per keyword.
            site_filter: Optional site filter.

        Yields:
            SearchResult objects for each keyword.
        """
        for keyword in keywords:
            results = self.search(keyword, max_results, site_filter)
            for result in results:
                yield result

            if self.delay > 0:
                time.sleep(self.delay)

    def search_to_dataframe(
        self,
        keywords: List[str],
        max_results: int = 5,
        site_filter: Optional[str] = None,
    ) -> pd.DataFrame:
        """Search keywords and return results as a DataFrame.

        Args:
            keywords: List of keywords to search for.
            max_results: Maximum results per keyword.
            site_filter: Optional site filter.

        Returns:
            DataFrame with columns: query, link, title.
        """
        results = list(self.search_keywords(keywords, max_results, site_filter))
        return pd.DataFrame([r.to_dict() for r in results])

    @staticmethod
    def load_keywords_from_file(file_path: str) -> List[str]:
        """Load keywords from a text file (one per line).

        Args:
            file_path: Path to the keywords file.

        Returns:
            List of keywords.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
