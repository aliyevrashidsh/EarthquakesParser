"""Base storage backend interface."""

from abc import ABC, abstractmethod
from typing import Any, List

import pandas as pd


class StorageBackend(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    def save(self, data: Any, key: str) -> None:
        """Save data to storage.

        Args:
            data: Data to save (DataFrame, dict, list, etc.).
            key: Storage key/path identifier.
        """
        pass

    @abstractmethod
    def load(self, key: str) -> Any:
        """Load data from storage.

        Args:
            key: Storage key/path identifier.

        Returns:
            Loaded data.
        """
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists in storage.

        Args:
            key: Storage key/path identifier.

        Returns:
            True if exists, False otherwise.
        """
        pass

    def save_dataframe(self, df: pd.DataFrame, key: str) -> None:
        """Save a DataFrame.

        Args:
            df: DataFrame to save.
            key: Storage key/path identifier.
        """
        self.save(df, key)

    def save_records(self, records: List[dict], key: str) -> None:
        """Save a list of records.

        Args:
            records: List of dictionaries to save.
            key: Storage key/path identifier.
        """
        self.save(records, key)
