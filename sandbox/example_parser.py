"""Example: Using the ContentParser."""

import sys
from pathlib import Path

from earthquakes_parser import ContentParser, CSVStorage

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    """Demonstrate parsing earthquake-related web content."""
    # Initialize components
    parser = ContentParser(
        model_name="google/flan-t5-small"
    )  # smaller model for testing
    storage = CSVStorage(base_path="sandbox/data")

    # Load search results (assuming you've run example_search.py first)
    if storage.exists("web_results.csv"):
        df = storage.load("web_results.csv")
        print(f"Loaded {len(df)} URLs to parse")

        # Parse first few URLs
        results = parser.parse_dataframe(df.head(3))

        # Save results
        storage.save_records(results, "parsed_content.json")
        print(f"\nSaved {len(results)} parsed results")
    else:
        print("No search results found. Run example_search.py first.")


if __name__ == "__main__":
    main()
