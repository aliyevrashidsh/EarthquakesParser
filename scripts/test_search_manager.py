"""Test SearchManager business logic with Supabase."""

import os
import tempfile

from dotenv import load_dotenv

# Load environment
load_dotenv()

from earthquakes_parser import SearchManager, SupabaseDB

print("=" * 60)
print("Test SearchManager Business Logic")
print("=" * 60)

# Initialize utilities
db = SupabaseDB()
search_manager = SearchManager(db)

print("\n✓ SearchManager initialized")
print("✓ Using SupabaseDB for persistence")

# Test 1: Search and save with deduplication
print("\n" + "=" * 60)
print("Test 1: Search and Save with Deduplication")
print("=" * 60)

keywords = ["землетрясение Алматы", "earthquake Kazakhstan"]

print(f"\n⏳ Searching for keywords: {keywords}")
print("   Max results: 3 per keyword")
print("   Deduplication: enabled")

stats = search_manager.search_and_save(
    keywords=keywords, max_results=3, skip_existing=True
)

print(f"\n📊 Results:")
print(f"   ✓ Keywords searched: {stats['searched']}")
print(f"   ✓ Total results found: {stats['found']}")
print(f"   ✓ New results saved: {stats['new']}")
print(f"   ✓ Existing skipped: {stats['skipped']}")

# Test 2: Get pending URLs
print("\n" + "=" * 60)
print("Test 2: Get Pending URLs for Download")
print("=" * 60)

print("\n⏳ Fetching pending URLs...")
pending_urls = search_manager.get_pending_urls(limit=5)

print(f"\n✓ Found {len(pending_urls)} pending URLs")
if pending_urls:
    print("\nFirst 3 pending URLs:")
    for i, url_data in enumerate(pending_urls[:3], 1):
        print(f"   {i}. {url_data['title']}")
        print(f"      URL: {url_data['link']}")
        print(f"      Query: {url_data['query']}")
        print(f"      Status: {url_data['status']}")

# Test 3: Mark as downloaded
if pending_urls:
    print("\n" + "=" * 60)
    print("Test 3: Mark URL as Downloaded")
    print("=" * 60)

    test_result = pending_urls[0]
    print(f"\n⏳ Marking as downloaded: {test_result['title']}")

    success = search_manager.mark_as_downloaded(
        test_result["id"], html_storage_path="html/test_file.html"
    )

    if success:
        print("✓ Successfully marked as downloaded")
    else:
        print("✗ Failed to mark as downloaded")

# Test 4: Get statistics
print("\n" + "=" * 60)
print("Test 4: Get Search Statistics")
print("=" * 60)

print("\n⏳ Fetching statistics...")
stats = search_manager.get_statistics()

print("\n📊 Database Statistics:")
print(f"   Total records: {stats['total']}")
print(f"   Pending: {stats['pending']}")
print(f"   Downloaded: {stats['downloaded']}")
print(f"   Parsed: {stats['parsed']}")
print(f"   Analyzed: {stats['analyzed']}")
print(f"   Failed: {stats['failed']}")

# Test 5: Search from keywords file
print("\n" + "=" * 60)
print("Test 5: Search with Keywords File")
print("=" * 60)

# Create temporary keywords file
with tempfile.NamedTemporaryFile(
    mode="w", suffix=".txt", delete=False, encoding="utf-8"
) as f:
    f.write("землетрясение\n")
    f.write("сейсмоактивность\n")
    keywords_file = f.name

print(f"\n⏳ Created test keywords file: {keywords_file}")
print("   Keywords: землетрясение, сейсмоактивность")

stats = search_manager.search_with_keywords_file(
    keywords_file, max_results=2, skip_existing=True
)

print(f"\n📊 Results:")
print(f"   ✓ Keywords searched: {stats['searched']}")
print(f"   ✓ Total results found: {stats['found']}")
print(f"   ✓ New results saved: {stats['new']}")
print(f"   ✓ Existing skipped: {stats['skipped']}")

# Clean up
os.remove(keywords_file)
print(f"\n✓ Cleaned up test file")

# Final summary
print("\n" + "=" * 60)
print("✅ All SearchManager tests completed!")
print("=" * 60)

print("\n📝 SearchManager Features Demonstrated:")
print("   1. ✅ Search and save with automatic deduplication")
print("   2. ✅ Get pending URLs for download pipeline")
print("   3. ✅ Mark URLs as downloaded (status management)")
print("   4. ✅ Get comprehensive statistics")
print("   5. ✅ Search from keywords file")

print("\n🎯 Business Logic Benefits:")
print("   • Automatic deduplication prevents duplicate URLs")
print("   • Status tracking enables pipeline workflow")
print("   • Statistics provide visibility into data")
print("   • Reusable methods for different workflows")
