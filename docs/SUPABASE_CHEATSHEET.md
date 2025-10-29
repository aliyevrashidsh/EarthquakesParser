# SupabaseStorage - Шпаргалка

Быстрый справочник по всем методам класса.

## 🚀 Инициализация

```python
from earthquakes_parser import SupabaseStorage

storage = SupabaseStorage()  # Из .env
storage = SupabaseStorage(storage_bucket="my-bucket")  # Другой bucket
```

---

## 📥 Сохранение данных

### 1. Сохранить результаты поиска
```python
ids = storage.save_search_results(df)
# → List[UUID] созданных записей
# Статус: pending
```

### 2. Сохранить HTML файл
```python
path = storage.save_html_to_storage(html, url, search_result_id)
# → "html/uuid_timestamp.html"
# Статус: downloaded
```

### 3. Сохранить parsed content
```python
parsed_id = storage.save_parsed_content(search_result_id, raw_text, main_text)
# → UUID parsed_content
# Статус: parsed
```

---

## 📤 Чтение данных

### 1. Получить pending URLs (ещё не скачаны)
```python
pending_df = storage.get_pending_urls(limit=100)
# → DataFrame с id, query, link, title, status
```

### 2. Получить downloaded URLs (скачаны, не распарсены)
```python
downloaded_df = storage.get_downloaded_not_parsed(limit=50)
# → DataFrame с id, link, html_storage_path
```

### 3. Прочитать HTML файл
```python
html = storage.get_html_from_storage(storage_path)
# → str (HTML content)
```

---

## 🔍 Проверки

### Проверить существование URL
```python
exists = storage.url_exists("https://example.com/news")
# → True/False
```

---

## 📊 Workflow пример

```python
from earthquakes_parser import SupabaseStorage
import requests

storage = SupabaseStorage()

# Шаг 1: Сохранить результаты поиска
ids = storage.save_search_results(search_results_df)

# Шаг 2: Скачать HTML для pending URLs
pending = storage.get_pending_urls(limit=10)
for _, row in pending.iterrows():
    html = requests.get(row['link']).text
    storage.save_html_to_storage(html, row['link'], row['id'])

# Шаг 3: Парсить downloaded HTML
downloaded = storage.get_downloaded_not_parsed(limit=10)
for _, row in downloaded.iterrows():
    html = storage.get_html_from_storage(row['html_storage_path'])
    parsed = parse(html)  # твоя функция парсинга
    storage.save_parsed_content(row['id'], parsed['raw'], parsed['main'])
```

---

## 📋 Статусы

```
pending → downloaded → parsed → analyzed
```

| Статус | Метод |
|--------|-------|
| `pending` | `save_search_results()` |
| `downloaded` | `save_html_to_storage()` |
| `parsed` | `save_parsed_content()` |

---

## 💡 Частые паттерны

### Дедупликация перед скачиванием
```python
if not storage.url_exists(url):
    # Скачать и сохранить
    html = download(url)
    storage.save_html_to_storage(html, url, id)
```

### Батч обработка
```python
# Сохранить большой объём данных
storage.save_search_results(big_df, batch_size=500)
```

### Pipeline обработка
```python
# 1. Search → pending
ids = storage.save_search_results(results)

# 2. Download → downloaded
for row in storage.get_pending_urls():
    storage.save_html_to_storage(...)

# 3. Parse → parsed
for row in storage.get_downloaded_not_parsed():
    storage.save_parsed_content(...)
```

---

## 🗄️ Структура storage

```
Supabase Storage (bucket: storage)
└── html/
    ├── uuid1_20250129_123456.html
    ├── uuid2_20250129_123457.html
    └── ...

Database
├── search_results      (метаданные + статусы)
├── parsed_content      (текст)
└── fake_detection_results (анализ)
```

---

## ⚙️ Конфигурация

### Переменные окружения (.env)
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
```

### Python
```python
storage = SupabaseStorage(
    url="...",              # или из SUPABASE_URL
    key="...",              # или из SUPABASE_KEY
    storage_bucket="storage"  # имя bucket
)
```

---

## 🔗 См. также

- [Полный API Reference](SUPABASE_STORAGE_API.md)
- [Руководство по Supabase](SUPABASE_USAGE.md)
- [Миграция с AWS](../MIGRATION_SUMMARY.md)
