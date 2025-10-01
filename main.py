import pandas as pd
from ddgs import DDGS
import time

with open("keywords.txt", "r", encoding="utf-8") as file:
    keywords = [line.strip() for line in file if line.strip()]

ddgs = DDGS()

instagram_df = pd.DataFrame(columns=["query", "link"])
other_df = pd.DataFrame(columns=["query", "link"])

for word in keywords:
    insta_query = f"site:instagram.com {word}"
    print(f"Instagram search: {insta_query}")
    insta_results = ddgs.text(insta_query)
    count = 0
    for result in insta_results:
        link = result.get("href", "")
        if "instagram.com" in link:
            instagram_df = pd.concat([instagram_df, pd.DataFrame([{"query": word, "link": link}])], ignore_index=True)
            count += 1
        if count >= 5:
            break
    instagram_df.to_csv("instagram_links.csv", index=False)
    time.sleep(1)

    normal_query = word
    print(f"Normal search: {normal_query}")
    normal_results = ddgs.text(normal_query)
    count = 0
    for result in normal_results:
        link = result.get("href", "")
        other_df = pd.concat([other_df, pd.DataFrame([{"query": word, "link": link}])], ignore_index=True)
        count += 1
        if count >= 5:
            break
    other_df.to_csv("links.csv", index=False)
    time.sleep(1)
