# SearchManager - Business Logic for Search Operations

## Overview

`SearchManager` provides business logic for managing earthquake search operations with database persistence. It wraps `KeywordSearcher` (search utility) and `SupabaseDB` (database utility) to implement the complete search workflow.

## Architecture

```
SearchManager (Business Logic)
    ├── KeywordSearcher (Search Utility)
    └── SupabaseDB (Database Utility)
```

**Responsibilities:**
- Search for earthquake-related content
- Save search results with deduplication
- Manage search result status workflow
- Provide statistics and reporting

## Quick Start

```python
from earthquakes_parser import SearchManager, SupabaseDB

# Initialize
db = SupabaseDB()
search_manager = SearchManager(db)

# Search and save with deduplication
stats = search_manager.search_and_save(
    keywords=["землетрясение", "earthquake"],
    max_results=5,
    skip_existing=True  # Automatic deduplication
)

print(f"Found: {stats['found']}, New: {stats['new']}, Skipped: {stats['skipped']}")
```

## API Reference

### Constructor

```python
SearchManager(db: SupabaseDB, searcher: Optional[KeywordSearcher] = None)
```

**Parameters:**
- `db`: Supabase database utility for persistence
- `searcher`: Optional KeywordSearcher instance (creates default if None)

### Methods

#### `search_and_save()`

Search for keywords and save results to database with deduplication.

```python
stats = search_manager.search_and_save(
    keywords: List[str],
    max_results: int = 5,
    site_filter: Optional[str] = None,
    skip_existing: bool = True
) -> dict
```

**Parameters:**
- `keywords`: List of search keywords
- `max_results`: Maximum results per keyword
- `site_filter`: Optional site filter (e.g., 'instagram.com')
- `skip_existing`: Skip URLs that already exist (default: True)

**Returns:**
```python
{
    'searched': int,  # Total keywords searched
    'found': int,     # Total results found
    'new': int,       # New results saved
    'skipped': int    # Existing results skipped
}
```

**Business Logic:**
1. Search using KeywordSearcher
2. Check for duplicates (deduplication)
3. Save new results with status='pending'
4. Return statistics

**Example:**
```python
stats = search_manager.search_and_save(
    keywords=["землетрясение Алматы", "earthquake Kazakhstan"],
    max_results=10,
    skip_existing=True
)

if stats['new'] > 0:
    print(f"✓ Saved {stats['new']} new URLs")
if stats['skipped'] > 0:
    print(f"⚠ Skipped {stats['skipped']} existing URLs")
```

#### `get_pending_urls()`

Get URLs that need to be downloaded.

```python
pending_urls = search_manager.get_pending_urls(limit: int = 100) -> List[dict]
```

**Returns:** List of dicts with keys: `id`, `query`, `link`, `title`, `status`

**Example:**
```python
pending = search_manager.get_pending_urls(limit=10)

for url_data in pending:
    print(f"Download: {url_data['link']}")
    # Your download logic here...
```

#### `mark_as_downloaded()`

Mark a search result as downloaded.

```python
success = search_manager.mark_as_downloaded(
    search_result_id: str,
    html_storage_path: str
) -> bool
```

**Business Logic:** Updates status from 'pending' to 'downloaded'

**Example:**
```python
success = search_manager.mark_as_downloaded(
    search_id,
    html_storage_path="html/abc123_20230101.html"
)

if success:
    print("✓ Marked as downloaded")
```

#### `mark_as_failed()`

Mark a search result as failed.

```python
success = search_manager.mark_as_failed(
    search_result_id: str,
    error_message: str = ""
) -> bool
```

**Example:**
```python
try:
    # Download logic...
    pass
except Exception as e:
    search_manager.mark_as_failed(search_id, str(e))
```

#### `get_statistics()`

Get search statistics by status.

```python
stats = search_manager.get_statistics() -> dict
```

**Returns:**
```python
{
    'total': int,
    'pending': int,
    'downloaded': int,
    'parsed': int,
    'analyzed': int,
    'failed': int
}
```

**Example:**
```python
stats = search_manager.get_statistics()
print(f"Pending downloads: {stats['pending']}")
print(f"Ready to parse: {stats['downloaded']}")
```

#### `search_with_keywords_file()`

Search using keywords from file.

```python
stats = search_manager.search_with_keywords_file(
    keywords_file: str,
    max_results: int = 5,
    site_filter: Optional[str] = None,
    skip_existing: bool = True
) -> dict
```

**Example:**
```python
# config/keywords.txt
# землетрясение
# сейсмоактивность

stats = search_manager.search_with_keywords_file(
    "config/keywords.txt",
    max_results=10
)
```

## Complete Workflow Example

```python
from earthquakes_parser import SearchManager, SupabaseDB, SupabaseFileStorage
import requests

# Initialize utilities
db = SupabaseDB()
files = SupabaseFileStorage()
search_manager = SearchManager(db)

# Step 1: Search and save
print("Step 1: Searching...")
stats = search_manager.search_and_save(
    keywords=["землетрясение", "earthquake"],
    max_results=10,
    skip_existing=True
)
print(f"✓ Saved {stats['new']} new URLs")

# Step 2: Download HTML files
print("\nStep 2: Downloading...")
pending = search_manager.get_pending_urls(limit=5)

for url_data in pending:
    search_id = url_data['id']
    url = url_data['link']

    try:
        # Download HTML
        response = requests.get(url, timeout=10)
        html_content = response.text

        # Save to storage
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"html/{search_id}_{timestamp}.html"
        files.upload(path, html_content, 'text/html')

        # Mark as downloaded
        search_manager.mark_as_downloaded(search_id, path)
        print(f"✓ Downloaded: {url}")

    except Exception as e:
        # Mark as failed
        search_manager.mark_as_failed(search_id, str(e))
        print(f"✗ Failed: {url} - {e}")

# Step 3: Check statistics
print("\nStep 3: Statistics")
stats = search_manager.get_statistics()
print(f"Total: {stats['total']}")
print(f"Pending: {stats['pending']}")
print(f"Downloaded: {stats['downloaded']}")
```

## Status Workflow

```
pending → downloaded → parsed → analyzed
           ↓
         failed
```

**Status Management:**
- `pending`: Initial status after search
- `downloaded`: HTML saved to storage
- `parsed`: Content extracted from HTML
- `analyzed`: Fake detection completed
- `failed`: Error occurred at any stage

## Benefits

### ✅ Automatic Deduplication
Prevents duplicate URLs in database using `skip_existing` flag.

```python
# First run
stats = search_manager.search_and_save(keywords, max_results=10)
# stats['new'] = 10, stats['skipped'] = 0

# Second run with same keywords
stats = search_manager.search_and_save(keywords, max_results=10)
# stats['new'] = 0, stats['skipped'] = 10
```

### ✅ Status Tracking
Pipeline workflow with clear status transitions.

```python
# Get work items for each stage
pending = search_manager.get_pending_urls()        # Stage 1: Download
downloaded = db.select('search_results', filters={'status': 'downloaded'})  # Stage 2: Parse
parsed = db.select('search_results', filters={'status': 'parsed'})  # Stage 3: Analyze
```

### ✅ Statistics & Monitoring
Visibility into pipeline progress.

```python
stats = search_manager.get_statistics()
completion_rate = (stats['analyzed'] / stats['total']) * 100 if stats['total'] > 0 else 0
print(f"Completion: {completion_rate:.1f}%")
```

### ✅ Clean Separation
Business logic separate from utilities.

```
SearchManager:  Business logic (what to do)
KeywordSearcher: Search utility (how to search)
SupabaseDB:     Database utility (how to store)
```

## See Also

- [SUPABASE_ARCHITECTURE.md](SUPABASE_ARCHITECTURE.md) - Overall architecture
- [SUPABASE_USAGE.md](SUPABASE_USAGE.md) - Supabase utilities guide
- [scripts/test_search_manager.py](../scripts/test_search_manager.py) - Test script
