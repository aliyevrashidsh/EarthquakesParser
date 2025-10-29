"""Test Supabase Storage (file storage) - save HTML files."""

from dotenv import load_dotenv

load_dotenv()

from earthquakes_parser import SupabaseStorage

print("=" * 60)
print("Supabase File Storage Test")
print("=" * 60)

# Initialize storage
storage = SupabaseStorage()
print("\n✓ SupabaseStorage initialized")
print(f"✓ Bucket name: {storage.storage_bucket}")

# Create sample HTML content
sample_html = """<!DOCTYPE html>
<html>
<head>
    <title>Тестовая статья о землетрясении</title>
</head>
<body>
    <h1>Землетрясение магнитудой 5.2 произошло в регионе</h1>
    <p>Сегодня в 14:30 по местному времени произошло землетрясение магнитудой 5.2.</p>
    <p>Эпицентр находился на глубине 10 км.</p>
    <p>Пострадавших и разрушений не зарегистрировано.</p>
</body>
</html>"""

print(f"\n✓ Created sample HTML ({len(sample_html)} bytes)")

# First, we need a search_result_id
# Let's create a search result first
import pandas as pd

sample_data = pd.DataFrame(
    [
        {
            "query": "тестовое землетрясение storage",
            "link": "https://example.com/test-storage-article",
            "title": "Test Storage Article",
        }
    ]
)

print("\n⏳ Creating search result...")
inserted_ids = storage.save_search_results(sample_data)
search_result_id = inserted_ids[0]
print(f"✓ Search result created: {search_result_id}")

# Save HTML to storage
print("\n⏳ Saving HTML to Supabase Storage...")
storage_path = storage.save_html_to_storage(
    html_content=sample_html,
    url="https://example.com/test-storage-article",
    search_result_id=search_result_id,
)

if storage_path:
    print(f"✓ HTML saved to: {storage_path}")

    # Try to retrieve it back
    print("\n⏳ Retrieving HTML from storage...")
    retrieved_html = storage.get_html_from_storage(storage_path)

    if retrieved_html:
        print(f"✓ Retrieved HTML ({len(retrieved_html)} bytes)")
        print(f"✓ Content matches: {retrieved_html == sample_html}")

        # Show first 200 characters
        print(f"\nFirst 200 chars:")
        print(retrieved_html[:200] + "...")
    else:
        print("❌ Failed to retrieve HTML")
else:
    print("❌ Failed to save HTML")

# Check search_result status
print("\n⏳ Checking search result status...")
pending_df = storage.get_downloaded_not_parsed(limit=10)
downloaded = pending_df[pending_df["id"] == search_result_id]

if len(downloaded) > 0:
    print(f"✓ Status: {downloaded.iloc[0]['status']}")
    print(f"✓ Storage path: {downloaded.iloc[0]['html_storage_path']}")
else:
    print("⚠️  Search result not found in 'downloaded' status")

print("\n" + "=" * 60)
print("✓ File storage test complete!")
print("=" * 60)
print("\nCheck your Supabase Storage:")
print(
    "https://supabase.com/dashboard/project/jovcvbqigjdjishdxrke/storage/buckets/html-files"
)
