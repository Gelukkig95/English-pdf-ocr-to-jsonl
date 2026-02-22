import requests
from bs4 import BeautifulSoup
import re
import time
from pathlib import Path

HEADERS = {"User-Agent": "Mozilla/5.0"}

def clean_text(text: str) -> str:
    
    text = re.sub(r"\[\d+\]", "", text)

    
    text = text.replace("[edit]", "")
    text = re.sub(r"\s+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

def scrape_wikisource_page(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    
    content = soup.select_one("#mw-content-text .mw-parser-output")
    if not content:
        return ""

    
    for bad in content.select("table, .mw-editsection, .metadata, .reference, sup.reference"):
        bad.decompose()

    
    parts = []
    for el in content.select("h2, h3, p"):
        t = el.get_text(" ", strip=True)
        if t:
            parts.append(t)

    return clean_text("\n\n".join(parts))

def save_txt(title: str, text: str, out_dir="data/raw_txt"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    safe_title = re.sub(r'[\\/:*?"<>|]', "_", title)  # windows-safe filename
    path = Path(out_dir) / f"{safe_title}.txt"
    path.write_text(text, encoding="utf-8")
    print(f"Saved: {path}")

def scrape_many(pages: dict, sleep_sec=1):
    for title, url in pages.items():
        print(f"crawling: {title} ({url})")
        try:
            text = scrape_wikisource_page(url)
            if not text:
                print(f"No content found: {title}\n")
                continue
            save_txt(title, text)
            print()
        except Exception as e:
            print(f"❌ Error: {e}\n")
        time.sleep(sleep_sec)

if __name__ == "__main__":
    target_pages = {
        # examples (replace with the English novels/pages you want)
        "The_Yellow_Wallpaper": "https://en.wikisource.org/wiki/The_Yellow_Wallpaper",
        "The_Gift_of_the_Magi": "https://en.wikisource.org/wiki/The_Gift_of_the_Magi",
    }

    scrape_many(target_pages, sleep_sec=1)