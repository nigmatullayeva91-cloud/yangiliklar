import requests
import urllib.parse

# Pollinations.ai - to'liq bepul, API kaliti talab qilmaydi
POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}?width=1024&height=1024&nologo=true"


def generate_image(prompt: str) -> bytes | None:
    """Berilgan prompt asosida rasm yaratadi va uning baytlarini qaytaradi.
    Muvaffaqiyatsiz bo'lsa None qaytaradi (bu holda rasmsiz, faqat matn joylanadi)."""
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        url = POLLINATIONS_URL.format(prompt=encoded_prompt)
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        if resp.headers.get("content-type", "").startswith("image"):
            return resp.content
        print("[OGOHLANTIRISH] Pollinations rasm emas, boshqa narsa qaytardi.")
        return None
    except Exception as e:
        print(f"[XATO] Rasm yaratishda xatolik: {e}")
        return None


def download_image(url: str) -> bytes | None:
    """Manbadagi tayyor rasmni yuklab oladi (agar RSS ichida rasm bo'lsa)."""
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.content
    except Exception as e:
        print(f"[XATO] Rasmni yuklab olishda xatolik: {e}")
        return None
