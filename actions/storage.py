import json
import os
from typing import Dict, Optional

STORAGE_FILE = "user_data.json"

def load_user_data() -> Dict[str, Dict[str, str]]:
    if not os.path.exists(STORAGE_FILE):
        return {}
    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_user_data(data: Dict[str, Dict[str, str]]) -> None:
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_user_data(user_id: str) -> Dict[str, str]:
    data = load_user_data()
    return data.get(user_id, {})

def update_user_data(user_id: str, key: str, value: str) -> None:
    data = load_user_data()
    if user_id not in data:
        data[user_id] = {}
    data[user_id][key] = value
    save_user_data(data)