"""Test SearchManager business logic with Supabase."""

import os
import tempfile
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment
load_dotenv()

from earthquakes_parser import SupabaseDB, SupabaseFileStorage
from earthquakes_parser.search import SearchManager, GoogleSearcher

print("=" * 60)
print("Test SearchManager Business Logic")
print("=" * 60)

# Initialize components
db = SupabaseDB()
searcher = GoogleSearcher(delay=1.0)
search_manager = SearchManager(db=db, searcher=searcher)
file_storage = SupabaseFileStorage(bucket_name="html-files")

print("\n✓ SearchManager initialized")
print("✓ Using SupabaseDB for persistence")
print("✓ Using GoogleSearcher for keyword search")
print("✓ Using SupabaseFileStorage for HTML upload")

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

# Test 2: Download HTML for pending URLs
print("\n" + "=" * 60)
print("Test 2: Download HTML for Pending URLs")
print("=" * 60)

print("\n⏳ Downloading HTML with Selenium...")
download_stats = search_manager.download_html(
    storage=file_storage,
    fetch_with="selenium",
    limit=5
)

print(f"\n📊 Download Results:")
print(f"   ✓ HTML downloaded: {download_stats['downloaded']}")
print(f"   ✗ Failed downloads: {download_stats['failed']}")

# Test 3: Get statistics
print("\n" + "=" * 60)
print("Test 3: Get Search Statistics")
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

# Test 4: Search from keywords file
print("\n" + "=" * 60)
print("Test 4: Search with Keywords File")
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
print("   2. ✅ Download HTML with modular fetcher (bs4 or selenium)")
print("   3. ✅ Get comprehensive statistics")
print("   4. ✅ Search from keywords file")

print("\n🎯 Business Logic Benefits:")
print("   • Automatic deduplication prevents duplicate URLs")
print("   • Status tracking enables pipeline workflow")
print("   • Statistics provide visibility into data")
print("   • Modular design supports flexible workflows")
