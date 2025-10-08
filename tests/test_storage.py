"""Tests for storage backends."""

import json

import pandas as pd
import pytest

from earthquakes_parser.storage.csv_storage import CSVStorage


class TestCSVStorage:
    """Tests for CSVStorage backend."""

    @pytest.fixture
    def storage(self, tmp_path):
        """Create a CSVStorage instance with temp directory."""
        return CSVStorage(base_path=str(tmp_path))

    def test_storage_initialization(self, storage, tmp_path):
        """Test storage initialization."""
        assert storage.base_path == tmp_path
        assert tmp_path.exists()

    def test_save_and_load_dataframe(self, storage):
        """Test saving and loading a DataFrame."""
        df = pd.DataFrame(
            {
                "query": ["test1", "test2"],
                "link": ["http://example.com/1", "http://example.com/2"],
            }
        )

        storage.save(df, "test.csv")
        loaded_df = storage.load("test.csv")

        pd.testing.assert_frame_equal(df, loaded_df)

    def test_save_and_load_records(self, storage):
        """Test saving and loading list of dicts."""
        records = [
            {"query": "test1", "link": "http://example.com/1"},
            {"query": "test2", "link": "http://example.com/2"},
        ]

        storage.save(records, "test.json")
        loaded_records = storage.load("test.json")

        assert loaded_records == records

    def test_exists(self, storage):
        """Test checking if file exists."""
        df = pd.DataFrame({"col": [1, 2]})
        storage.save(df, "exists.csv")

        assert storage.exists("exists.csv")
        assert not storage.exists("nonexistent.csv")

    def test_append(self, storage):
        """Test appending to existing CSV."""
        df1 = pd.DataFrame({"col": [1, 2]})
        df2 = pd.DataFrame({"col": [3, 4]})

        storage.save(df1, "append_test.csv")
        storage.append(df2, "append_test.csv")

        loaded_df = storage.load("append_test.csv")
        assert len(loaded_df) == 4
        assert loaded_df["col"].tolist() == [1, 2, 3, 4]

    def test_save_unsupported_type(self, storage):
        """Test that saving unsupported type raises error."""
        with pytest.raises(ValueError, match="Unsupported data type"):
            storage.save("string data", "test.csv")
