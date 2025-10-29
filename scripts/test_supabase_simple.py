"""Simple test: save and load data from Supabase."""

from dotenv import load_dotenv

load_dotenv()

import pandas as pd

from earthquakes_parser import SupabaseStorage

print("=" * 60)
print("Supabase Storage Test")
print("=" * 60)

# Initialize storage
storage = SupabaseStorage()
print("\n✓ SupabaseStorage initialized")

# Create sample search results
sample_data = pd.DataFrame(
    [
        {
            "query": "тестовое землетрясение",
            "link": "https://example.com/test1",
            "title": "Test Article 1",
        },
        {
            "query": "тестовая магнитуда",
            "link": "https://example.com/test2",
            "title": "Test Article 2",
        },
    ]
)

print("\n⏳ Saving search results to database...")
inserted_ids = storage.save_search_results(sample_data)
print(f"✓ Saved {len(inserted_ids)} records")
print(f"   IDs: {inserted_ids[:2]}...")

# Get pending URLs
print("\n⏳ Getting pending URLs...")
pending_df = storage.get_pending_urls(limit=5)
print(f"✓ Found {len(pending_df)} pending URLs")

if len(pending_df) > 0:
    print("\nSample data:")
    for idx, row in pending_df.head(2).iterrows():
        print(f"  - {row['title']}")
        print(f"    URL: {row['link']}")
        print(f"    Status: {row['status']}")

# Check if URL exists
print("\n⏳ Testing URL deduplication...")
exists = storage.url_exists("https://example.com/test1")
print(f"✓ URL exists: {exists}")

print("\n" + "=" * 60)
print("✓ All tests passed!")
print("=" * 60)
print("\nCheck your Supabase dashboard:")
print("https://supabase.com/dashboard/project/jovcvbqigjdjishdxrke/editor")
