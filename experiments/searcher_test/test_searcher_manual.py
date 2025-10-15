"""Manual test script for KeywordSearcher.

This script allows you to manually test the KeywordSearcher functionality
with custom keywords and see the results in real-time.
"""

import sys
from pathlib import Path

from earthquakes_parser import CSVStorage, KeywordSearcher

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def test_basic_search():
    """Test basic search functionality with a single keyword."""
    print("=" * 60)
    print("TEST 1: Basic Search")
    print("=" * 60)

    searcher = KeywordSearcher(delay=1.0)
    keyword = "землетрясение"

    print(f"\nSearching for: {keyword}")
    results = searcher.search(keyword, max_results=3)

    print(f"\nFound {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.title}")
        print(f"   URL: {result.link}")


def test_multiple_keywords():
    """Test searching with multiple keywords."""
    print("\n" + "=" * 60)
    print("TEST 2: Multiple Keywords Search")
    print("=" * 60)

    searcher = KeywordSearcher(delay=1.0)
    keywords = ["землетрясение", "магнитуда", "эпицентр"]

    print(f"\nSearching for {len(keywords)} keywords: {', '.join(keywords)}")
    print("This may take a moment...\n")

    results = list(searcher.search_keywords(keywords, max_results=2))

    print(f"\nTotal results: {len(results)}")
    for keyword in keywords:
        keyword_results = [r for r in results if r.query == keyword]
        print(f"  - {keyword}: {len(keyword_results)} results")


def test_site_filter():
    """Test searching with site filter (Instagram)."""
    print("\n" + "=" * 60)
    print("TEST 3: Site Filter (Instagram)")
    print("=" * 60)

    searcher = KeywordSearcher(delay=1.0)
    keyword = "землетрясение"

    print(f"\nSearching for '{keyword}' on Instagram only...")
    results = searcher.search(keyword, max_results=3, site_filter="instagram.com")

    print(f"\nFound {len(results)} Instagram results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.title}")
        print(f"   URL: {result.link}")


def test_dataframe_export():
    """Test exporting results to DataFrame and CSV."""
    print("\n" + "=" * 60)
    print("TEST 4: Export to DataFrame/CSV")
    print("=" * 60)

    searcher = KeywordSearcher(delay=1.0)
    storage = CSVStorage(base_path="experiments/searcher_test/data")

    keywords = ["землетрясение", "сейсмическая активность"]

    print("\nSearching and exporting results...")
    df = searcher.search_to_dataframe(keywords, max_results=2)

    print(f"\nDataFrame shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst few rows:")
    print(df.head())

    # Save to CSV
    output_file = "test_results.csv"
    storage.save(df, output_file)
    print(f"\n✓ Results saved to: experiments/searcher_test/data/{output_file}")


def test_custom_keywords():
    """Interactive test - search for user-provided keywords."""
    print("\n" + "=" * 60)
    print("TEST 5: Custom Keywords (Interactive)")
    print("=" * 60)

    print("\nEnter keywords to search (comma-separated):")
    print("Example: землетрясение, магнитуда, сейсмолог")
    user_input = input("\nKeywords: ").strip()

    if not user_input:
        print("No keywords provided, skipping test.")
        return

    keywords = [k.strip() for k in user_input.split(",") if k.strip()]

    print(f"\nSearching for: {', '.join(keywords)}")
    searcher = KeywordSearcher(delay=1.0)

    results = list(searcher.search_keywords(keywords, max_results=3))

    print(f"\nFound {len(results)} total results:")
    for keyword in keywords:
        keyword_results = [r for r in results if r.query == keyword]
        print(f"\n--- {keyword} ({len(keyword_results)} results) ---")
        for i, result in enumerate(keyword_results, 1):
            print(f"{i}. {result.title[:60]}...")
            print(f"   {result.link}")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("KEYWORD SEARCHER MANUAL TESTING")
    print("=" * 60)
    print("\nThis script will test the KeywordSearcher functionality.")
    print("Each test will make real web searches, so it may take time.")

    # Run automated tests
    test_basic_search()
    test_multiple_keywords()
    test_site_filter()
    test_dataframe_export()

    # Ask if user wants to run interactive test
    print("\n" + "=" * 60)
    response = (
        input("\nWould you like to test with custom keywords? (y/n): ").strip().lower()
    )
    if response == "y":
        test_custom_keywords()

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)
    print("\nCheck experiments/searcher_test/data/ for exported CSV files.")


if __name__ == "__main__":
    main()
