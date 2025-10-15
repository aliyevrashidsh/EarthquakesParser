# Configuration

This directory contains configuration files for the EarthquakesParser project.

## Files

### [keywords.txt](keywords.txt)

List of Russian keywords related to earthquakes, disasters, and emergencies for search queries.

**Format:** One keyword per line (plain text, UTF-8)

**Categories included:**

- Earthquake terms (землетрясение, магнитуда, эпицентр)
- Immediate response (эвакуация, укрытие, спасатели)
- Damage and casualties (жертвы, пострадавшие, разрушение)
- Infrastructure (нет связи, отключили свет)
- Other disasters (цунами, наводнение, пожар)
- Emergency services (ЧС, МЧС)

**Usage:**

```python
from earthquakes_parser import KeywordSearcher

# Load keywords from config
keywords = KeywordSearcher.load_keywords_from_file("config/keywords.txt")

# Use for search
searcher = KeywordSearcher()
results = searcher.search_to_dataframe(keywords, max_results=5)
```

## Adding More Keywords

### For Earthquakes

Edit `keywords.txt` and add earthquake-related terms:

```text
сейсмическая активность
подземные толчки
афтершоки
```

### For Other Disasters

Create separate keyword files:

- `keywords_floods.txt` - Flood keywords
- `keywords_fires.txt` - Fire keywords
- `keywords_storms.txt` - Storm keywords

Example:

```bash
# Create flood-specific keywords
cat > config/keywords_floods.txt << EOF
наводнение
потоп
паводок
затопление
EOF
```

## Configuration Best Practices

### File Organization

```text
config/
├── README.md
├── keywords.txt              # Main earthquake keywords
├── keywords_en.txt           # English keywords (optional)
├── keywords_custom.txt       # Custom keywords (optional)
└── search_settings.json      # Search settings (optional)
```

### Example: Search Settings (Future)

```json
{
  "default_max_results": 10,
  "delay_between_searches": 1.0,
  "default_timeout": 15,
  "sites": {
    "social": ["instagram.com", "twitter.com", "vk.com"],
    "news": ["tass.ru", "ria.ru", "interfax.ru"]
  }
}
```

## Environment-Specific Configs

For different environments:

```text
config/
├── keywords.txt              # Default
├── keywords.dev.txt          # Development
├── keywords.prod.txt         # Production
├── keywords.test.txt         # Testing
```

Load based on environment:

```python
import os

env = os.getenv("ENV", "dev")
keywords_file = f"config/keywords.{env}.txt"
keywords = KeywordSearcher.load_keywords_from_file(keywords_file)
```

## Version Control

- ✅ **DO** commit keyword files
- ✅ **DO** document keyword meanings
- ❌ **DON'T** commit sensitive API keys or credentials
- ❌ **DON'T** commit local/personal configurations

Use `.env` files for secrets:

```bash
# .env (gitignored)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
```

## Localization

For multi-language support:

```text
config/
├── keywords.ru.txt           # Russian (current)
├── keywords.en.txt           # English
├── keywords.es.txt           # Spanish
├── keywords.tr.txt           # Turkish
```

Usage:

```python
language = "ru"
keywords = KeywordSearcher.load_keywords_from_file(f"config/keywords.{language}.txt")
```
