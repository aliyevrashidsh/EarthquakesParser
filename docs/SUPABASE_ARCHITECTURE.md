# Supabase Architecture

## Overview

This project uses **Supabase** for data storage with a clean separation between infrastructure utilities and business logic.

## Architecture Principles

### 1. **Separation of Concerns**

- **Business Logic** → Lives in domain modules (`parser/`, `searcher/`)
- **Infrastructure** → Lives in utility modules (`storage/supabase/`)

### 2. **Two Independent Utilities**

#### `SupabaseDB` - Database Operations
Low-level PostgreSQL database operations (CRUD).

```python
from earthquakes_parser import SupabaseDB

db = SupabaseDB()

# Generic CRUD operations
db.insert(table, data)
db.select(table, filters, limit)
db.update(table, record_id, data)
db.delete(table, record_id)
db.exists(table, column, value)
db.get_by_id(table, record_id)
```

#### `SupabaseFileStorage` - File Operations
Low-level S3-compatible file storage operations.

```python
from earthquakes_parser import SupabaseFileStorage

files = SupabaseFileStorage(bucket_name="storage")

# Generic file operations
files.upload(path, content, content_type)
files.download(path)
files.delete(path)
files.exists(path)
files.list_files(folder)
```

### 3. **Business Logic Uses Utilities**

Domain modules contain business logic and use utilities for storage:

```python
# searcher/searcher.py
class KeywordSearcher:
    def __init__(self, db: SupabaseDB):
        self.db = db

    def save_results(self, results):
        # Business logic: validation, transformation
        validated = self.validate(results)
        processed = self.transform(validated)

        # Use utility for storage
        return self.db.insert('search_results', processed)

    def get_pending_urls(self):
        # Business logic: get URLs to download
        return self.db.select(
            'search_results',
            filters={'status': 'pending'},
            limit=100
        )

# parser/content_parser.py
class ContentParser:
    def __init__(self, db: SupabaseDB, files: SupabaseFileStorage):
        self.db = db
        self.files = files

    def parse_and_save(self, html, search_id):
        # Business logic: parsing
        parsed = self.parse(html)

        # Use utilities for storage
        # 1. Save HTML file
        path = f'html/{search_id}_{timestamp}.html'
        self.files.upload(path, html, 'text/html')

        # 2. Save parsed content to DB
        self.db.insert('parsed_content', {
            'search_result_id': search_id,
            'raw_text': parsed['raw'],
            'main_text': parsed['main']
        })

        # 3. Update search result status
        self.db.update('search_results', search_id, {
            'status': 'parsed',
            'html_storage_path': path
        })
```

## Directory Structure

```
earthquakes_parser/
├── parser/                 # BUSINESS LOGIC
│   ├── content_parser.py   # Parsing logic + storage orchestration
│   └── ...
│
├── searcher/               # BUSINESS LOGIC
│   ├── searcher.py         # Search logic + storage orchestration
│   └── ...
│
└── storage/                # INFRASTRUCTURE (utilities)
    ├── base.py
    ├── csv_storage.py
    ├── s3_storage.py
    └── supabase/           # Supabase utilities
        ├── __init__.py
        ├── database.py     # SupabaseDB (PostgreSQL)
        └── file_storage.py # SupabaseFileStorage (S3)
```

## Database Schema

### Tables

#### `search_results`
Stores search results from earthquake queries.

```sql
CREATE TABLE search_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query TEXT NOT NULL,
    link TEXT NOT NULL UNIQUE,  -- For deduplication
    title TEXT,
    status processing_status NOT NULL DEFAULT 'pending',
    html_storage_path TEXT,     -- Path in Supabase Storage
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
```

#### `parsed_content`
Stores parsed text extracted from HTML files.

```sql
CREATE TABLE parsed_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    search_result_id UUID NOT NULL REFERENCES search_results(id),
    raw_text TEXT NOT NULL,
    main_text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);
```

#### `fake_detection_results`
Stores ML/analysis results for fake detection.

```sql
CREATE TABLE fake_detection_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parsed_content_id UUID NOT NULL REFERENCES parsed_content(id),
    is_fake BOOLEAN,
    confidence FLOAT,
    reasoning TEXT,
    model_version TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
```

### Status Workflow

```
pending → downloaded → parsed → analyzed
           ↓
         failed
```

## Usage Examples

### Example 1: Search Workflow

```python
from earthquakes_parser import SupabaseDB

# Initialize utility
db = SupabaseDB()

# Business logic: Save search results
search_results = [
    {
        'query': 'землетрясение Алматы',
        'link': 'https://example.com/article1',
        'title': 'Earthquake in Almaty',
        'status': 'pending'
    }
]

ids = db.insert('search_results', search_results)

# Business logic: Get pending URLs
pending = db.select('search_results', filters={'status': 'pending'}, limit=10)

# Business logic: Update after download
db.update('search_results', ids[0], {'status': 'downloaded'})
```

### Example 2: Parser Workflow

```python
from earthquakes_parser import SupabaseDB, SupabaseFileStorage
from datetime import datetime

# Initialize utilities
db = SupabaseDB()
files = SupabaseFileStorage(bucket_name='storage')

# Business logic: Parse and save
html_content = "<html>...</html>"
search_id = "abc-123"

# 1. Save HTML file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
path = f'html/{search_id}_{timestamp}.html'
files.upload(path, html_content, 'text/html')

# 2. Save parsed content
parsed_data = [{
    'search_result_id': search_id,
    'raw_text': 'Raw extracted text...',
    'main_text': 'Cleaned text...'
}]
db.insert('parsed_content', parsed_data)

# 3. Update status
db.update('search_results', search_id, {
    'status': 'parsed',
    'html_storage_path': path
})
```

## Benefits of This Architecture

### ✅ Clear Separation
- **Infrastructure** (storage utilities) separated from **business logic** (domain modules)
- Each utility has single responsibility (DB or Files, not both)

### ✅ Testability
- Business logic can be tested with mocked utilities
- Utilities can be tested independently

### ✅ Flexibility
- Easy to swap storage implementations
- Can use DB without files, or files without DB

### ✅ Parallel Development
- Different team members can work on different domain modules
- No conflicts in storage layer

### ✅ Reusability
- Utilities are generic and can be used by any module
- No business logic leakage into infrastructure

## Migration from Old Architecture

### Old (Monolithic)
```python
# ❌ Everything in one class
from earthquakes_parser import SupabaseStorage

storage = SupabaseStorage()
storage.save_search_results(data)      # DB operation
storage.save_html_to_storage(html)     # File operation
storage.save_parsed_content(parsed)    # DB operation
# Mixed responsibilities, hard to test, tightly coupled
```

### New (Separated)
```python
# ✅ Clear separation
from earthquakes_parser import SupabaseDB, SupabaseFileStorage

db = SupabaseDB()
files = SupabaseFileStorage()

# Business logic chooses what it needs
db.insert('search_results', data)
files.upload('html/file.html', html, 'text/html')
db.insert('parsed_content', parsed)
# Clean, testable, loosely coupled
```

## Configuration

### Environment Variables

```bash
# .env file
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
```

### Initialization

```python
# Option 1: Use environment variables
db = SupabaseDB()  # Reads from SUPABASE_URL and SUPABASE_KEY

# Option 2: Pass explicitly
db = SupabaseDB(url='https://...', key='...')

# File storage with custom bucket
files = SupabaseFileStorage(bucket_name='my-bucket')
```

## See Also

- [examples/supabase_example.py](../examples/supabase_example.py) - Complete examples
- [scripts/test_new_architecture.py](../scripts/test_new_architecture.py) - Test script
- [supabase/migrations/](../supabase/migrations/) - Database schema
