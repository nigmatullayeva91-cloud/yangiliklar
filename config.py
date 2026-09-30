import os

# --- Maxfiy ma'lumotlar (GitHub Secrets orqali keladi, kodga yozilmaydi!) ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "")   # masalan: @kanal_nomi yoki -1001234567890
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# --- Yangilik manbalari (RSS) ---
# Faqat BITTA alifboda qoldirildi (lotin), aks holda bir xil yangilik
# ikki marta (kirill + lotin) joylanib qolardi.
RSS_SOURCES = [
    "https://www.gazeta.uz/oz/rss/",
    # Agar kirill alifboni afzal ko'rsangiz, tepadagini o'chirib
    # o'rniga shuni yozing: "https://www.gazeta.uz/uz/rss/",
]

# Har ishga tushganda ko'pi bilan nechta yangilik joylansin
MAX_NEWS_PER_RUN = int(os.environ.get("MAX_NEWS_PER_RUN", "3"))

# Qaysi yangiliklar allaqachon joylanganini saqlaydigan fayl
SEEN_FILE = "seen_links.json"

# AI orqali matn qayta yozish uchun model (Groq, bepul)
GROQ_MODEL = "openai/gpt-oss-120b"

# --- Ob-havo posti uchun shahar ---
CITY_NAME = os.environ.get("CITY_NAME", "Toshkent")
CITY_LAT = float(os.environ.get("CITY_LAT", "41.2995"))
CITY_LON = float(os.environ.get("CITY_LON", "69.2401"))
