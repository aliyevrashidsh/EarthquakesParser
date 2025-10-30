# Supabase Quick Start

## Installation

```bash
pip install supabase python-dotenv
```

## Configuration

Create `.env` file:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
```

## Basic Usage

### Database Operations

```python
from earthquakes_parser import SupabaseDB

db = SupabaseDB()

# Insert
ids = db.insert('search_results', [
    {'query': 'test', 'link': 'https://example.com', 'status': 'pending'}
])

# Select
results = db.select('search_results', filters={'status': 'pending'}, limit=10)

# Update
db.update('search_results', record_id, {'status': 'downloaded'})

# Delete
db.delete('search_results', record_id)

# Check existence
exists = db.exists('search_results', 'link', 'https://example.com')

# Get by ID
record = db.get_by_id('search_results', record_id)
```

### File Storage Operations

```python
from earthquakes_parser import SupabaseFileStorage

files = SupabaseFileStorage(bucket_name='storage')

# Upload
path = files.upload('html/file.html', '<html>...</html>', 'text/html')

# Download
content = files.download('html/file.html')

# Delete
files.delete('html/file.html')

# Check existence
exists = files.exists('html/file.html')

# List files
file_list = files.list_files('html')
```

## Common Patterns

### Save Search Results

```python
db = SupabaseDB()

search_results = [
    {
        'query': 'землетрясение',
        'link': 'https://example.com/article',
        'title': 'Article Title',
        'status': 'pending'
    }
]

ids = db.insert('search_results', search_results)
```

### Download and Parse HTML

```python
db = SupabaseDB()
files = SupabaseFileStorage()

# 1. Get pending URLs
pending = db.select('search_results', filters={'status': 'pending'}, limit=10)

for _, row in pending.iterrows():
    search_id = row['id']
    url = row['link']

    # 2. Download HTML (your download logic)
    html = download_html(url)

    # 3. Save HTML to storage
    path = f'html/{search_id}_{timestamp}.html'
    files.upload(path, html, 'text/html')

    # 4. Update status
    db.update('search_results', search_id, {
        'status': 'downloaded',
        'html_storage_path': path
    })
```

### Parse and Save Content

```python
db = SupabaseDB()
files = SupabaseFileStorage()

# 1. Get downloaded but not parsed
downloaded = db.select('search_results', filters={'status': 'downloaded'}, limit=10)

for _, row in downloaded.iterrows():
    search_id = row['id']
    html_path = row['html_storage_path']

    # 2. Load HTML from storage
    html = files.download(html_path)

    # 3. Parse HTML (your parsing logic)
    raw_text, main_text = parse_html(html)

    # 4. Save parsed content
    db.insert('parsed_content', [{
        'search_result_id': search_id,
        'raw_text': raw_text,
        'main_text': main_text
    }])

    # 5. Update status
    db.update('search_results', search_id, {'status': 'parsed'})
```

## Database Schema

### Tables

- **search_results** - Search results with status tracking
  - `id`, `query`, `link`, `title`, `status`, `html_storage_path`
  - Status: `pending` → `downloaded` → `parsed` → `analyzed`

- **parsed_content** - Extracted text from HTML
  - `id`, `search_result_id`, `raw_text`, `main_text`

- **fake_detection_results** - ML analysis results
  - `id`, `parsed_content_id`, `is_fake`, `confidence`, `reasoning`

## API Reference

### SupabaseDB

| Method | Description |
|--------|-------------|
| `insert(table, data, batch_size=100)` | Insert records |
| `select(table, columns='*', filters=None, limit=None)` | Select records |
| `update(table, record_id, data)` | Update record by ID |
| `delete(table, record_id)` | Delete record by ID |
| `exists(table, column, value)` | Check if record exists |
| `get_by_id(table, record_id)` | Get record by ID |
| `execute_sql(query)` | Execute raw SQL |

### SupabaseFileStorage

| Method | Description |
|--------|-------------|
| `upload(path, content, content_type='text/plain')` | Upload file |
| `download(path)` | Download file |
| `delete(path)` | Delete file |
| `exists(path)` | Check if file exists |
| `list_files(folder='')` | List files in folder |

## Troubleshooting

### Import Error

```python
# Error: cannot import name 'SupabaseDB'
# Solution: Install supabase package
pip install supabase
```

### Connection Error

```python
# Error: Supabase URL and key are required
# Solution: Set environment variables or pass explicitly
db = SupabaseDB(url='https://...', key='...')
```

### Bucket Not Found

```python
# Error: Bucket not found
# Solution: SupabaseFileStorage auto-creates bucket on init
files = SupabaseFileStorage(bucket_name='storage')
```

## Next Steps

- See [SUPABASE_ARCHITECTURE.md](SUPABASE_ARCHITECTURE.md) for detailed architecture
- See [examples/supabase_example.py](../examples/supabase_example.py) for complete examples
- See [scripts/test_new_architecture.py](../scripts/test_new_architecture.py) for test scripts
