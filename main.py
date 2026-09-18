"""
O'zbekiston Yangiliklar Boti
----------------------------
Ish tartibi:
1. RSS manbalardan yangiliklarni yig'adi
2. Hali joylanmagan yangiliklarni tanlaydi
3. Har birini AI yordamida kanal uslubida qayta yozadi
4. Har biriga mos rasm yaratadi (yoki manbadagi rasmni oladi)
5. Telegram kanaliga joylaydi
6. Joylangan yangilikni "ko'rilgan" deb belgilaydi (qayta joylanmasligi uchun)
"""

import sys
import time

from config import BOT_TOKEN, CHANNEL_ID, MAX_NEWS_PER_RUN
from fetch_news import fetch_all_news
from seen_store import load_seen, save_seen
from ai_rewrite import rewrite_news
from image_gen import generate_image, download_image
from telegram_post import post_to_channel


def build_fallback_text(title: str, summary: str) -> str:
    """AI ishlamay qolsa ham, kanalga oddiy formatda post tayyorlaydi."""
    text = f"📰 <b>{title}</b>"
    if summary:
        text += f"\n\n{summary[:500]}"
    return text


def main():
    if not BOT_TOKEN or not CHANNEL_ID:
        print("[XATO] BOT_TOKEN yoki CHANNEL_ID topilmadi. "
              "GitHub Secrets yoki muhit o'zgaruvchilarini tekshiring.")
        sys.exit(1)

    print("Yangiliklar yig'ilmoqda...")
    all_news = fetch_all_news()
    print(f"Jami topildi: {len(all_news)} ta yangilik")

    seen = load_seen()
    fresh_news = [n for n in all_news if n["link"] not in seen]
    print(f"Yangi (hali joylanmagan): {len(fresh_news)} ta")

    posted_count = 0
    for item in fresh_news:
        if posted_count >= MAX_NEWS_PER_RUN:
            break

        print(f"\n--- Ishlanmoqda: {item['title'][:60]}...")

        # 1) AI orqali qayta yozish
        ai_result = rewrite_news(item["title"], item["summary"])
        if ai_result:
            post_text = ai_result["post_text"]
            image_prompt = ai_result["image_prompt"]
        else:
            post_text = build_fallback_text(item["title"], item["summary"])
            image_prompt = f"{item['title']}, news illustration, digital art"

        # 2) Rasm tayyorlash: avval manbadagi rasmni sinaymiz, bo'lmasa AI bilan yaratamiz
        image_bytes = None
        if item.get("image"):
            image_bytes = download_image(item["image"])
        if not image_bytes:
            image_bytes = generate_image(image_prompt)

        # 3) Kanalga joylash
        success = post_to_channel(post_text, image_bytes, item["link"])
        if success:
            print("✅ Joylandi")
            seen.add(item["link"])
            posted_count += 1
        else:
            print("❌ Joylanmadi, keyingisiga o'tildi")

        time.sleep(3)  # Telegram limitlariga tegib ketmaslik uchun kichik pauza

    save_seen(seen)
    print(f"\nTugadi. Jami joylangan: {posted_count} ta yangilik.")


if __name__ == "__main__":
    main()
