import requests
from config import BOT_TOKEN, CHANNEL_ID

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"


def post_to_channel(text: str, image_bytes: bytes | None, source_link: str) -> bool:
    """Kanalga rasm bilan (yoki rasmsiz) post joylaydi."""
    caption = f"{text}\n\n🔗 Manba: {source_link}"

    if image_bytes:
        url = f"{API_BASE}/sendPhoto"
        files = {"photo": ("news.jpg", image_bytes)}
        data = {
            "chat_id": CHANNEL_ID,
            "caption": caption[:1024],  # Telegram caption chegarasi
            "parse_mode": "HTML",
        }
        try:
            resp = requests.post(url, data=data, files=files, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            if result.get("ok"):
                return True
            print(f"[XATO] Telegram javobi: {result}")
            return False
        except Exception as e:
            print(f"[XATO] Rasm bilan joylashda xatolik: {e}")
            # Rasm bilan bo'lmasa, faqat matn bilan urinib ko'ramiz
            return _post_text_only(caption)
    else:
        return _post_text_only(caption)


def _post_text_only(text: str) -> bool:
    url = f"{API_BASE}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": text[:4096],
        "parse_mode": "HTML",
    }
    try:
        resp = requests.post(url, data=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if result.get("ok"):
            return True
        print(f"[XATO] Telegram javobi: {result}")
        return False
    except Exception as e:
        print(f"[XATO] Matn joylashda xatolik: {e}")
        return False
