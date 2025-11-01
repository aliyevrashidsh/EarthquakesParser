"""DuckDuckGo-based searcher implementation."""

import time
from typing import List, Optional
from ddgs import DDGS

from earthquakes_parser.search.base_searcher import BaseSearcher
from earthquakes_parser.search.search_result import SearchResult


class DDGSearcher(BaseSearcher):
    """DuckDuckGo searcher using ddgs library."""

    def __init__(self, delay: float = 1.0):
        self.ddgs = DDGS()
        self.delay = delay

    def search(
        self, query: str, max_results: int = 5, site_filter: Optional[str] = None
    ) -> List[SearchResult]:
        results = []
        search_query = f"site:{site_filter} {query}" if site_filter else query

        try:
            for result in self.ddgs.text(search_query):
                link = result.get("href", "")
                title = result.get("title", "")

                if site_filter and site_filter not in link:
                    continue

                results.append(SearchResult(query=query, link=link, title=title))
                if len(results) >= max_results:
                    break

        except Exception as e:
            print(f"DDG search error for '{query}': {e}")

        time.sleep(self.delay)
        return results
