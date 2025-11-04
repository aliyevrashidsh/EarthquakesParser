"""Main parser manager orchestrating the parsing workflow."""
import os
from typing import Optional
from urllib.parse import urlparse

from dotenv import load_dotenv
import pandas as pd

from earthquakes_parser.storage.supabase.database import SupabaseDB
from earthquakes_parser.parser.data_extractor import DataExtractor
from earthquakes_parser.parser.models import ParsedContent
from earthquakes_parser.parser.schema_extractor import SchemaExtractor
from earthquakes_parser.parser.schema_manager import SchemaManager


class ParserManager:
    """Orchestrates the parsing workflow for search results."""

    def __init__(
            self,
            db: SupabaseDB,
            openai_base_url: str = "http://192.168.8.22:9999/v1",
            openai_api_key: str = "api-key",
    ):
        """Initialize parser manager.

        Args:
            db: Database instance.
            openai_base_url: Base URL for OpenAI-compatible API.
            openai_api_key: API key for OpenAI.
        """
        load_dotenv()
        self.db = db
        self.schema_manager = SchemaManager(db)
        if openai_base_url:
            self.openai_base_url = openai_base_url
        else:
            self.openai_base_url = os.getenv("OPENAI_BASE_URL")
        if openai_api_key:
            self.openai_api_key = openai_api_key
        else:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")

        if not all([self.openai_base_url, self.openai_api_key]):
            raise ValueError(
                "Missing required environment variables: "
                "openai_base_url, openai_api_key"
            )

        self.schema_extractor = SchemaExtractor(openai_base_url, openai_api_key)
        self.data_extractor = DataExtractor()

        self.search_results_table = "search_results"
        self.parsed_content_table = "parsed_content"

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL.

        Args:
            url: Full URL.

        Returns:
            Domain name (e.g., 'example.com').
        """
        parsed = urlparse(url)
        return parsed.netloc

    def _save_parsed_content(
            self,
            search_result_id: str,
            url: str,
            main_text: list,
            date: Optional[str],
            schema_id: str,
    ) -> Optional[str]:
        """Save parsed content to database.

        Args:
            search_result_id: ID of search result.
            url: URL of the page.
            main_text: Extracted main text.
            date: Extracted date.
            schema_id: Schema ID used for extraction.

        Returns:
            Parsed content ID or None if failed.
        """
        content = ParsedContent(
            search_result_id=search_result_id,
            url=url,
            main_text=main_text,
            date=date,
            schema_id=schema_id,
        )

        try:
            inserted_ids = self.db.insert(
                self.parsed_content_table,
                [content.to_dict()],
                batch_size=1,
            )
            return inserted_ids[0] if inserted_ids else None
        except Exception as e:
            print(f"❌ Error saving parsed content: {e}")
            return None

    def parse_url(
            self,
            url: str,
            title: str,
            search_result_id: str,
            force_reextract: bool = False,
    ) -> bool:
        """Parse a single URL.

        Args:
            url: URL to parse.
            title: Page title.
            search_result_id: ID from search_results table.
            force_reextract: Force schema re-extraction even if exists.

        Returns:
            True if successful, False otherwise.
        """
        domain = self._get_domain(url)
        print(f"\n{'=' * 100}")
        print(f"🌐 Processing: {title}")
        print(f"🔗 URL: {url}")
        print(f"📍 Domain: {domain}")

        # Step 1: Check if schema exists
        schema = self.schema_manager.get_by_domain(domain)

        if not schema or force_reextract:
            print(f"📝 No schema found for {domain}, extracting...")
            schema = self.schema_extractor.extract_schema(url, title, domain)

            if not schema:
                print(f"❌ Failed to extract schema for {domain}")
                return False

            # Save schema
            schema_id = self.schema_manager.save(schema)
            if not schema_id:
                print(f"❌ Failed to save schema for {domain}")
                return False

            schema.id = schema_id
            print(f"✅ Schema saved with ID: {schema_id}")
        else:
            print(f"✅ Using existing schema (ID: {schema.id})")

        # Check if page is valid
        if not schema.is_valid:
            print(f"⚠️ Page is not about earthquakes, skipping...")
            return False

        # Step 2: Fetch HTML and extract data
        html = self.schema_extractor.fetch_html(url)
        if not html:
            print(f"❌ Failed to fetch HTML from {url}")
            return False

        # Extract data
        result = self.data_extractor.extract(html, schema)

        # Step 3: Check if extraction was successful
        if self.data_extractor.validate_extraction(result):
            print(f"⚠️ Extraction failed (both fields empty), re-extracting schema...")

            # Re-extract schema
            schema = self.schema_extractor.extract_schema(url, title, domain)
            if not schema:
                print(f"❌ Failed to re-extract schema")
                return False

            # Save updated schema
            schema_id = self.schema_manager.save(schema)
            if not schema_id:
                print(f"❌ Failed to save re-extracted schema")
                return False

            schema.id = schema_id

            # Try extraction again
            result = self.data_extractor.extract(html, schema)

            if self.data_extractor.validate_extraction(result):
                print(f"❌ Re-extraction also failed, skipping...")
                return False

        # Step 4: Save parsed content
        print(f"📌 Extracted text: {len(result.main_text)} paragraphs")
        print(f"📅 Date: {result.date}")

        content_id = self._save_parsed_content(
            search_result_id=search_result_id,
            url=url,
            main_text=result.main_text,
            date=result.date,
            schema_id=schema.id,
        )

        if content_id:
            print(f"✅ Content saved with ID: {content_id}")
            return True
        else:
            print(f"❌ Failed to save content")
            return False

    def parse_from_dataframe(self, df: pd.DataFrame) -> dict:
        """Parse URLs from DataFrame.

        Args:
            df: DataFrame with columns: id, link, title

        Returns:
            Dictionary with statistics.
        """
        stats = {
            "total": len(df),
            "successful": 0,
            "failed": 0,
            "skipped": 0,
        }

        for _, row in df.iterrows():
            try:
                search_result_id = str(row["id"])
                url = row["link"]
                title = row["title"]

                success = self.parse_url(url, title, search_result_id)

                if success:
                    stats["successful"] += 1
                else:
                    stats["failed"] += 1

            except Exception as e:
                print(f"❌ Error processing row: {e}")
                stats["failed"] += 1

        print(f"\n{'=' * 100}")
        print(f"📊 Parsing complete:")
        print(f"   Total: {stats['total']}")
        print(f"   ✅ Successful: {stats['successful']}")
        print(f"   ❌ Failed: {stats['failed']}")
        print(f"{'=' * 100}")

        return stats

    def parse_all_from_db(
            self,
            limit: Optional[int] = None,
            filters: Optional[dict] = None,
    ) -> dict:
        """Parse all URLs from search_results table.

        Args:
            limit: Maximum number of records to process.
            filters: Additional filters for search_results query.

        Returns:
            Dictionary with statistics.
        """
        print(f"📥 Loading search results from database...")

        df = self.db.select(
            self.search_results_table,
            columns="id,link,title",
            filters=filters,
            limit=limit,
        )

        if df.empty:
            print("⚠️ No search results found in database")
            return {"total": 0, "successful": 0, "failed": 0}

        print(f"✅ Loaded {len(df)} search results")

        return self.parse_from_dataframe(df)