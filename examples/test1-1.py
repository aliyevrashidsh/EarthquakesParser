import requests
import trafilatura
import pandas as pd
import json
from transformers import pipeline


# === 1. Инициализация LLM ===
llm = pipeline("text2text-generation", model="google/flan-t5-large")


# === 2. Функция: извлечь черновой текст через trafilatura ===
def extract_raw_text(url: str) -> str:
    try:
        html = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        ).text
        text = trafilatura.extract(html, include_comments=False, include_tables=False)
        return text if text else ""
    except Exception as e:
        return f"Ошибка загрузки: {e}"


# === 3. Функция: очистить через LLM по блокам ===
def clean_with_llm_blockwise(raw_text: str, block_size: int = 3000) -> str:
    if not raw_text or raw_text.startswith("Ошибка"):
        return raw_text

    try:
        blocks = [raw_text[i:i+block_size] for i in range(0, len(raw_text), block_size)]
        cleaned_blocks = []

        for i, block in enumerate(blocks):
            prompt = (
                "Из следующего текста извлеки только основной связный текст статьи. "
                "Удали рекламу, меню, навигацию и технические вставки:\n\n"
                f"{block}"
            )
            out = llm(prompt, max_length=1024, clean_up_tokenization_spaces=True)
            result = out[0]["generated_text"].strip()

            if len(result.split()) >= 30:
                cleaned_blocks.append(result)
            else:
                cleaned_blocks.append(block)  # fallback

        return "\n\n".join(cleaned_blocks)
    except Exception as e:
        return raw_text


# === 4. Основной парсер: обрабатывает все строки ===
def hybrid_parser(csv_path: str, output_path: str = "output.json"):
    df = pd.read_csv(csv_path)
    results = []

    for idx, row in df.iterrows():
        url = row.get("link", "")
        query = row.get("query", "")

        raw_text = extract_raw_text(url)
        main_text = clean_with_llm_blockwise(raw_text)

        results.append({
            "query": query,
            "link": url,
            "raw_text": raw_text,
            "main_text": main_text
        })
        print(f"✅ [{idx+1}/{len(df)}] Обработано: {url}")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n📂 Все результаты сохранены в {output_path}")


# === 5. Запуск ===
if __name__ == "__main__":
    hybrid_parser("links.csv", "output.json")
