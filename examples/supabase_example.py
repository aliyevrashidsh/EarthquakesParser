"""
Complete example of using Supabase storage for fake detection project.

This script demonstrates the full pipeline:
1. Search for keywords
2. Save results to Supabase database
3. Download HTML and store in Supabase Storage
4. Parse HTML content
5. Save parsed content to database

Setup:
1. Install dependencies: uv pip install -e ".[supabase]"
2. Set environment variables:
   export SUPABASE_URL="https://your-project.supabase.co"
   export SUPABASE_KEY="your-service-role-key"
3. Apply database migration (see docs/SUPABASE_USAGE.md)
4. Run: python examples/supabase_example.py
"""

import requests

from earthquakes_parser import ContentParser, KeywordSearcher, SupabaseStorage


def main():
    """Run the complete fake detection pipeline with Supabase."""
    print("=" * 60)
    print("Fake Detection Pipeline with Supabase")
    print("=" * 60)

    # Initialize components
    print("\n[1/5] Initializing components...")
    searcher = KeywordSearcher(delay=1.0)
    parser = ContentParser(model_name="google/flan-t5-large")
    storage = SupabaseStorage()
    print("✓ Components initialized")

    # Load keywords
    print("\n[2/5] Loading keywords...")
    try:
        keywords = KeywordSearcher.load_keywords_from_file("config/keywords.txt")
        print(f"✓ Loaded {len(keywords)} keywords")
    except FileNotFoundError:
        print("⚠ keywords.txt not found, using sample keywords")
        keywords = ["землетрясение", "магнитуда", "эпицентр"]

    # Step 1: Search and save results to database
    print("\n[3/5] Searching and saving to database...")
    print(f"  Searching for {len(keywords)} keywords...")

    results_df = searcher.search_to_dataframe(
        keywords[:3], max_results=5, site_filter="instagram.com"  # Limit for demo
    )

    print(f"  Found {len(results_df)} search results")

    if len(results_df) > 0:
        inserted_ids = storage.save_search_results(results_df)
        print(f"✓ Saved {len(inserted_ids)} results to database")

        # Show sample of what was saved
        print("\n  Sample results:")
        for _, row in results_df.head(3).iterrows():
            print(f"    - {row['title'][:50]}...")
            print(f"      {row['link']}")

    # Step 2: Download HTML for pending URLs
    print("\n[4/5] Downloading HTML files...")
    pending_df = storage.get_pending_urls(limit=5)  # Limit for demo

    print(f"  Found {len(pending_df)} pending URLs to download")

    downloaded_count = 0
    for _, row in pending_df.iterrows():
        try:
            print(f"  Downloading: {row['link'][:60]}...")

            response = requests.get(
                row["link"], timeout=15, headers={"User-Agent": "Mozilla/5.0"}
            )

            storage_path = storage.save_html_to_storage(
                response.text, row["link"], row["id"]
            )

            if storage_path:
                print(f"  ✓ Saved to: {storage_path}")
                downloaded_count += 1
            else:
                print("  ✗ Failed to save")

        except Exception as e:
            print(f"  ✗ Error: {str(e)[:100]}")

    print(f"\n✓ Downloaded {downloaded_count} HTML files")

    # Step 3: Parse downloaded HTML
    print("\n[5/5] Parsing HTML content...")
    downloaded_df = storage.get_downloaded_not_parsed(limit=3)  # Limit for demo

    print(f"  Found {len(downloaded_df)} downloaded files to parse")

    parsed_count = 0
    for _, row in downloaded_df.iterrows():
        try:
            print(f"  Parsing: {row['link'][:60]}...")

            # Retrieve HTML from storage
            html_content = storage.get_html_from_storage(row["html_storage_path"])

            if html_content:
                # Parse using ContentParser
                result = parser.parse_url(row["link"], row["query"])

                # Save parsed content
                parsed_id = storage.save_parsed_content(
                    row["id"], result["raw_text"], result["main_text"]
                )

                if parsed_id:
                    text_preview = result["main_text"][:100].replace("\n", " ")
                    print(f"  ✓ Parsed: {text_preview}...")
                    parsed_count += 1
                else:
                    print("  ✗ Failed to save parsed content")
            else:
                print("  ✗ Could not retrieve HTML")

        except Exception as e:
            print(f"  ✗ Error: {str(e)[:100]}")

    print(f"\n✓ Parsed {parsed_count} HTML files")

    # Summary
    print("\n" + "=" * 60)
    print("Pipeline Summary")
    print("=" * 60)
    saved_count = len(inserted_ids) if "inserted_ids" in locals() else 0
    print(f"Search results saved: {saved_count}")
    print(f"HTML files downloaded: {downloaded_count}")
    print(f"Files parsed: {parsed_count}")
    print("\nNext steps:")
    print("1. Check Supabase Dashboard to see your data")
    print("2. View search_results table for URLs")
    print("3. View parsed_content table for extracted text")
    print("4. Implement fake detection analysis on parsed content")
    print("=" * 60)


def demo_deduplication():
    """Demonstrate URL deduplication feature."""
    print("\n" + "=" * 60)
    print("Deduplication Demo")
    print("=" * 60)

    storage = SupabaseStorage()

    test_url = "https://example.com/test-article"

    if storage.url_exists(test_url):
        print(f"✓ URL already in database: {test_url}")
        print("  Skipping re-download...")
    else:
        print(f"✗ URL not found: {test_url}")
        print("  Would proceed with download...")


def demo_status_tracking():
    """Demonstrate status tracking feature."""
    print("\n" + "=" * 60)
    print("Status Tracking Demo")
    print("=" * 60)

    _ = SupabaseStorage()

    # Get counts by status
    statuses = ["pending", "downloaded", "parsed", "analyzed", "failed"]

    for status in statuses:
        # This would require a custom query - simplified for demo
        print(f"  {status}: (query database to get count)")


if __name__ == "__main__":
    try:
        main()

        # Optional demos
        # demo_deduplication()
        # demo_status_tracking()

    except ImportError as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease install Supabase dependencies:")
        print("  uv pip install -e '.[supabase]'")

    except ValueError as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease set environment variables:")
        print('  export SUPABASE_URL="https://your-project.supabase.co"')
        print('  export SUPABASE_KEY="your-service-role-key"')

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
