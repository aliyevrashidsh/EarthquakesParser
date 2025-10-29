"""Supabase storage backend for database and file storage."""

import os
from datetime import datetime
from io import StringIO
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import pandas as pd

from earthquakes_parser.storage.base import StorageBackend

if TYPE_CHECKING:
    from supabase import Client  # type: ignore[attr-defined]  # noqa: F401


class SupabaseStorage(StorageBackend):
    """Storage backend using Supabase (PostgreSQL + Storage).

    This backend provides:
    - Database storage for search results and parsed content
    - File storage (S3-compatible) for HTML files
    - Automatic status tracking and deduplication
    """

    def __init__(
        self,
        url: Optional[str] = None,
        key: Optional[str] = None,
        storage_bucket: str = "storage",
    ):
        """Initialize Supabase storage backend.

        Args:
            url: Supabase project URL (defaults to SUPABASE_URL env var).
            key: Supabase service role key (defaults to SUPABASE_KEY env var).
            storage_bucket: Name of the storage bucket for HTML files.

        Raises:
            ImportError: If supabase-py is not installed.
            ValueError: If credentials are not provided.
        """
        try:
            from supabase import create_client  # type: ignore[attr-defined]
        except ImportError:
            raise ImportError(
                "supabase is required for SupabaseStorage. "
                "Install it with: uv pip install supabase"
            )

        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_KEY")

        if not self.url or not self.key:
            raise ValueError(
                "Supabase URL and key must be provided either as arguments "
                "or via SUPABASE_URL and SUPABASE_KEY environment variables"
            )

        self.client: Any = create_client(self.url, self.key)
        self.storage_bucket = storage_bucket

        # Ensure bucket exists
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        """Create storage bucket if it doesn't exist."""
        try:
            buckets = self.client.storage.list_buckets()
            bucket_names = [b.name for b in buckets]

            if self.storage_bucket not in bucket_names:
                self.client.storage.create_bucket(
                    self.storage_bucket, options={"public": False}
                )
        except Exception as e:
            print(f"Warning: Could not verify/create bucket: {e}")

    def save_search_results(
        self,
        results: Union[pd.DataFrame, List[Dict[str, Any]]],
        batch_size: int = 100,
    ) -> List[str]:
        """Save search results to database.

        Args:
            results: DataFrame or list of dicts with columns: query, link, title.
            batch_size: Number of records to insert at once.

        Returns:
            List of inserted record IDs.
        """
        if isinstance(results, pd.DataFrame):
            records = results.to_dict("records")
        else:
            records = results

        inserted_ids = []

        # Process in batches
        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]

            # Prepare data for insertion
            data = []
            for record in batch:
                data.append(
                    {
                        "query": record.get("query", ""),
                        "link": record.get("link", ""),
                        "title": record.get("title"),
                        "site_filter": record.get("site_filter"),
                        "status": "pending",
                    }
                )

            try:
                # Use upsert to avoid duplicates (based on unique link constraint)
                response = (
                    self.client.table("search_results")
                    .upsert(data, on_conflict="link")
                    .execute()
                )

                if response.data:
                    inserted_ids.extend([r["id"] for r in response.data])

            except Exception as e:
                print(f"Error inserting search results batch: {e}")

        return inserted_ids

    def save_html_to_storage(
        self, html_content: str, url: str, search_result_id: str
    ) -> Optional[str]:
        """Save HTML content to Supabase Storage and update search_results.

        Args:
            html_content: Raw HTML content.
            url: Original URL (used for filename generation).
            search_result_id: ID of the search result record.

        Returns:
            Storage path if successful, None otherwise.
        """
        try:
            # Generate unique filename based on search_result_id
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{search_result_id}_{timestamp}.html"
            storage_path = f"html/{filename}"

            # Upload to storage
            html_bytes = html_content.encode("utf-8")
            self.client.storage.from_(self.storage_bucket).upload(
                storage_path, html_bytes, {"content-type": "text/html"}
            )

            # Update search_results with storage path and status
            self.client.table("search_results").update(
                {"html_storage_path": storage_path, "status": "downloaded"}
            ).eq("id", search_result_id).execute()

            return storage_path

        except Exception as e:
            print(f"Error saving HTML to storage: {e}")
            # Mark as failed
            self.client.table("search_results").update({"status": "failed"}).eq(
                "id", search_result_id
            ).execute()
            return None

    def get_html_from_storage(self, storage_path: str) -> Optional[str]:
        """Retrieve HTML content from Supabase Storage.

        Args:
            storage_path: Path to the HTML file in storage.

        Returns:
            HTML content as string, or None if not found.
        """
        try:
            response = self.client.storage.from_(self.storage_bucket).download(
                storage_path
            )
            return str(response.decode("utf-8"))
        except Exception as e:
            print(f"Error retrieving HTML from storage: {e}")
            return None

    def save_parsed_content(
        self, search_result_id: str, raw_text: str, main_text: str
    ) -> Optional[str]:
        """Save parsed content to database.

        Args:
            search_result_id: ID of the related search result.
            raw_text: Raw extracted text.
            main_text: Cleaned/processed text.

        Returns:
            ID of the inserted parsed_content record, or None if failed.
        """
        try:
            data = {
                "search_result_id": search_result_id,
                "raw_text": raw_text,
                "main_text": main_text,
            }

            response = self.client.table("parsed_content").insert(data).execute()

            if response.data:
                parsed_id = str(response.data[0]["id"])

                # Update search_results status
                self.client.table("search_results").update({"status": "parsed"}).eq(
                    "id", search_result_id
                ).execute()

                return parsed_id
            return None

        except Exception as e:
            print(f"Error saving parsed content: {e}")
            # Mark as failed
            self.client.table("search_results").update({"status": "failed"}).eq(
                "id", search_result_id
            ).execute()
            return None

    def get_pending_urls(self, limit: int = 100) -> pd.DataFrame:
        """Get URLs that are pending download/parsing.

        Args:
            limit: Maximum number of records to return.

        Returns:
            DataFrame with pending search results.
        """
        try:
            response = (
                self.client.table("search_results")
                .select("*")
                .eq("status", "pending")
                .limit(limit)
                .execute()
            )

            return pd.DataFrame(response.data)

        except Exception as e:
            print(f"Error fetching pending URLs: {e}")
            return pd.DataFrame()

    def get_downloaded_not_parsed(self, limit: int = 100) -> pd.DataFrame:
        """Get URLs that are downloaded but not yet parsed.

        Args:
            limit: Maximum number of records to return.

        Returns:
            DataFrame with downloaded but unparsed search results.
        """
        try:
            response = (
                self.client.table("search_results")
                .select("*")
                .eq("status", "downloaded")
                .limit(limit)
                .execute()
            )

            return pd.DataFrame(response.data)

        except Exception as e:
            print(f"Error fetching downloaded URLs: {e}")
            return pd.DataFrame()

    def url_exists(self, url: str) -> bool:
        """Check if a URL already exists in the database.

        Args:
            url: URL to check.

        Returns:
            True if URL exists, False otherwise.
        """
        try:
            response = (
                self.client.table("search_results")
                .select("id")
                .eq("link", url)
                .execute()
            )

            return len(response.data) > 0

        except Exception as e:
            print(f"Error checking URL existence: {e}")
            return False

    # StorageBackend interface implementation
    def save(self, data: Any, key: str) -> None:
        """Save data (generic method for compatibility).

        For search results, use save_search_results() instead.
        This method saves to database based on key pattern.

        Args:
            data: Data to save (DataFrame or list of dicts).
            key: Storage identifier (e.g., 'search_results', 'parsed_content').
        """
        if key == "search_results" or key.endswith("_search_results"):
            self.save_search_results(data)
        else:
            # For backward compatibility, save as DataFrame to storage
            if isinstance(data, pd.DataFrame):
                csv_buffer = StringIO()
                data.to_csv(csv_buffer, index=False)
                csv_bytes = csv_buffer.getvalue().encode("utf-8")

                self.client.storage.from_(self.storage_bucket).upload(
                    f"data/{key}.csv", csv_bytes, {"content-type": "text/csv"}
                )
            elif isinstance(data, list):
                df = pd.DataFrame(data)
                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=False)
                csv_bytes = csv_buffer.getvalue().encode("utf-8")

                self.client.storage.from_(self.storage_bucket).upload(
                    f"data/{key}.csv", csv_bytes, {"content-type": "text/csv"}
                )

    def load(self, key: str) -> Any:
        """Load data from storage.

        Args:
            key: Storage identifier.

        Returns:
            Loaded data as DataFrame.
        """
        try:
            response = self.client.storage.from_(self.storage_bucket).download(
                f"data/{key}.csv"
            )
            csv_content = response.decode("utf-8")
            return pd.read_csv(StringIO(csv_content))

        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    def exists(self, key: str) -> bool:
        """Check if key exists in storage.

        Args:
            key: Storage identifier.

        Returns:
            True if exists, False otherwise.
        """
        try:
            files = self.client.storage.from_(self.storage_bucket).list("data/")
            filenames = [f["name"] for f in files]
            return f"{key}.csv" in filenames

        except Exception as e:
            print(f"Error checking existence: {e}")
            return False
