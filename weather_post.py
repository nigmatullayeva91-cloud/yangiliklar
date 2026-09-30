"""
Ertangi kun ob-havosini Open-Meteo (bepul, kalitsiz) orqali olib,
Telegram kanaliga alohida post sifatida joylaydi.
"""

import sys
import requests
from datetime import datetime

from config import BOT_TOKEN, CHANNEL_ID, CITY_NAME, CITY_LAT, CITY_LON

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: ("Ochiq, quyoshli havo", "☀️"),
    1: ("Deyarli ochiq havo", "🌤️"),
    2: ("Qisman bulutli", "⛅"),
    3: ("Bulutli havo", "☁️"),
    45: ("Tuman", "🌫️"),
    48: ("Muzli tuman", "🌫️"),
    51: ("Mayda yomg'ir (kuchsiz)", "🌦️"),
    53: ("Mayda yomg'ir (o'rtacha)", "🌦️"),
    55: ("Mayda yomg'ir (kuchli)", "🌧️"),
    61: ("Yomg'ir (kuchsiz)", "🌧️"),
    63: ("Yomg'ir (o'rtacha)", "🌧️"),
    65: ("Yomg'ir (kuchli)", "🌧️"),
    71: ("Qor yog'ishi (kuchsiz)", "🌨️"),
    73: ("Qor yog'ishi (o'rtacha)", "❄️"),
    75: ("Qor yog'ishi (kuchli)", "❄️"),
    80: ("Jala (kuchsiz)", "🌦️"),
    81: ("Jala (o'rtacha)", "🌧️"),
    82: ("Jala (kuchli)", "⛈️"),
    95: ("Momaqaldiroq", "⛈️"),
    96: ("Do'l bilan momaqaldiroq", "⛈️"),
    99: ("Kuchli do'l bilan momaqaldiroq", "⛈️"),
}


def describe_weather(code: int):
    return WEATHER_CODES.get(code, ("Aralash ob-havo", "🌡️"))


def fetch_tomorrow_weather():
    params = {
        "latitude": CITY_LAT,
        "longitude": CITY_LON,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,"
                 "precipitation_probability_max,wind_speed_10m_max",
        "timezone": "Asia/Tashkent",
        "forecast_days": 2,
    }
    resp = requests.get(WEATHER_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    daily = data["daily"]
    idx = 1
    return {
        "date": daily["time"][idx],
        "code": daily["weather_code"][idx],
        "temp_max": round(daily["temperature_2m_max"][idx]),
        "temp_min": round(daily["temperature_2m_min"][idx]),
        "rain_chance": daily["precipitation_probability_max"][idx],
        "wind": round(daily["wind_speed_10m_max"][idx]),
    }


def build_message(weather: dict) -> str:
    desc, emoji = describe_weather(weather["code"])
    date_obj = datetime.strptime(weather["date"], "%Y-%m-%d")
    date_str = date_obj.strftime("%d.%m.%Y")
    text = (
        f"{emoji} <b>Ertangi kun ob-havosi — {CITY_NAME}</b>\n"
        f"📅 {date_str}\n\n"
        f"{desc}\n"
        f"🌡️ Harorat: {weather['temp_min']}°C ... {weather['temp_max']}°C\n"
        f"💧 Yomg'ir ehtimoli: {weather['rain_chance']}%\n"
        f"💨 Shamol: {weather['wind']} km/soat\n\n"
        f"#ObHavo #{CITY_NAME.replace(' ', '')}"
    )
    return text


def send_message(text: str) -> bool:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "HTML"}
    try:
        resp = requests.post(url, data=data, timeout=30)
        result = resp.json()
        if result.get("ok"):
            return True
        print(f"[XATO] Telegram javobi: {result}")
        return False
    except Exception as e:
        print(f"[XATO] Ob-havo postini joylashda xatolik: {e}")
        return False


def main():
    if not BOT_TOKEN or not CHANNEL_ID:
        print("[XATO] BOT_TOKEN yoki CHANNEL_ID topilmadi.")
        sys.exit(1)
    print("Ob-havo ma'lumoti olinmoqda...")
    weather = fetch_tomorrow_weather()
    message = build_message(weather)
    print(message)
    if send_message(message):
        print("✅ Ob-havo posti joylandi")
    else:
        print("❌ Ob-havo posti joylanmadi")


if __name__ == "__main__":
    main()
