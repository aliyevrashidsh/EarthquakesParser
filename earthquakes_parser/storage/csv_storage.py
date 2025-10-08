"""CSV file storage backend."""

import json
import os
from pathlib import Path
from typing import Any, List, Union

import pandas as pd

from earthquakes_parser.storage.base import StorageBackend


class CSVStorage(StorageBackend):
    """Storage backend for CSV files."""

    def __init__(self, base_path: str = "."):
        """Initialize CSV storage.

        Args:
            base_path: Base directory for storing CSV files.
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_path(self, key: str) -> Path:
        """Get full path for a key.

        Args:
            key: Storage key (filename).

        Returns:
            Full path to the file.
        """
        return self.base_path / key

    def save(self, data: Any, key: str) -> None:
        """Save data to a CSV or JSON file.

        Args:
            data: Data to save (DataFrame or list of dicts).
            key: Filename to save to.
        """
        path = self._get_path(key)

        if isinstance(data, pd.DataFrame):
            data.to_csv(path, index=False)
        elif isinstance(data, list):
            if key.endswith(".json"):
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                df = pd.DataFrame(data)
                df.to_csv(path, index=False)
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

    def load(self, key: str) -> Union[pd.DataFrame, List[dict]]:
        """Load data from a CSV or JSON file.

        Args:
            key: Filename to load from.

        Returns:
            Loaded DataFrame or list of dicts.
        """
        path = self._get_path(key)

        if key.endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return pd.read_csv(path)

    def exists(self, key: str) -> bool:
        """Check if file exists.

        Args:
            key: Filename to check.

        Returns:
            True if file exists.
        """
        return self._get_path(key).exists()

    def append(self, data: pd.DataFrame, key: str) -> None:
        """Append data to an existing CSV file.

        Args:
            data: DataFrame to append.
            key: Filename to append to.
        """
        path = self._get_path(key)

        if path.exists():
            existing_df = pd.read_csv(path)
            combined_df = pd.concat([existing_df, data], ignore_index=True)
            combined_df.to_csv(path, index=False)
        else:
            data.to_csv(path, index=False)
