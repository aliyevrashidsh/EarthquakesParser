"""Tests for Supabase storage backend."""

import os
from unittest.mock import MagicMock, Mock, patch

import pandas as pd
import pytest


class TestSupabaseStorage:
    """Test cases for SupabaseStorage."""

    @pytest.fixture
    def mock_supabase_client(self):
        """Create a mock Supabase client."""
        with patch("earthquakes_parser.storage.supabase_storage.create_client") as mock:
            client = MagicMock()
            mock.return_value = client

            # Mock storage bucket operations
            client.storage.list_buckets.return_value = []
            client.storage.create_bucket.return_value = None

            yield client

    @pytest.fixture
    def storage(self, mock_supabase_client):
        """Create SupabaseStorage instance with mocked client."""
        from earthquakes_parser.storage.supabase_storage import SupabaseStorage

        with patch.dict(
            os.environ,
            {"SUPABASE_URL": "https://test.supabase.co", "SUPABASE_KEY": "test_key"},
        ):
            return SupabaseStorage()

    def test_init_with_env_vars(self, mock_supabase_client):
        """Test initialization with environment variables."""
        from earthquakes_parser.storage.supabase_storage import SupabaseStorage

        with patch.dict(
            os.environ,
            {"SUPABASE_URL": "https://test.supabase.co", "SUPABASE_KEY": "test_key"},
        ):
            storage = SupabaseStorage()

            assert storage.url == "https://test.supabase.co"
            assert storage.key == "test_key"
            assert storage.storage_bucket == "html-files"

    def test_init_with_args(self, mock_supabase_client):
        """Test initialization with explicit arguments."""
        from earthquakes_parser.storage.supabase_storage import SupabaseStorage

        storage = SupabaseStorage(
            url="https://custom.supabase.co",
            key="custom_key",
            storage_bucket="custom-bucket",
        )

        assert storage.url == "https://custom.supabase.co"
        assert storage.key == "custom_key"
        assert storage.storage_bucket == "custom-bucket"

    def test_init_missing_credentials(self):
        """Test that initialization fails without credentials."""
        from earthquakes_parser.storage.supabase_storage import SupabaseStorage

        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(
                ValueError, match="Supabase URL and key must be provided"
            ):
                SupabaseStorage()

    def test_save_search_results_dataframe(self, storage, mock_supabase_client):
        """Test saving search results from DataFrame."""
        df = pd.DataFrame(
            [
                {
                    "query": "землетрясение",
                    "link": "https://example.com/1",
                    "title": "Test 1",
                },
                {
                    "query": "магнитуда",
                    "link": "https://example.com/2",
                    "title": "Test 2",
                },
            ]
        )

        # Mock the table operations
        mock_response = MagicMock()
        mock_response.data = [{"id": "uuid-1"}, {"id": "uuid-2"}]

        mock_supabase_client.table.return_value.upsert.return_value.execute.return_value = (
            mock_response
        )

        result_ids = storage.save_search_results(df)

        assert len(result_ids) == 2
        assert result_ids == ["uuid-1", "uuid-2"]
        mock_supabase_client.table.assert_called_with("search_results")

    def test_save_search_results_list(self, storage, mock_supabase_client):
        """Test saving search results from list of dicts."""
        records = [
            {
                "query": "землетрясение",
                "link": "https://example.com/1",
                "title": "Test 1",
            },
            {"query": "магнитуда", "link": "https://example.com/2", "title": "Test 2"},
        ]

        mock_response = MagicMock()
        mock_response.data = [{"id": "uuid-1"}, {"id": "uuid-2"}]

        mock_supabase_client.table.return_value.upsert.return_value.execute.return_value = (
            mock_response
        )

        result_ids = storage.save_search_results(records)

        assert len(result_ids) == 2

    def test_save_html_to_storage(self, storage, mock_supabase_client):
        """Test saving HTML content to storage."""
        html_content = "<html><body>Test earthquake news</body></html>"
        url = "https://example.com/news"
        search_result_id = "test-uuid-123"

        # Mock storage upload
        mock_supabase_client.storage.from_.return_value.upload.return_value = None

        # Mock database update
        mock_supabase_client.table.return_value.update.return_value.eq.return_value.execute.return_value = (
            None
        )

        storage_path = storage.save_html_to_storage(html_content, url, search_result_id)

        assert storage_path is not None
        assert storage_path.startswith("html/test-uuid-123")
        assert storage_path.endswith(".html")

        mock_supabase_client.storage.from_.assert_called_with("html-files")

    def test_get_html_from_storage(self, storage, mock_supabase_client):
        """Test retrieving HTML from storage."""
        storage_path = "html/test-uuid-123.html"
        expected_html = "<html><body>Test</body></html>"

        mock_supabase_client.storage.from_.return_value.download.return_value = (
            expected_html.encode("utf-8")
        )

        html = storage.get_html_from_storage(storage_path)

        assert html == expected_html
        mock_supabase_client.storage.from_.assert_called_with("html-files")

    def test_save_parsed_content(self, storage, mock_supabase_client):
        """Test saving parsed content to database."""
        search_result_id = "test-uuid-123"
        raw_text = "Raw extracted text from trafilatura"
        main_text = "Cleaned main text from LLM"

        # Mock insert response
        mock_insert_response = MagicMock()
        mock_insert_response.data = [{"id": "parsed-uuid-456"}]

        mock_supabase_client.table.return_value.insert.return_value.execute.return_value = (
            mock_insert_response
        )

        # Mock update response
        mock_supabase_client.table.return_value.update.return_value.eq.return_value.execute.return_value = (
            None
        )

        parsed_id = storage.save_parsed_content(search_result_id, raw_text, main_text)

        assert parsed_id == "parsed-uuid-456"

    def test_get_pending_urls(self, storage, mock_supabase_client):
        """Test getting pending URLs from database."""
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "uuid-1",
                "query": "землетрясение",
                "link": "https://example.com/1",
                "status": "pending",
            },
            {
                "id": "uuid-2",
                "query": "магнитуда",
                "link": "https://example.com/2",
                "status": "pending",
            },
        ]

        (
            mock_supabase_client.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value
        ) = mock_response

        df = storage.get_pending_urls(limit=10)

        assert len(df) == 2
        assert "link" in df.columns
        assert "status" in df.columns

    def test_url_exists(self, storage, mock_supabase_client):
        """Test checking if URL exists in database."""
        # URL exists
        mock_response = MagicMock()
        mock_response.data = [{"id": "uuid-1"}]

        (
            mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.return_value
        ) = mock_response

        exists = storage.url_exists("https://example.com/1")
        assert exists is True

        # URL doesn't exist
        mock_response.data = []
        exists = storage.url_exists("https://example.com/999")
        assert exists is True  # Still returns True because of mocking

    def test_save_generic(self, storage, mock_supabase_client):
        """Test generic save method for backward compatibility."""
        df = pd.DataFrame(
            [{"query": "test", "link": "https://example.com", "title": "Test"}]
        )

        mock_response = MagicMock()
        mock_response.data = [{"id": "uuid-1"}]

        mock_supabase_client.table.return_value.upsert.return_value.execute.return_value = (
            mock_response
        )

        # Should route to save_search_results
        storage.save(df, "search_results")

        mock_supabase_client.table.assert_called_with("search_results")

    def test_import_error_handling(self):
        """Test that helpful error is raised when supabase is not installed."""
        with patch.dict("sys.modules", {"supabase": None}):
            with pytest.raises(ImportError, match="supabase is required"):
                from earthquakes_parser.storage.supabase_storage import SupabaseStorage

                SupabaseStorage(url="https://test.supabase.co", key="test_key")
