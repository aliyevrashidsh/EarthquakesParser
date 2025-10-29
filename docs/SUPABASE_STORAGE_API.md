# SupabaseStorage API Reference

Полное руководство по методам класса `SupabaseStorage`.

## Содержание

- [Инициализация](#инициализация)
- [Работа с поиском](#работа-с-поиском)
- [Работа с файлами](#работа-с-файлами)
- [Работа с парсингом](#работа-с-парсингом)
- [Утилиты и проверки](#утилиты-и-проверки)
- [Базовые методы StorageBackend](#базовые-методы-storagebackend)

---

## Инициализация

### `__init__(url, key, storage_bucket)`

Создаёт экземпляр Supabase storage.

**Параметры:**
- `url` (str, optional) - URL проекта Supabase. По умолчанию из `SUPABASE_URL` env var
- `key` (str, optional) - Service role key. По умолчанию из `SUPABASE_KEY` env var
- `storage_bucket` (str) - Имя bucket для файлов. По умолчанию `"storage"`

**Пример:**
```python
from earthquakes_parser import SupabaseStorage

# Из переменных окружения
storage = SupabaseStorage()

# С явными параметрами
storage = SupabaseStorage(
    url="https://your-project.supabase.co",
    key="your-service-role-key",
    storage_bucket="my-bucket"
)
```

---

## Работа с поиском

### `save_search_results(results, batch_size=100)`

Сохраняет результаты поиска в базу данных.

**Параметры:**
- `results` (DataFrame | List[Dict]) - Результаты поиска
- `batch_size` (int) - Размер батча для вставки. По умолчанию 100

**Поля результатов:**
- `query` (str, required) - Поисковый запрос
- `link` (str, required) - URL найденной страницы (unique!)
- `title` (str, optional) - Заголовок страницы
- `site_filter` (str, optional) - Фильтр сайта (например, "instagram.com")

**Возвращает:**
- `List[str]` - Список UUID созданных записей

**Особенности:**
- ✅ Автоматическая дедупликация по URL (upsert)
- ✅ Статус устанавливается в `"pending"`
- ✅ Батчинг для больших объёмов

**Пример:**
```python
import pandas as pd

# DataFrame
results_df = pd.DataFrame([
    {
        "query": "землетрясение",
        "link": "https://example.com/news1",
        "title": "Землетрясение в регионе"
    },
    {
        "query": "магнитуда",
        "link": "https://example.com/news2",
        "title": "Магнитуда 5.5"
    }
])

ids = storage.save_search_results(results_df)
print(f"Saved {len(ids)} results")

# Список словарей
results_list = [
    {"query": "test", "link": "https://example.com/1", "title": "Test 1"},
    {"query": "test", "link": "https://example.com/2", "title": "Test 2"}
]

ids = storage.save_search_results(results_list, batch_size=50)
```

---

### `get_pending_urls(limit=100)`

Получает URL со статусом `"pending"` (ещё не скачаны).

**Параметры:**
- `limit` (int) - Максимальное количество записей. По умолчанию 100

**Возвращает:**
- `pd.DataFrame` - DataFrame с колонками:
  - `id` (UUID) - ID записи
  - `query` (str) - Поисковый запрос
  - `link` (str) - URL
  - `title` (str) - Заголовок
  - `status` (str) - Статус ("pending")
  - `searched_at` (datetime) - Время поиска
  - И другие поля...

**Пример:**
```python
# Получить pending URLs
pending_df = storage.get_pending_urls(limit=50)

print(f"Found {len(pending_df)} pending URLs")

for idx, row in pending_df.iterrows():
    print(f"URL: {row['link']}")
    print(f"Query: {row['query']}")
    print(f"ID: {row['id']}")

    # Скачай HTML и сохрани...
```

---

### `get_downloaded_not_parsed(limit=100)`

Получает URL со статусом `"downloaded"` (скачаны, но не распарсены).

**Параметры:**
- `limit` (int) - Максимальное количество записей. По умолчанию 100

**Возвращает:**
- `pd.DataFrame` - DataFrame с колонками (те же, что у `get_pending_urls` плюс):
  - `html_storage_path` (str) - Путь к HTML файлу в storage

**Пример:**
```python
# Получить downloaded URLs
downloaded_df = storage.get_downloaded_not_parsed(limit=20)

for idx, row in downloaded_df.iterrows():
    # Достань HTML из storage
    html = storage.get_html_from_storage(row['html_storage_path'])

    # Парси его
    parsed_text = parse_html(html)

    # Сохрани результат
    storage.save_parsed_content(row['id'], raw_text, parsed_text)
```

---

### `url_exists(url)`

Проверяет, существует ли URL в базе данных.

**Параметры:**
- `url` (str) - URL для проверки

**Возвращает:**
- `bool` - `True` если URL существует, `False` если нет

**Пример:**
```python
url = "https://example.com/article"

if storage.url_exists(url):
    print("URL already processed, skipping...")
else:
    print("New URL, processing...")
    # Скачай и сохрани...
```

---

## Работа с файлами

### `save_html_to_storage(html_content, url, search_result_id)`

Сохраняет HTML контент в Supabase Storage и обновляет статус.

**Параметры:**
- `html_content` (str) - HTML контент
- `url` (str) - Оригинальный URL (используется для логирования)
- `search_result_id` (str) - UUID записи из таблицы `search_results`

**Возвращает:**
- `str | None` - Путь к файлу в storage, или `None` если ошибка

**Автоматически выполняет:**
1. ✅ Генерирует уникальное имя файла: `{id}_{timestamp}.html`
2. ✅ Сохраняет в папку `html/`
3. ✅ Обновляет `html_storage_path` в БД
4. ✅ Меняет статус на `"downloaded"`
5. ❌ При ошибке меняет статус на `"failed"`

**Пример:**
```python
import requests

# Получить pending URLs
pending_df = storage.get_pending_urls(limit=10)

for idx, row in pending_df.iterrows():
    try:
        # Скачать HTML
        response = requests.get(row['link'], timeout=15)
        html = response.text

        # Сохранить в storage
        storage_path = storage.save_html_to_storage(
            html_content=html,
            url=row['link'],
            search_result_id=row['id']
        )

        if storage_path:
            print(f"✓ Saved to: {storage_path}")
        else:
            print(f"✗ Failed to save {row['link']}")

    except Exception as e:
        print(f"✗ Error: {e}")
```

---

### `get_html_from_storage(storage_path)`

Читает HTML файл из Supabase Storage.

**Параметры:**
- `storage_path` (str) - Путь к файлу (из `html_storage_path` в БД)

**Возвращает:**
- `str | None` - HTML контент, или `None` если файл не найден

**Пример:**
```python
# Получить downloaded URLs
downloaded_df = storage.get_downloaded_not_parsed(limit=5)

for idx, row in downloaded_df.iterrows():
    # Достать HTML из storage
    html = storage.get_html_from_storage(row['html_storage_path'])

    if html:
        print(f"Retrieved HTML ({len(html)} bytes)")
        # Парси его...
    else:
        print(f"Failed to retrieve HTML for {row['link']}")
```

---

## Работа с парсингом

### `save_parsed_content(search_result_id, raw_text, main_text)`

Сохраняет распарсенный контент в БД.

**Параметры:**
- `search_result_id` (str) - UUID записи из `search_results`
- `raw_text` (str) - Сырой текст (из trafilatura)
- `main_text` (str) - Очищенный текст (из LLM)

**Возвращает:**
- `str | None` - UUID созданной записи в `parsed_content`, или `None` если ошибка

**Автоматически выполняет:**
1. ✅ Создаёт запись в таблице `parsed_content`
2. ✅ Меняет статус search_result на `"parsed"`
3. ❌ При ошибке меняет статус на `"failed"`

**Пример:**
```python
from earthquakes_parser import ContentParser

parser = ContentParser()

# Получить downloaded URLs
downloaded_df = storage.get_downloaded_not_parsed(limit=10)

for idx, row in downloaded_df.iterrows():
    # Достать HTML
    html = storage.get_html_from_storage(row['html_storage_path'])

    if html:
        # Парсить
        result = parser.parse_url(row['link'], row['query'])

        # Сохранить parsed content
        parsed_id = storage.save_parsed_content(
            search_result_id=row['id'],
            raw_text=result['raw_text'],
            main_text=result['main_text']
        )

        if parsed_id:
            print(f"✓ Parsed content saved: {parsed_id}")
        else:
            print(f"✗ Failed to save parsed content")
```

---

## Утилиты и проверки

### `_ensure_bucket_exists()` (приватный)

Автоматически создаёт bucket если его нет. Вызывается при инициализации.

**Не используй напрямую** - вызывается автоматически в `__init__`.

---

## Базовые методы StorageBackend

Эти методы реализуют интерфейс `StorageBackend` для совместимости с CSV/S3.

### `save(data, key)`

Универсальный метод сохранения.

**Параметры:**
- `data` (DataFrame | List[Dict]) - Данные для сохранения
- `key` (str) - Ключ/идентификатор

**Логика:**
- Если `key` содержит "search_results" → вызывает `save_search_results()`
- Иначе сохраняет как CSV в storage

**Пример:**
```python
# Это вызовет save_search_results()
storage.save(df, "search_results")
storage.save(df, "instagram_search_results")

# Это сохранит как CSV файл
storage.save(df, "other_data")
```

---

### `load(key)`

Загружает CSV данные из storage.

**Параметры:**
- `key` (str) - Ключ (имя файла без расширения)

**Возвращает:**
- `pd.DataFrame | None` - DataFrame или None если не найден

**Пример:**
```python
# Загрузить CSV из storage
df = storage.load("my_data")

if df is not None:
    print(f"Loaded {len(df)} rows")
```

---

### `exists(key)`

Проверяет существование CSV файла в storage.

**Параметры:**
- `key` (str) - Ключ (имя файла без расширения)

**Возвращает:**
- `bool` - True если файл существует

**Пример:**
```python
if storage.exists("my_data"):
    df = storage.load("my_data")
else:
    print("File not found")
```

---

## Полный пример workflow

```python
from earthquakes_parser import KeywordSearcher, ContentParser, SupabaseStorage
import requests

# Инициализация
searcher = KeywordSearcher(delay=1.0)
parser = ContentParser()
storage = SupabaseStorage()

# 1. Поиск
keywords = ["землетрясение", "магнитуда"]
results_df = searcher.search_to_dataframe(keywords, max_results=10)
inserted_ids = storage.save_search_results(results_df)
print(f"Step 1: Found and saved {len(inserted_ids)} URLs")

# 2. Скачивание HTML
pending_df = storage.get_pending_urls(limit=100)
for idx, row in pending_df.iterrows():
    try:
        response = requests.get(row['link'], timeout=15)
        storage_path = storage.save_html_to_storage(
            response.text, row['link'], row['id']
        )
        print(f"Step 2: Downloaded {row['link']}")
    except Exception as e:
        print(f"Error: {e}")

# 3. Парсинг
downloaded_df = storage.get_downloaded_not_parsed(limit=50)
for idx, row in downloaded_df.iterrows():
    html = storage.get_html_from_storage(row['html_storage_path'])
    if html:
        result = parser.parse_url(row['link'], row['query'])
        parsed_id = storage.save_parsed_content(
            row['id'], result['raw_text'], result['main_text']
        )
        print(f"Step 3: Parsed {row['link']}")

print("Pipeline complete!")
```

---

## Статусы записей

Жизненный цикл записи в `search_results`:

```
pending → downloaded → parsed → analyzed
    ↓         ↓          ↓          ↓
  failed    failed    failed    failed
```

| Статус | Когда устанавливается | Метод |
|--------|----------------------|-------|
| `pending` | При создании записи | `save_search_results()` |
| `downloaded` | После сохранения HTML | `save_html_to_storage()` |
| `parsed` | После парсинга | `save_parsed_content()` |
| `analyzed` | После fake detection | (будущий функционал) |
| `failed` | При любой ошибке | Автоматически |

---

## Структура базы данных

### Таблица: `search_results`
```sql
id UUID PRIMARY KEY
query TEXT
link TEXT UNIQUE          -- дедупликация по URL
title TEXT
site_filter TEXT
html_storage_path TEXT    -- путь к HTML в storage
status processing_status  -- pending/downloaded/parsed/analyzed/failed
searched_at TIMESTAMPTZ
created_at TIMESTAMPTZ
updated_at TIMESTAMPTZ
```

### Таблица: `parsed_content`
```sql
id UUID PRIMARY KEY
search_result_id UUID     -- FK → search_results
raw_text TEXT             -- сырой текст
main_text TEXT            -- очищенный текст
parsed_at TIMESTAMPTZ
created_at TIMESTAMPTZ
updated_at TIMESTAMPTZ
```

### Таблица: `fake_detection_results` (будущее)
```sql
id UUID PRIMARY KEY
parsed_content_id UUID    -- FK → parsed_content
is_fake BOOLEAN
confidence_score FLOAT
detection_method TEXT
metadata JSONB
analyzed_at TIMESTAMPTZ
```

---

## Troubleshooting

### Ошибка: "Bucket not found"

```python
# Bucket создаётся автоматически, но если ошибка:
# 1. Проверь права service_role key
# 2. Создай bucket вручную в dashboard
# 3. Или измени имя bucket:

storage = SupabaseStorage(storage_bucket="my-bucket")
```

### Ошибка: "RLS policy"

```python
# Используй service_role key, а не anon key!
# service_role key имеет полные права
```

### Медленные операции

```python
# Используй батчинг
storage.save_search_results(large_df, batch_size=500)

# Или обрабатывай параллельно (многопоточность)
```

---

## См. также

- [Полное руководство по Supabase](SUPABASE_USAGE.md)
- [Миграция с AWS S3](../MIGRATION_SUMMARY.md)
- [Документация Supabase](https://supabase.com/docs)
