import json
import os
from datetime import datetime, timezone

OUTPUT_DIR = os.path.join(os.path.dirname(__file__),"..","data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_to_json(headlines: list[dict]) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"Headlines_{timestamp}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(headlines, f, indent=2, ensure_ascii=False)

    print(f"[storage] Saved {len(headlines)} headlines -> {filepath}")
    return filepath