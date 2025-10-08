"""Tests for the KeywordSearcher module."""

import pytest
from unittest.mock import MagicMock, patch

from earthquakes_parser.search.searcher import KeywordSearcher, SearchResult


class TestSearchResult:
    """Tests for SearchResult class."""

    def test_search_result_creation(self):
        """Test creating a SearchResult instance."""
        result = SearchResult(
            query="earthquake",
            link="https://example.com",
            title="Test Article"
        )
        assert result.query == "earthquake"
        assert result.link == "https://example.com"
        assert result.title == "Test Article"

    def test_to_dict(self):
        """Test converting SearchResult to dictionary."""
        result = SearchResult(
            query="earthquake",
            link="https://example.com",
            title="Test"
        )
        data = result.to_dict()
        assert data == {
            "query": "earthquake",
            "link": "https://example.com",
            "title": "Test"
        }


class TestKeywordSearcher:
    """Tests for KeywordSearcher class."""

    @pytest.fixture
    def searcher(self):
        """Create a KeywordSearcher instance."""
        return KeywordSearcher(delay=0.1)

    def test_searcher_initialization(self, searcher):
        """Test searcher initialization."""
        assert searcher.delay == 0.1
        assert searcher.ddgs is not None

    @patch('earthquakes_parser.search.searcher.DDGS')
    def test_search_without_filter(self, mock_ddgs, searcher):
        """Test search without site filter."""
        mock_results = [
            {"href": "https://example.com/1", "title": "Article 1"},
            {"href": "https://example.com/2", "title": "Article 2"},
        ]
        searcher.ddgs.text = MagicMock(return_value=iter(mock_results))

        results = searcher.search("earthquake", max_results=2)

        assert len(results) == 2
        assert results[0].link == "https://example.com/1"
        assert results[0].query == "earthquake"

    @patch('earthquakes_parser.search.searcher.DDGS')
    def test_search_with_site_filter(self, mock_ddgs, searcher):
        """Test search with site filter."""
        mock_results = [
            {"href": "https://instagram.com/post1", "title": "Post 1"},
            {"href": "https://example.com/other", "title": "Other"},
        ]
        searcher.ddgs.text = MagicMock(return_value=iter(mock_results))

        results = searcher.search(
            "earthquake",
            max_results=5,
            site_filter="instagram.com"
        )

        assert len(results) == 1
        assert "instagram.com" in results[0].link

    def test_load_keywords_from_file(self, tmp_path):
        """Test loading keywords from file."""
        keywords_file = tmp_path / "keywords.txt"
        keywords_file.write_text("keyword1\nkeyword2\n\nkeyword3\n")

        keywords = KeywordSearcher.load_keywords_from_file(str(keywords_file))

        assert keywords == ["keyword1", "keyword2", "keyword3"]
