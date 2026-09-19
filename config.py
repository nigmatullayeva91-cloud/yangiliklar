import os

# --- Maxfiy ma'lumotlar (GitHub Secrets orqali keladi, kodga yozilmaydi!) ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "")   # masalan: @kanal_nomi yoki -1001234567890
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# --- Yangilik manbalari (RSS) ---
# Bu yerga istalgancha RSS manba qo'shishingiz mumkin.
# Manba RSS'ga ega ekanini brauzerda ochib tekshiring.
RSS_SOURCES = [
    "https://www.gazeta.uz/uz/rss/",
    "https://www.gazeta.uz/oz/rss/",
    # Quyidagilarni o'zingiz tekshirib, ishlasa qo'shing:
    # "https://kun.uz/uz/rss",
    # "https://daryo.uz/uz/rss",
    # "https://www.uzreport.news/rss",
]

# Har ishga tushganda ko'pi bilan nechta yangilik joylansin
MAX_NEWS_PER_RUN = int(os.environ.get("MAX_NEWS_PER_RUN", "3"))

# Qaysi yangiliklar allaqachon joylanganini saqlaydigan fayl
SEEN_FILE = "seen_links.json"

# AI orqali matn qayta yozish uchun model (Groq, bepul) 
GROQ_MODEL = "openai/gpt-oss-120b"
