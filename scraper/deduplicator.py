import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

SEEN_URLS_FILE = os.path.join(DATA_DIR, "seen_urls.json")


# def load_seen_urls() -> set:
#     if not os.path.exists(SEEN_URLS_FILE):
#         return set()
#     with open(SEEN_URLS_FILE, "r", encoding="utf-8") as f:
#         return set(json.load(f))

def load_seen_urls() -> set:
    if not os.path.exists(SEEN_URLS_FILE):
        return set()
    with open(SEEN_URLS_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:          # handle empty file
            return set()
        return set(json.loads(content))


def save_seen_urls(seen: set):
    with open(SEEN_URLS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f, indent=2)


def filter_new(headlines: list[dict]) -> list[dict]:
    seen = load_seen_urls()
    new_headlines = []

    for item in headlines:
        if item["url"] not in seen:
            new_headlines.append(item)
            seen.add(item["url"])

    save_seen_urls(seen)
    print(f"[dedup] {len(new_headlines)} new / {len(headlines) - len(new_headlines)} duplicates skipped")
    return new_headlines