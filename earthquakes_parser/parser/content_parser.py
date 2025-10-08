"""Content extraction and cleaning using trafilatura and LLM."""

from typing import Dict, List, Optional

import pandas as pd
import requests
import trafilatura
from transformers import pipeline


class ContentParser:
    """Extracts and cleans web content using trafilatura and LLM."""

    def __init__(
        self,
        model_name: str = "google/flan-t5-large",
        block_size: int = 3000,
        timeout: int = 15,
    ):
        """Initialize the content parser.

        Args:
            model_name: HuggingFace model name for text cleaning.
            block_size: Size of text blocks for LLM processing.
            timeout: Request timeout in seconds.
        """
        self.llm = pipeline("text2text-generation", model=model_name)
        self.block_size = block_size
        self.timeout = timeout

    def extract_raw_text(self, url: str) -> str:
        """Extract raw text from a URL using trafilatura.

        Args:
            url: The URL to extract text from.

        Returns:
            Extracted text or error message.
        """
        try:
            html = requests.get(
                url,
                timeout=self.timeout,
                headers={"User-Agent": "Mozilla/5.0"},
            ).text
            text = trafilatura.extract(
                html, include_comments=False, include_tables=False
            )
            return text if text else ""
        except Exception as e:
            return f"Error loading: {e}"

    def clean_with_llm(self, raw_text: str) -> str:
        """Clean text using LLM by processing in blocks.

        Args:
            raw_text: Raw text to clean.

        Returns:
            Cleaned text.
        """
        if not raw_text or raw_text.startswith("Error"):
            return raw_text

        try:
            blocks = [
                raw_text[i : i + self.block_size]
                for i in range(0, len(raw_text), self.block_size)
            ]
            cleaned_blocks = []

            for block in blocks:
                prompt = (
                    "Extract only the main coherent article text from the following. "
                    "Remove ads, menus, navigation, and technical inserts:\n\n"
                    f"{block}"
                )
                out = self.llm(
                    prompt, max_length=1024, clean_up_tokenization_spaces=True
                )
                result = out[0]["generated_text"].strip()

                if len(result.split()) >= 30:
                    cleaned_blocks.append(result)
                else:
                    cleaned_blocks.append(block)

            return "\n\n".join(cleaned_blocks)
        except Exception:
            return raw_text

    def parse_url(self, url: str, query: Optional[str] = None) -> Dict[str, str]:
        """Parse a single URL.

        Args:
            url: URL to parse.
            query: Optional search query associated with this URL.

        Returns:
            Dictionary with query, link, raw_text, and main_text.
        """
        raw_text = self.extract_raw_text(url)
        main_text = self.clean_with_llm(raw_text)

        return {
            "query": query or "",
            "link": url,
            "raw_text": raw_text,
            "main_text": main_text,
        }

    def parse_dataframe(
        self, df: pd.DataFrame, link_column: str = "link", query_column: str = "query"
    ) -> List[Dict[str, str]]:
        """Parse all URLs from a DataFrame.

        Args:
            df: DataFrame containing URLs to parse.
            link_column: Column name containing URLs.
            query_column: Column name containing queries.

        Returns:
            List of dictionaries with parsed content.
        """
        results = []

        for idx, row in df.iterrows():
            url = row.get(link_column, "")
            query = row.get(query_column, "")

            result = self.parse_url(url, query)
            results.append(result)
            print(f"✅ [{idx + 1}/{len(df)}] Processed: {url}")

        return results

    def parse_csv(self, csv_path: str) -> List[Dict[str, str]]:
        """Parse all URLs from a CSV file.

        Args:
            csv_path: Path to CSV file with 'link' and 'query' columns.

        Returns:
            List of dictionaries with parsed content.
        """
        df = pd.read_csv(csv_path)
        return self.parse_dataframe(df)
