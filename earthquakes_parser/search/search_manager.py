"""Business logic for managing earthquake search operations with Supabase storage."""

from typing import List, Optional

from earthquakes_parser.search.searcher import KeywordSearcher, SearchResult
from earthquakes_parser.storage.supabase import SupabaseDB


class SearchManager:
    """Manages earthquake search operations with database persistence.

    This class contains business logic for:
    - Searching for earthquake-related content
    - Saving search results to database with deduplication
    - Managing search result status workflow
    """

    def __init__(self, db: SupabaseDB, searcher: Optional[KeywordSearcher] = None):
        """Initialize search manager.

        Args:
            db: Supabase database utility for persistence.
            searcher: Optional KeywordSearcher instance. Creates default if None.
        """
        self.db = db
        self.searcher = searcher or KeywordSearcher(delay=1.0)

    def search_and_save(
        self,
        keywords: List[str],
        max_results: int = 5,
        site_filter: Optional[str] = None,
        skip_existing: bool = True,
    ) -> dict:
        """Search for keywords and save results to database.

        Business logic:
        1. Search using KeywordSearcher
        2. Check for duplicates (deduplication)
        3. Save new results with status='pending'
        4. Return statistics

        Args:
            keywords: List of search keywords.
            max_results: Maximum results per keyword.
            site_filter: Optional site filter (e.g., 'instagram.com').
            skip_existing: Skip URLs that already exist in database.

        Returns:
            Dict with statistics: {
                'searched': int,  # Total keywords searched
                'found': int,     # Total results found
                'new': int,       # New results saved
                'skipped': int    # Existing results skipped
            }
        """
        stats = {"searched": 0, "found": 0, "new": 0, "skipped": 0}

        # Collect all search results
        all_results: List[SearchResult] = []
        for keyword in keywords:
            results = self.searcher.search(keyword, max_results, site_filter)
            all_results.extend(results)
            stats["searched"] += 1
            stats["found"] += len(results)

        if not all_results:
            return stats

        # Prepare data for database
        new_results = []
        for result in all_results:
            # Business logic: Check if URL already exists (deduplication)
            if skip_existing and self.db.exists("search_results", "link", result.link):
                stats["skipped"] += 1
                continue

            # Prepare record with initial status
            new_results.append(
                {
                    "query": result.query,
                    "link": result.link,
                    "title": result.title,
                    "status": "pending",  # Initial status
                }
            )

        # Save to database
        if new_results:
            inserted_ids = self.db.insert("search_results", new_results)
            stats["new"] = len(inserted_ids)

        return stats

    def get_pending_urls(self, limit: int = 100) -> List[dict]:
        """Get URLs that need to be downloaded.

        Business logic: Fetch records with status='pending'.

        Args:
            limit: Maximum number of URLs to return.

        Returns:
            List of dicts with keys: id, query, link, title, status.
        """
        df = self.db.select(
            "search_results", filters={"status": "pending"}, limit=limit
        )

        if df.empty:
            return []

        return list(df.to_dict("records"))

    def mark_as_downloaded(self, search_result_id: str, html_storage_path: str) -> bool:
        """Mark a search result as downloaded.

        Business logic: Update status from 'pending' to 'downloaded'.

        Args:
            search_result_id: ID of the search result.
            html_storage_path: Path where HTML was saved in storage.

        Returns:
            True if successful, False otherwise.
        """
        updated = self.db.update(
            "search_results",
            search_result_id,
            {"status": "downloaded", "html_storage_path": html_storage_path},
        )
        return updated is not None

    def mark_as_failed(self, search_result_id: str, error_message: str = "") -> bool:
        """Mark a search result as failed.

        Business logic: Update status to 'failed' with optional error message.

        Args:
            search_result_id: ID of the search result.
            error_message: Optional error message for debugging.

        Returns:
            True if successful, False otherwise.
        """
        # Note: error_message not stored in current schema, but kept for future
        updated = self.db.update(
            "search_results", search_result_id, {"status": "failed"}
        )
        return updated is not None

    def get_statistics(self) -> dict:
        """Get search statistics.

        Business logic: Count records by status.

        Returns:
            Dict with counts by status: {
                'total': int,
                'pending': int,
                'downloaded': int,
                'parsed': int,
                'analyzed': int,
                'failed': int
            }
        """
        stats = {
            "total": 0,
            "pending": 0,
            "downloaded": 0,
            "parsed": 0,
            "analyzed": 0,
            "failed": 0,
        }

        # Get counts for each status
        for status in ["pending", "downloaded", "parsed", "analyzed", "failed"]:
            df = self.db.select(
                "search_results", filters={"status": status}, limit=None
            )
            count = len(df)
            stats[status] = count
            stats["total"] += count

        return stats

    def search_with_keywords_file(
        self,
        keywords_file: str,
        max_results: int = 5,
        site_filter: Optional[str] = None,
        skip_existing: bool = True,
    ) -> dict:
        """Search using keywords from file and save results.

        Business logic wrapper: Load keywords from file and search.

        Args:
            keywords_file: Path to keywords file (one per line).
            max_results: Maximum results per keyword.
            site_filter: Optional site filter.
            skip_existing: Skip existing URLs.

        Returns:
            Statistics dict from search_and_save().
        """
        keywords = KeywordSearcher.load_keywords_from_file(keywords_file)
        return self.search_and_save(keywords, max_results, site_filter, skip_existing)
