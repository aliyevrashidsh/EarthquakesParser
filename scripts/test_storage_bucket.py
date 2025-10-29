"""Test Supabase Storage with 'storage' bucket."""

from dotenv import load_dotenv

load_dotenv()

import pandas as pd

from earthquakes_parser import SupabaseStorage

print("=" * 60)
print("Test Storage Bucket")
print("=" * 60)

# Initialize storage (will use 'storage' bucket by default now)
storage = SupabaseStorage()
print(f"\n✓ SupabaseStorage initialized")
print(f"✓ Bucket name: {storage.storage_bucket}")

# Create sample HTML
sample_html = """<!DOCTYPE html>
<html>
<head>
    <title>Тест storage bucket</title>
</head>
<body>
    <h1>Проверка нового bucket 'storage'</h1>
    <p>Этот файл сохранён в bucket с именем 'storage'</p>
</body>
</html>"""

# Create search result
sample_data = pd.DataFrame(
    [
        {
            "query": "тест storage bucket",
            "link": "https://example.com/test-new-bucket",
            "title": "Test New Bucket",
        }
    ]
)

print("\n⏳ Creating search result...")
inserted_ids = storage.save_search_results(sample_data)
search_result_id = inserted_ids[0]
print(f"✓ ID: {search_result_id}")

# Save HTML to new 'storage' bucket
print("\n⏳ Saving HTML to 'storage' bucket...")
try:
    storage_path = storage.save_html_to_storage(
        html_content=sample_html,
        url="https://example.com/test-new-bucket",
        search_result_id=search_result_id,
    )

    if storage_path:
        print(f"✓ HTML saved to: {storage_path}")

        # Try to retrieve
        print("\n⏳ Retrieving HTML...")
        retrieved_html = storage.get_html_from_storage(storage_path)

        if retrieved_html:
            print(f"✓ Retrieved successfully ({len(retrieved_html)} bytes)")
            print(f"✓ Content matches: {retrieved_html == sample_html}")
        else:
            print("❌ Failed to retrieve")
    else:
        print("❌ Failed to save")

except Exception as e:
    print(f"❌ Error: {e}")
    print("\nNote: You may need to create 'storage' bucket in Supabase Dashboard:")
    print("https://supabase.com/dashboard/project/jovcvbqigjdjishdxrke/storage/buckets")

print("\n" + "=" * 60)
print("Test complete!")
print("=" * 60)
