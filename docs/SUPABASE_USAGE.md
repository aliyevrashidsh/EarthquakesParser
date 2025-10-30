# Supabase Usage Guide

This guide explains how to use Supabase utilities in the EarthquakesParser (Fake Detection) project.

## Overview

The Supabase integration provides two independent utilities:

- **SupabaseDB**: PostgreSQL database operations (tables, CRUD)
- **SupabaseFileStorage**: S3-compatible file storage operations (upload, download)

## Quick Start

### 1. Install Dependencies

```bash
# Install with Supabase support
uv pip install -e ".[supabase]"

# Or install supabase separately
uv pip install supabase python-dotenv
```

### 2. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Wait for the database to be provisioned
4. Get your credentials from project settings

### 3. Configure Environment

Create `.env` file in project root:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
```

### 4. Apply Database Schema

```bash
# Use Supabase CLI or SQL Editor in dashboard
# Apply migration from: supabase/migrations/20250122_create_fake_detection_schema.sql
```

## Usage

### Import Utilities

```python
from earthquakes_parser import SupabaseDB, SupabaseFileStorage
```

### Database Operations

```python
# Initialize
db = SupabaseDB()

# Insert records
search_results = [
    {
        'query': 'землетрясение Алматы',
        'link': 'https://example.com/article',
        'title': 'Earthquake in Almaty',
        'status': 'pending'
    }
]
ids = db.insert('search_results', search_results)

# Select with filters
pending = db.select(
    'search_results',
    filters={'status': 'pending'},
    limit=10
)

# Update record
db.update('search_results', record_id, {
    'status': 'downloaded',
    'html_storage_path': 'html/file.html'
})

# Check existence
exists = db.exists('search_results', 'link', 'https://example.com')

# Get by ID
record = db.get_by_id('search_results', record_id)

# Delete
db.delete('search_results', record_id)
```

### File Storage Operations

```python
# Initialize
files = SupabaseFileStorage(bucket_name='storage')

# Upload file
html_content = '<html>...</html>'
path = files.upload('html/file.html', html_content, 'text/html')

# Download file
content = files.download('html/file.html')

# Check if exists
exists = files.exists('html/file.html')

# List files
file_list = files.list_files('html')

# Delete file
files.delete('html/file.html')
```

## Workflow Examples

### Complete Search → Parse → Analyze Pipeline

```python
from earthquakes_parser import SupabaseDB, SupabaseFileStorage, KeywordSearcher, ContentParser
from datetime import datetime

# Initialize utilities
db = SupabaseDB()
files = SupabaseFileStorage(bucket_name='storage')

# Step 1: Search and save results
searcher = KeywordSearcher()
search_results = searcher.search('землетрясение')

# Save to database
results_data = [
    {
        'query': 'землетрясение',
        'link': r.link,
        'title': r.title,
        'status': 'pending'
    }
    for r in search_results
]
db.insert('search_results', results_data)

# Step 2: Download HTML files
pending = db.select('search_results', filters={'status': 'pending'}, limit=10)

for _, row in pending.iterrows():
    search_id = row['id']
    url = row['link']

    # Download (your logic)
    html = download_html(url)

    # Save to storage
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f'html/{search_id}_{timestamp}.html'
    files.upload(path, html, 'text/html')

    # Update status
    db.update('search_results', search_id, {
        'status': 'downloaded',
        'html_storage_path': path
    })

# Step 3: Parse HTML
parser = ContentParser()
downloaded = db.select('search_results', filters={'status': 'downloaded'}, limit=10)

for _, row in downloaded.iterrows():
    search_id = row['id']
    html_path = row['html_storage_path']

    # Load HTML
    html = files.download(html_path)

    # Parse
    raw_text = parser.extract_raw_text(html)
    main_text = parser.clean_with_llm(raw_text)

    # Save parsed content
    db.insert('parsed_content', [{
        'search_result_id': search_id,
        'raw_text': raw_text,
        'main_text': main_text
    }])

    # Update status
    db.update('search_results', search_id, {'status': 'parsed'})

# Step 4: Fake detection analysis (future)
# Your ML model logic here...
```

## Database Schema

### Tables

#### `search_results`
Tracks search results and processing status.

**Columns:**
- `id` (UUID) - Primary key
- `query` (TEXT) - Search query
- `link` (TEXT) - URL (unique for deduplication)
- `title` (TEXT) - Article title
- `status` (ENUM) - Processing status
- `html_storage_path` (TEXT) - Path in Supabase Storage
- `created_at`, `updated_at` (TIMESTAMP)

**Status Flow:**
```
pending → downloaded → parsed → analyzed
           ↓
         failed
```

#### `parsed_content`
Stores extracted text from HTML.

**Columns:**
- `id` (UUID) - Primary key
- `search_result_id` (UUID) - Foreign key to search_results
- `raw_text` (TEXT) - Raw extracted text
- `main_text` (TEXT) - Cleaned/processed text
- `created_at` (TIMESTAMP)

#### `fake_detection_results`
Stores ML analysis results.

**Columns:**
- `id` (UUID) - Primary key
- `parsed_content_id` (UUID) - Foreign key to parsed_content
- `is_fake` (BOOLEAN) - Detection result
- `confidence` (FLOAT) - Confidence score
- `reasoning` (TEXT) - Explanation
- `model_version` (TEXT) - ML model version
- `created_at` (TIMESTAMP)

## Best Practices

### 1. **Use Utilities in Business Logic**

```python
# ✅ Good: Business logic in domain module
class ContentParser:
    def __init__(self, db: SupabaseDB, files: SupabaseFileStorage):
        self.db = db
        self.files = files

    def parse_and_save(self, search_id):
        # Business logic here
        # Use utilities for storage
        pass

# ❌ Bad: Business logic in utility module
# Don't add business methods to SupabaseDB or SupabaseFileStorage
```

### 2. **Batch Inserts for Performance**

```python
# ✅ Good: Batch insert
db.insert('search_results', search_results, batch_size=100)

# ❌ Bad: Individual inserts in loop
for result in search_results:
    db.insert('search_results', [result])  # Slow!
```

### 3. **Check Existence Before Insert**

```python
# Avoid duplicate URLs
url = 'https://example.com/article'
if not db.exists('search_results', 'link', url):
    db.insert('search_results', [{'link': url, ...}])
```

### 4. **Use Filters for Efficient Queries**

```python
# ✅ Good: Filter at database level
pending = db.select('search_results', filters={'status': 'pending'}, limit=10)

# ❌ Bad: Load all, filter in Python
all_results = db.select('search_results')  # Loads everything!
pending = all_results[all_results['status'] == 'pending']
```

### 5. **Handle Errors Gracefully**

```python
try:
    ids = db.insert('search_results', data)
    if not ids:
        print("Insert failed, no IDs returned")
except Exception as e:
    print(f"Error inserting data: {e}")
```

## Configuration Options

### Database

```python
# Use environment variables
db = SupabaseDB()

# Or pass explicitly
db = SupabaseDB(
    url='https://your-project.supabase.co',
    key='your-service-role-key'
)
```

### File Storage

```python
# Default bucket name is 'storage'
files = SupabaseFileStorage()

# Custom bucket
files = SupabaseFileStorage(bucket_name='my-custom-bucket')

# Explicit credentials
files = SupabaseFileStorage(
    url='https://your-project.supabase.co',
    key='your-service-role-key',
    bucket_name='storage'
)
```

## Troubleshooting

### Import Error

```
ImportError: cannot import name 'SupabaseDB'
```

**Solution:** Install supabase package
```bash
pip install supabase
```

### Connection Error

```
ValueError: Supabase URL and key are required
```

**Solution:** Set environment variables or pass credentials explicitly
```python
db = SupabaseDB(url='https://...', key='...')
```

### Column Not Found

```
Could not find the 'column_name' column in the schema cache
```

**Solution:** Check column name matches database schema, apply migrations

### Bucket Not Found

The bucket is created automatically on first use. If you see errors, check:
1. Credentials are correct
2. Service role key has storage permissions

## See Also

- [SUPABASE_ARCHITECTURE.md](SUPABASE_ARCHITECTURE.md) - Detailed architecture explanation
- [SUPABASE_QUICKSTART.md](SUPABASE_QUICKSTART.md) - Quick reference
- [examples/supabase_example.py](../examples/supabase_example.py) - Complete examples
- [scripts/test_new_architecture.py](../scripts/test_new_architecture.py) - Test script
