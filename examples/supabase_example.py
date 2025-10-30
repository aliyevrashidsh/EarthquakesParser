"""Example: Using Supabase utilities for earthquake data management.

This example demonstrates the new architecture where:
- SupabaseDB: Handles database operations (tables)
- SupabaseFileStorage: Handles file operations (storage bucket)
- Business logic in domain modules uses these utilities
"""

import os
from datetime import datetime

from earthquakes_parser import SupabaseDB, SupabaseFileStorage

# Set credentials (or use .env file)
os.environ["SUPABASE_URL"] = "your-project-url"
os.environ["SUPABASE_KEY"] = "your-service-role-key"


def example_search_workflow():
    """Demonstrate search results workflow using SupabaseDB."""
    print("=" * 60)
    print("Example 1: Search Results Workflow")
    print("=" * 60)

    # Initialize DB utility
    db = SupabaseDB()

    # Business logic: Save search results
    search_results = [
        {
            "query": "землетрясение Алматы",
            "link": "https://example.com/article1",
            "title": "Earthquake in Almaty",
            "status": "pending",
        },
        {
            "query": "землетрясение Алматы",
            "link": "https://example.com/article2",
            "title": "Another article",
            "status": "pending",
        },
    ]

    print("\n1. Saving search results to database...")
    ids = db.insert("search_results", search_results)
    print(f"   ✓ Saved {len(ids)} results")

    # Business logic: Get pending URLs for download
    print("\n2. Getting pending URLs...")
    pending = db.select("search_results", filters={"status": "pending"}, limit=10)
    print(f"   ✓ Found {len(pending)} pending results")

    # Business logic: Update status after download
    if ids:
        print("\n3. Updating status to 'downloaded'...")
        db.update("search_results", ids[0], {"status": "downloaded"})
        print("   ✓ Status updated")


def example_parser_workflow():
    """Demonstrate content parsing workflow using both utilities."""
    print("\n" + "=" * 60)
    print("Example 2: Content Parser Workflow")
    print("=" * 60)

    # Initialize utilities
    db = SupabaseDB()
    file_storage = SupabaseFileStorage(bucket_name="storage")

    # Simulate parsed HTML content
    html_content = """<!DOCTYPE html>
<html>
<head><title>Earthquake Article</title></head>
<body>
    <h1>Major Earthquake Hits Region</h1>
    <p>A 6.2 magnitude earthquake struck...</p>
</body>
</html>"""

    # Get a search result ID (for demo, use first pending)
    pending = db.select("search_results", filters={"status": "downloaded"}, limit=1)

    if not pending.empty:
        search_id = pending.iloc[0]["id"]

        # Business logic: Save HTML file
        print("\n1. Uploading HTML to storage...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"html/{search_id}_{timestamp}.html"
        file_storage.upload(file_path, html_content, "text/html")
        print(f"   ✓ Uploaded: {file_path}")

        # Business logic: Save parsed content
        print("\n2. Saving parsed content to database...")
        parsed_data = [
            {
                "search_result_id": search_id,
                "raw_text": "Major Earthquake Hits Region\nA 6.2 magnitude...",
                "main_text": "A 6.2 magnitude earthquake struck the region...",
            }
        ]
        db.insert("parsed_content", parsed_data)
        print("   ✓ Parsed content saved")

        # Business logic: Update search result status
        print("\n3. Updating search result status to 'parsed'...")
        db.update(
            "search_results",
            search_id,
            {"status": "parsed", "html_storage_path": file_path},
        )
        print("   ✓ Status updated")


def example_file_operations():
    """Demonstrate file storage operations."""
    print("\n" + "=" * 60)
    print("Example 3: File Storage Operations")
    print("=" * 60)

    # Initialize file storage
    file_storage = SupabaseFileStorage(bucket_name="storage")

    # Upload file
    content = "Test content for file storage"
    file_path = f"test/example_{datetime.now().timestamp()}.txt"

    print(f"\n1. Uploading file: {file_path}")
    file_storage.upload(file_path, content, "text/plain")
    print("   ✓ File uploaded")

    # Download file
    print("\n2. Downloading file...")
    downloaded = file_storage.download(file_path)
    if downloaded:
        print(f"   ✓ Downloaded: {downloaded[:50]}...")

    # Check existence
    print("\n3. Checking if file exists...")
    exists = file_storage.exists(file_path)
    print(f"   ✓ Exists: {exists}")

    # List files
    print("\n4. Listing files in 'test' folder...")
    files = file_storage.list_files("test")
    print(f"   ✓ Found {len(files)} files")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("SUPABASE UTILITIES EXAMPLES")
    print("=" * 60)

    try:
        example_search_workflow()
        example_parser_workflow()
        example_file_operations()

        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure to:")
        print("1. Set SUPABASE_URL and SUPABASE_KEY environment variables")
        print("2. Create the database schema (see supabase/migrations/)")


if __name__ == "__main__":
    main()
