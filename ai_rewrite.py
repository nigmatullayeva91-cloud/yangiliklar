import requests
import json
from config import GROQ_API_KEY, GROQ_MODEL

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """Sen o'zbek tilidagi yangiliklar Telegram kanali uchun kontent tayyorlovchi muharrirsan.
Senga bitta yangilikning sarlavhasi va qisqacha matni beriladi.
Vazifang:
1. Uni o'z so'zlaring bilan (manba matnini so'zma-so'z ko'chirmasdan) qayta yoz.
2. Telegram kanal posti uslubida yoz: qisqa, aniq, tushunarli, 4-6 gapdan oshmasin.
3. Boshiga mos 1 ta emoji qo'y.
4. Oxiriga voqeaga mos 2-3 ta hashtag qo'sh (masalan: #Iqtisodiyot #Ozbekiston).
5. Rasm generatsiya qilish uchun, voqeaning mazmunini aks ettiruvchi, ODOB bilan tasvirlangan
   inglizcha qisqa rasm-so'rov (image prompt) yoz. Odamlarning yuzini yoki haqiqiy shaxslarni
   tasvirlashdan qoch, umumiy sahna/mavzuni tasvirla (masalan: "Tashkent city skyline, modern
   buildings, blue sky, digital illustration, news style").

Javobni FAQAT quyidagi JSON formatida qaytar, boshqa hech narsa yozma:
{"post_text": "...", "image_prompt": "..."}
"""


def rewrite_news(title: str, summary: str) -> dict | None:
    """Yangilikni AI yordamida qayta yozadi. Muvaffaqiyatsiz bo'lsa None qaytaradi."""
    if not GROQ_API_KEY:
        print("[OGOHLANTIRISH] GROQ_API_KEY yo'q, AI qayta yozishsiz davom etamiz.")
        return None

    user_content = f"Sarlavha: {title}\nMatn: {summary}"

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.7,
        "max_tokens": 500,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        data = json.loads(content)
        if "post_text" in data and "image_prompt" in data:
            return data
        print("[OGOHLANTIRISH] AI javobi kutilgan formatda emas.")
        return None
    except Exception as e:
        print(f"[XATO] Groq AI so'rovida xatolik: {e}")
        return None
