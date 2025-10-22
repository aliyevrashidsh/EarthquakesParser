# Migration from AWS to Supabase - Summary

## What Changed

This project has been migrated from AWS S3 storage to **Supabase** (PostgreSQL database + S3-compatible storage) for better data management in the fake detection use case.

## Why Supabase Instead of AWS S3?

### Before (AWS S3):
- ❌ Only stored CSV/JSON files in S3 buckets
- ❌ No structured querying (can't filter by date, keyword, status)
- ❌ No deduplication (might download same URL multiple times)
- ❌ No status tracking (don't know what's pending/completed/failed)
- ❌ No relationships between search results and parsed content

### After (Supabase):
- ✅ **Structured database** for search results, parsed content, and fake detection results
- ✅ **Object storage** for raw HTML files (S3-compatible)
- ✅ **Automatic deduplication** by URL (unique constraint)
- ✅ **Status tracking** (pending → downloaded → parsed → analyzed → failed)
- ✅ **Queryable data** (filter by date, keyword, confidence score, etc.)
- ✅ **Relationships** (search result → HTML file → parsed content → fake detection)
- ✅ **Real-time subscriptions** (optional, for live updates)

## Files Created

### 1. Database Schema
- **Location**: [supabase/migrations/20250122_create_fake_detection_schema.sql](supabase/migrations/20250122_create_fake_detection_schema.sql)
- **What**: SQL migration creating 3 tables (search_results, parsed_content, fake_detection_results)
- **Features**:
  - UUID primary keys
  - Status enum (pending/downloaded/parsed/analyzed/failed)
  - Timestamps with auto-update triggers
  - Indexes for fast queries
  - Row Level Security (RLS) policies
  - Foreign key relationships

### 2. SupabaseStorage Backend
- **Location**: [earthquakes_parser/storage/supabase_storage.py](earthquakes_parser/storage/supabase_storage.py)
- **What**: Storage backend implementing database + file storage
- **Methods**:
  - `save_search_results()` - Save search results to database
  - `save_html_to_storage()` - Save HTML to object storage
  - `get_html_from_storage()` - Retrieve HTML from storage
  - `save_parsed_content()` - Save parsed text to database
  - `get_pending_urls()` - Get URLs pending download
  - `get_downloaded_not_parsed()` - Get URLs ready for parsing
  - `url_exists()` - Check for duplicates

### 3. Tests
- **Location**: [tests/test_supabase_storage.py](tests/test_supabase_storage.py)
- **Coverage**: 15+ test cases with mocked Supabase client

### 4. Documentation
- **Location**: [docs/SUPABASE_USAGE.md](docs/SUPABASE_USAGE.md)
- **Content**:
  - Complete setup guide
  - Database schema explanation
  - Usage examples for each method
  - Full pipeline example
  - Troubleshooting section

### 5. Example Script
- **Location**: [examples/supabase_example.py](examples/supabase_example.py)
- **What**: Complete working example of the full pipeline

### 6. Updated Files
- [pyproject.toml](pyproject.toml) - Added `supabase` optional dependency
- [earthquakes_parser/__init__.py](earthquakes_parser/__init__.py) - Export `SupabaseStorage`
- [README.md](README.md) - Added Supabase usage examples and environment variables

## Database Schema

### Table 1: `search_results`
Stores search query results and metadata.

```sql
id                UUID (PK)
query             TEXT          -- Keyword searched
link              TEXT UNIQUE   -- URL found
title             TEXT          -- Page title
site_filter       TEXT          -- e.g., "instagram.com"
html_storage_path TEXT          -- Path to HTML in storage
status            ENUM          -- pending/downloaded/parsed/analyzed/failed
searched_at       TIMESTAMPTZ
```

### Table 2: `parsed_content`
Stores extracted and cleaned text.

```sql
id                UUID (PK)
search_result_id  UUID (FK → search_results)
raw_text          TEXT          -- From trafilatura
main_text         TEXT          -- LLM-cleaned text
parsed_at         TIMESTAMPTZ
```

### Table 3: `fake_detection_results`
Stores fake news detection results (future use).

```sql
id                UUID (PK)
parsed_content_id UUID (FK → parsed_content)
is_fake           BOOLEAN
confidence_score  FLOAT (0.0-1.0)
detection_method  TEXT
metadata          JSONB
analyzed_at       TIMESTAMPTZ
```

## How to Setup

### 1. Install Dependencies

```bash
uv pip install -e ".[supabase]"
```

### 2. Create Supabase Project

1. Go to https://supabase.com
2. Create new project
3. Get credentials:
   - Project URL: `https://your-project.supabase.co`
   - Service Role Key (from Settings → API)

### 3. Set Environment Variables

```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-service-role-key"
```

### 4. Apply Database Migration

**Option A: Using Supabase CLI** (recommended)
```bash
# Install CLI
npm install -g supabase

# Login
supabase login

# Link to your project
supabase link --project-ref your-project-ref

# Push migration
supabase db push
```

**Option B: Manual via Dashboard**
1. Go to Supabase Dashboard → SQL Editor
2. Copy content from `supabase/migrations/20250122_create_fake_detection_schema.sql`
3. Paste and run

### 5. Run Example

```bash
python examples/supabase_example.py
```

## Usage Example

```python
from earthquakes_parser import KeywordSearcher, SupabaseStorage
import requests

# Initialize
searcher = KeywordSearcher(delay=1.0)
storage = SupabaseStorage()

# 1. Search and save to database
keywords = ["землетрясение", "магнитуда"]
results_df = searcher.search_to_dataframe(keywords, max_results=10)
inserted_ids = storage.save_search_results(results_df)

# 2. Download HTML for pending URLs
pending_df = storage.get_pending_urls(limit=100)

for idx, row in pending_df.iterrows():
    # Check for duplicates
    if storage.url_exists(row['link']):
        continue

    # Download HTML
    response = requests.get(row['link'])

    # Save to storage (also updates status to 'downloaded')
    storage.save_html_to_storage(response.text, row['link'], row['id'])

# 3. Parse downloaded HTML
downloaded_df = storage.get_downloaded_not_parsed(limit=50)

for idx, row in downloaded_df.iterrows():
    # Get HTML from storage
    html = storage.get_html_from_storage(row['html_storage_path'])

    # Parse with your parser
    # ... (parsing logic)

    # Save parsed content (updates status to 'parsed')
    storage.save_parsed_content(row['id'], raw_text, main_text)
```

## Data Flow

```
Keywords
   ↓
Search (DuckDuckGo) → save_search_results()
   ↓                  [search_results table, status='pending']
get_pending_urls()
   ↓
Download HTML → save_html_to_storage()
   ↓              [Supabase Storage + update status='downloaded']
get_downloaded_not_parsed()
   ↓
Parse HTML → save_parsed_content()
   ↓           [parsed_content table + update status='parsed']
Fake Detection → (future: save to fake_detection_results)
```

## Migration from AWS S3 Code

If you had this:

```python
# OLD: AWS S3
from earthquakes_parser.storage.s3_storage import S3Storage

storage = S3Storage(bucket_name="my-bucket", prefix="earthquakes")
storage.save_dataframe(df, "results.csv")
```

Change to this:

```python
# NEW: Supabase
from earthquakes_parser import SupabaseStorage

storage = SupabaseStorage()
storage.save_search_results(df)  # Saves to database with deduplication
```

## What's Still Compatible

The `S3Storage` class is still available if you need it:

```python
from earthquakes_parser.storage.s3_storage import S3Storage

# Still works!
storage = S3Storage(bucket_name="my-bucket")
```

Both backends implement the same `StorageBackend` interface, so you can switch between them easily.

## Next Steps

1. **Apply the migration** to your Supabase project
2. **Set environment variables** for Supabase credentials
3. **Run the example script** to test the integration
4. **Update your MCP config** in `.mcp.json` with your project reference:
   ```json
   {
     "mcpServers": {
       "supabase": {
         "command": "npx",
         "args": [
           "-y",
           "@supabase/mcp-server-supabase@latest",
           "--read-only",
           "--project-ref=YOUR_PROJECT_REF"
         ],
         "env": {
           "SUPABASE_ACCESS_TOKEN": "your_access_token"
         }
       }
     }
   }
   ```
5. **Implement fake detection** analysis and save to `fake_detection_results` table
6. **Remove AWS S3 dependencies** if no longer needed:
   ```bash
   # Remove boto3 from dependencies if not using S3
   # Update pyproject.toml to remove s3 optional dependency
   ```

## Questions?

See the complete guide: [docs/SUPABASE_USAGE.md](docs/SUPABASE_USAGE.md)
