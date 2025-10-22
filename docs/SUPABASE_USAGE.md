# Supabase Storage Guide

This guide explains how to use Supabase as the storage backend for the EarthquakesParser (Fake Detection) project.

## Overview

The Supabase integration provides:

- **PostgreSQL Database**: Store search results, parsed content, and fake detection analysis
- **Object Storage**: Store raw HTML files (S3-compatible)
- **Real-time capabilities**: Optional real-time subscriptions to data changes
- **Automatic deduplication**: Prevent re-processing the same URLs
- **Status tracking**: Track processing pipeline (pending → downloaded → parsed → analyzed)

## Architecture

```
Search Keywords
    ↓
DuckDuckGo Search → Save to Database (search_results table)
    ↓
Download HTML → Save to Supabase Storage + Update status
    ↓
Parse HTML → Save to Database (parsed_content table)
    ↓
Fake Detection → Save to Database (fake_detection_results table)
```

## Setup

### 1. Install Dependencies

```bash
# Install with Supabase support
uv pip install -e ".[supabase]"

# Or install supabase separately
uv pip install supabase
```

### 2. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Wait for the database to be provisioned
4. Get your project credentials:
   - Project URL: `https://your-project.supabase.co`
   - Service Role Key (for backend operations)
   - Anon Key (for frontend operations, if needed)

### 3. Set Environment Variables

```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-service-role-key"
```

Or create a `.env` file:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
```

### 4. Run Database Migrations

Apply the schema migration to create tables:

```bash
# Using Supabase CLI (recommended)
supabase db push

# Or manually via SQL Editor in Supabase Dashboard
# Copy and paste the content of: supabase/migrations/20250122_create_fake_detection_schema.sql
```

### 5. Create Storage Bucket

The storage bucket for HTML files will be created automatically on first use, but you can create it manually:

1. Go to Supabase Dashboard → Storage
2. Create a new bucket named `html-files`
3. Set to **Private** (not public)

## Database Schema

### Table: `search_results`

Stores metadata about search queries and found URLs.

| Column              | Type          | Description                              |
|---------------------|---------------|------------------------------------------|
| id                  | UUID          | Primary key                              |
| query               | TEXT          | Search keyword used                      |
| link                | TEXT          | URL found (unique)                       |
| title               | TEXT          | Page title                               |
| site_filter         | TEXT          | Site filter (e.g., "instagram.com")      |
| html_storage_path   | TEXT          | Path to HTML file in storage             |
| status              | ENUM          | pending/downloaded/parsed/analyzed/failed|
| searched_at         | TIMESTAMPTZ   | When the search was performed            |

### Table: `parsed_content`

Stores extracted and cleaned text from HTML files.

| Column              | Type          | Description                              |
|---------------------|---------------|------------------------------------------|
| id                  | UUID          | Primary key                              |
| search_result_id    | UUID          | Foreign key → search_results             |
| raw_text            | TEXT          | Raw text from trafilatura                |
| main_text           | TEXT          | LLM-cleaned text                         |
| parsed_at           | TIMESTAMPTZ   | When parsing was performed               |

### Table: `fake_detection_results`

Stores fake news detection analysis results (for future use).

| Column              | Type          | Description                              |
|---------------------|---------------|------------------------------------------|
| id                  | UUID          | Primary key                              |
| parsed_content_id   | UUID          | Foreign key → parsed_content             |
| is_fake             | BOOLEAN       | True if detected as fake                 |
| confidence_score    | FLOAT         | Confidence score (0.0 to 1.0)            |
| detection_method    | TEXT          | Model/method used for detection          |
| metadata            | JSONB         | Additional metadata                      |
| analyzed_at         | TIMESTAMPTZ   | When analysis was performed              |

## Usage Examples

### Basic Setup

```python
from earthquakes_parser import SupabaseStorage

# Initialize storage
storage = SupabaseStorage()

# Or with custom bucket
storage = SupabaseStorage(storage_bucket="my-html-files")
```

### 1. Save Search Results

```python
from earthquakes_parser import KeywordSearcher, SupabaseStorage

# Initialize
searcher = KeywordSearcher(delay=1.0)
storage = SupabaseStorage()

# Load keywords
keywords = KeywordSearcher.load_keywords_from_file("config/keywords.txt")

# Search and save to database
results_df = searcher.search_to_dataframe(
    keywords,
    max_results=10,
    site_filter="instagram.com"
)

# Save to Supabase database (automatically deduplicates by URL)
inserted_ids = storage.save_search_results(results_df)
print(f"Inserted {len(inserted_ids)} search results")
```

### 2. Download and Store HTML

```python
import requests

# Get pending URLs from database
pending_df = storage.get_pending_urls(limit=100)

for idx, row in pending_df.iterrows():
    url = row['link']
    search_result_id = row['id']

    # Download HTML
    response = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    html_content = response.text

    # Save to Supabase Storage (automatically updates status to 'downloaded')
    storage_path = storage.save_html_to_storage(
        html_content,
        url,
        search_result_id
    )

    print(f"Saved HTML to: {storage_path}")
```

### 3. Parse HTML and Save Content

```python
from earthquakes_parser import ContentParser

# Initialize parser
parser = ContentParser(model_name="google/flan-t5-large")

# Get downloaded but not parsed URLs
downloaded_df = storage.get_downloaded_not_parsed(limit=50)

for idx, row in downloaded_df.iterrows():
    search_result_id = row['id']
    html_storage_path = row['html_storage_path']

    # Retrieve HTML from storage
    html_content = storage.get_html_from_storage(html_storage_path)

    if html_content:
        # Extract and clean text
        import trafilatura
        raw_text = trafilatura.extract(html_content)
        main_text = parser.clean_with_llm(raw_text)

        # Save parsed content (automatically updates status to 'parsed')
        parsed_id = storage.save_parsed_content(
            search_result_id,
            raw_text,
            main_text
        )

        print(f"Parsed content saved with ID: {parsed_id}")
```

### 4. Check for Duplicates

```python
# Before downloading, check if URL already exists
url = "https://example.com/news/earthquake"

if storage.url_exists(url):
    print("URL already in database, skipping...")
else:
    print("New URL, proceeding with download...")
```

### 5. Query Database (Advanced)

You can use the Supabase client directly for custom queries:

```python
# Get all search results from the last 7 days
from datetime import datetime, timedelta

seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()

response = storage.client.table("search_results") \\
    .select("*") \\
    .gte("searched_at", seven_days_ago) \\
    .order("searched_at", desc=True) \\
    .execute()

import pandas as pd
recent_results = pd.DataFrame(response.data)
print(f"Found {len(recent_results)} results from last 7 days")
```

## Processing Pipeline Example

Complete workflow from search to storage:

```python
from earthquakes_parser import KeywordSearcher, ContentParser, SupabaseStorage
import requests

# Initialize components
searcher = KeywordSearcher(delay=1.0)
parser = ContentParser()
storage = SupabaseStorage()

# Load keywords
keywords = KeywordSearcher.load_keywords_from_file("config/keywords.txt")

# Step 1: Search and save results
print("Step 1: Searching...")
results_df = searcher.search_to_dataframe(keywords, max_results=5)
inserted_ids = storage.save_search_results(results_df)
print(f"Saved {len(inserted_ids)} search results")

# Step 2: Download HTML for pending URLs
print("Step 2: Downloading HTML...")
pending_df = storage.get_pending_urls(limit=10)

for idx, row in pending_df.iterrows():
    try:
        response = requests.get(
            row['link'],
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        storage_path = storage.save_html_to_storage(
            response.text,
            row['link'],
            row['id']
        )
        print(f"✓ Downloaded: {row['link']}")

    except Exception as e:
        print(f"✗ Error downloading {row['link']}: {e}")

# Step 3: Parse downloaded HTML
print("Step 3: Parsing content...")
downloaded_df = storage.get_downloaded_not_parsed(limit=10)

for idx, row in downloaded_df.iterrows():
    html = storage.get_html_from_storage(row['html_storage_path'])

    if html:
        parsed_data = parser.parse_url(row['link'])

        storage.save_parsed_content(
            row['id'],
            parsed_data['raw_text'],
            parsed_data['main_text']
        )
        print(f"✓ Parsed: {row['link']}")

print("Pipeline complete!")
```

## Best Practices

### 1. Use Service Role Key

For backend operations (downloading, parsing), use the **service role key** which has full access:

```bash
export SUPABASE_KEY="your-service-role-key"
```

### 2. Enable Row Level Security (RLS)

The migration automatically enables RLS policies. For production, customize policies:

```sql
-- Example: Only allow authenticated users to read
CREATE POLICY "Read access for authenticated users"
ON search_results FOR SELECT
TO authenticated
USING (true);
```

### 3. Batch Operations

Use batch operations to reduce API calls:

```python
# Good: Save 100 results at once
storage.save_search_results(results_df, batch_size=100)

# Avoid: Saving one by one in a loop
```

### 4. Error Handling

The storage backend automatically updates status to 'failed' on errors:

```python
try:
    storage.save_html_to_storage(html, url, id)
except Exception as e:
    # Status is already set to 'failed' in the database
    print(f"Error: {e}")
```

### 5. Monitor Storage Usage

Check your storage usage in Supabase Dashboard:
- Storage → Usage
- Database → Database Size

## Migration from AWS S3

If you were using S3Storage, here's how to migrate:

### Before (AWS S3):

```python
from earthquakes_parser.storage.s3_storage import S3Storage

storage = S3Storage(bucket_name="my-bucket", prefix="earthquakes")
storage.save_dataframe(df, "results.csv")
```

### After (Supabase):

```python
from earthquakes_parser import SupabaseStorage

storage = SupabaseStorage(storage_bucket="my-bucket")
storage.save_search_results(df)  # Saves to database instead
```

## Troubleshooting

### "Project reference in URL is not valid"

Make sure your `SUPABASE_URL` includes the full project URL:

```bash
# Correct
export SUPABASE_URL="https://abcdefghijk.supabase.co"

# Incorrect
export SUPABASE_URL="abcdefghijk"
```

### "Bucket not found"

Create the bucket manually or check that `_ensure_bucket_exists()` runs successfully.

### RLS Policy Errors

If you get permission errors, ensure you're using the **service role key** (not anon key):

```python
# Use service role key for backend operations
storage = SupabaseStorage(
    url="https://your-project.supabase.co",
    key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # Service role key
)
```

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Python Client](https://supabase.com/docs/reference/python/introduction)
- [Supabase Storage](https://supabase.com/docs/guides/storage)
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
