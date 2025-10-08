"""S3 storage backend (future implementation)."""

import json
from io import BytesIO, StringIO
from typing import Any, List, Union

import pandas as pd

from earthquakes_parser.storage.base import StorageBackend


class S3Storage(StorageBackend):
    """Storage backend for AWS S3 (requires boto3)."""

    def __init__(self, bucket_name: str, prefix: str = ""):
        """Initialize S3 storage.

        Args:
            bucket_name: S3 bucket name.
            prefix: Optional prefix for all keys.

        Raises:
            ImportError: If boto3 is not installed.
        """
        try:
            import boto3
        except ImportError:
            raise ImportError(
                "boto3 is required for S3Storage. Install with: pip install boto3"
            )

        self.s3_client = boto3.client("s3")
        self.bucket_name = bucket_name
        self.prefix = prefix

    def _get_key(self, key: str) -> str:
        """Get full S3 key with prefix.

        Args:
            key: Storage key.

        Returns:
            Full S3 key with prefix.
        """
        if self.prefix:
            return f"{self.prefix}/{key}"
        return key

    def save(self, data: Any, key: str) -> None:
        """Save data to S3.

        Args:
            data: Data to save (DataFrame or list of dicts).
            key: S3 key to save to.
        """
        s3_key = self._get_key(key)

        if isinstance(data, pd.DataFrame):
            csv_buffer = StringIO()
            data.to_csv(csv_buffer, index=False)
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=csv_buffer.getvalue().encode("utf-8"),
            )
        elif isinstance(data, list):
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=json_str.encode("utf-8"),
            )
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

    def load(self, key: str) -> Union[pd.DataFrame, List[dict]]:
        """Load data from S3.

        Args:
            key: S3 key to load from.

        Returns:
            Loaded DataFrame or list of dicts.
        """
        s3_key = self._get_key(key)
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
        content = response["Body"].read()

        if key.endswith(".json"):
            return json.loads(content.decode("utf-8"))
        else:
            return pd.read_csv(BytesIO(content))

    def exists(self, key: str) -> bool:
        """Check if key exists in S3.

        Args:
            key: S3 key to check.

        Returns:
            True if key exists.
        """
        s3_key = self._get_key(key)
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except Exception:
            return False
