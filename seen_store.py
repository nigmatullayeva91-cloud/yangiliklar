import json
import os
from config import SEEN_FILE


def load_seen() -> set:
    """Avval joylangan havolalar ro'yxatini o'qiydi."""
    if not os.path.exists(SEEN_FILE):
        return set()
    try:
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data)
    except (json.JSONDecodeError, ValueError):
        return set()


def save_seen(seen: set):
    """Yangilangan ro'yxatni saqlaydi. Fayl juda katta bo'lib ketmasligi uchun
    faqat oxirgi 500 tasini saqlaymiz."""
    seen_list = list(seen)[-500:]
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(seen_list, f, ensure_ascii=False, indent=2)
