import feedparser
from html import unescape
import re
from config import RSS_SOURCES


def _clean_html(raw_html: str) -> str:
    """RSS summary ichidagi HTML teglarini olib tashlaydi."""
    text = re.sub(r"<[^>]+>", "", raw_html or "")
    return unescape(text).strip()


def fetch_all_news() -> list[dict]:
    """Barcha RSS manbalardan yangiliklarni yig'ib, bitta ro'yxatga soladi.
    Har bir element: {title, link, summary, image, published}
    """
    all_items = []

    for url in RSS_SOURCES:
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print(f"[OGOHLANTIRISH] {url} manbasini o'qib bo'lmadi: {e}")
            continue

        for entry in feed.entries:
            title = getattr(entry, "title", "").strip()
            link = getattr(entry, "link", "").strip()
            summary = _clean_html(getattr(entry, "summary", ""))
            published = getattr(entry, "published", "")

            # Manba ichida rasm bo'lsa, uni ham olib qo'yamiz (bo'lmasa AI orqali yaratamiz)
            image = None
            if hasattr(entry, "media_content") and entry.media_content:
                image = entry.media_content[0].get("url")
            elif hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
                image = entry.media_thumbnail[0].get("url")
            elif hasattr(entry, "enclosures") and entry.enclosures:
                image = entry.enclosures[0].get("href")

            if not title or not link:
                continue

            all_items.append({
                "title": title,
                "link": link,
                "summary": summary,
                "image": image,
                "published": published,
            })

    return all_items
