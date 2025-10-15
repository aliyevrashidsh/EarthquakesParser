"""Example: Using the KeywordSearcher."""

import sys
from pathlib import Path

from earthquakes_parser import CSVStorage, KeywordSearcher

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    """Demonstrate searching for earthquake-related keywords."""
    # Initialize components
    searcher = KeywordSearcher(delay=1.0)
    storage = CSVStorage(base_path="sandbox/data")

    # Load keywords from config file
    # keywords = KeywordSearcher.load_keywords_from_file("config/keywords.txt")

    # Or use example keywords for quick testing
    keywords = ["землетрясение", "магнитуда", "эпицентр"]

    # Search Instagram
    print("Searching Instagram...")
    instagram_df = searcher.search_to_dataframe(
        keywords, max_results=3, site_filter="instagram.com"
    )
    storage.save_dataframe(instagram_df, "instagram_results.csv")
    print(f"Saved {len(instagram_df)} Instagram results")

    # Search general web
    print("\nSearching web...")
    web_df = searcher.search_to_dataframe(keywords, max_results=3)
    storage.save_dataframe(web_df, "web_results.csv")
    print(f"Saved {len(web_df)} web results")


if __name__ == "__main__":
    main()
