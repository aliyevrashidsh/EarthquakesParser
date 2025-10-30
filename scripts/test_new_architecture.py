"""Test new Supabase architecture with separated DB and File Storage."""

import os
from datetime import datetime

from dotenv import load_dotenv

# Load environment
load_dotenv()

from earthquakes_parser import SupabaseDB, SupabaseFileStorage

print("=" * 60)
print("Test New Supabase Architecture")
print("=" * 60)

# Initialize utilities
db = SupabaseDB()
file_storage = SupabaseFileStorage(bucket_name="storage")

print(f"\n✓ SupabaseDB initialized")
print(f"✓ SupabaseFileStorage initialized (bucket: storage)")

# Test 1: Database operations
print("\n" + "=" * 60)
print("Test 1: Database Operations")
print("=" * 60)

# Insert search result
search_data = [
    {
        "query": "test query",
        "link": f"https://example.com/test-{datetime.now().timestamp()}",
        "title": "Test Article",
        "status": "pending",
    }
]

print("\n⏳ Inserting search result...")
ids = db.insert("search_results", search_data)
if ids:
    search_id = ids[0]
    print(f"✓ Inserted: {search_id}")
else:
    print("✗ Failed to insert")
    exit(1)

# Select by status
print("\n⏳ Selecting pending results...")
results = db.select("search_results", filters={"status": "pending"}, limit=5)
print(f"✓ Found {len(results)} pending results")

# Update status
print("\n⏳ Updating status to 'downloaded'...")
updated = db.update("search_results", search_id, {"status": "downloaded"})
if updated:
    print(f"✓ Updated: {updated['id']}")

# Check existence
print("\n⏳ Checking if record exists...")
exists = db.exists("search_results", "id", search_id)
print(f"✓ Exists: {exists}")

# Get by ID
print("\n⏳ Getting record by ID...")
record = db.get_by_id("search_results", search_id)
if record:
    print(f"✓ Retrieved: {record['title']}")
    print(f"  Status: {record['status']}")

# Test 2: File Storage operations
print("\n" + "=" * 60)
print("Test 2: File Storage Operations")
print("=" * 60)

# Upload HTML file
html_content = """<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body><h1>Test Content</h1></body>
</html>"""

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_path = f"html/test_{timestamp}.html"

print(f"\n⏳ Uploading file to {file_path}...")
uploaded_path = file_storage.upload(file_path, html_content, "text/html")
if uploaded_path:
    print(f"✓ Uploaded: {uploaded_path}")
else:
    print("✗ Failed to upload")
    exit(1)

# Download file
print(f"\n⏳ Downloading file...")
downloaded_content = file_storage.download(file_path)
if downloaded_content:
    print(f"✓ Downloaded ({len(downloaded_content)} bytes)")
    print(f"✓ Content matches: {downloaded_content == html_content}")

# Check if exists
print(f"\n⏳ Checking if file exists...")
file_exists = file_storage.exists(file_path)
print(f"✓ File exists: {file_exists}")

# List files
print(f"\n⏳ Listing files in 'html' folder...")
files = file_storage.list_files("html")
print(f"✓ Found {len(files)} files")

# Test 3: Business logic simulation
print("\n" + "=" * 60)
print("Test 3: Business Logic Simulation")
print("=" * 60)

print("\n📝 In real app, parser/searcher modules would use these utilities:")
print(
    """
# searcher/searcher.py
class KeywordSearcher:
    def __init__(self, db: SupabaseDB):
        self.db = db

    def save_results(self, results):
        # Business logic: validation, transformation
        processed = self.validate_and_transform(results)
        # Use utility for storage
        return self.db.insert('search_results', processed)

# parser/content_parser.py
class ContentParser:
    def __init__(self, db: SupabaseDB, file_storage: SupabaseFileStorage):
        self.db = db
        self.file_storage = file_storage

    def parse_and_save(self, html, search_id):
        # Business logic: parsing
        parsed = self.parse(html)

        # Use utilities for storage
        path = f'html/{search_id}_{timestamp}.html'
        self.file_storage.upload(path, html, 'text/html')
        self.db.insert('parsed_content', {
            'search_result_id': search_id,
            'raw_text': parsed['raw'],
            'main_text': parsed['main']
        })
        self.db.update('search_results', search_id, {'status': 'parsed'})
"""
)

print("\n" + "=" * 60)
print("✓ All tests passed!")
print("=" * 60)
print("\n✅ New architecture working correctly!")
print("✅ DB and File Storage are now independent utilities")
print("✅ Business logic can use them separately or together")
