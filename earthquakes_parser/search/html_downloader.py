from typing import Literal
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class HTMLDownloader:
    def __init__(self):
        pass

    def fetch_html(self, url: str, fetch_with: Literal["bs4", "selenium"] = "bs4") -> str:
        match fetch_with:
            case "selenium":
                return self._fetch_with_selenium(url)
            case "bs4":
                return self._fetch_with_bs4(url)
            case _:
                raise ValueError(f"Unsupported fetch method: {fetch_with}")

    @staticmethod
    def _fetch_with_bs4(url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"[BS4] Failed to fetch {url}: {e}")
            return ""

    @staticmethod
    def _fetch_with_selenium(url: str) -> str:
        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(2)
            html = driver.page_source
            driver.quit()
            return html
        except Exception as e:
            print(f"[Selenium] Failed to fetch {url}: {e}")
            return ""
