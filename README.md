# O'zbekiston Yangiliklar Boti

Bu bot RSS orqali yangiliklarni yig'adi, AI yordamida qayta yozadi, mos rasm yaratadi va Telegram kanalingizga avtomatik joylaydi. Hammasi **bepul** — na server, na pullik API kerak emas.

## Qanday ishlaydi (arxitektura)

```
RSS manbalar (Gazeta.uz va h.k.)
        ↓
   fetch_news.py  → yangiliklarni yig'adi
        ↓
   seen_store.py  → qaysi yangilik joylanganini tekshiradi (takror bo'lmasligi uchun)
        ↓
   ai_rewrite.py  → Groq AI orqali matnni qayta yozadi (bepul)
        ↓
   image_gen.py   → Pollinations.ai orqali rasm yaratadi (bepul, kalitsiz)
        ↓
   telegram_post.py → kanalga joylaydi
```

Bularning barchasi **GitHub Actions** orqali serversiz, bepul, avtomatik ishlaydi (30 daqiqada bir marta).

## 1-qadam: Botni yaratish

1. Telegram'da [@BotFather](https://t.me/BotFather) ga yozing.
2. `/newbot` buyrug'ini yuboring, nom va username bering.
3. Sizga **token** beriladi (masalan: `123456:ABC-DEF...`). Buni hech kimga, hech qayerga (jumladan shu chatga ham) ochiq yozmang.
4. Botni o'z kanalingizga **admin** qilib qo'shing (post joylash huquqi bilan).
5. Kanal ID'sini bilish uchun: agar kanal public bo'lsa, `@kanal_username` shaklida ishlatasiz. Agar yopiq bo'lsa, [@userinfobot](https://t.me/userinfobot) yoki [@RawDataBot](https://t.me/RawDataBot) yordamida raqamli ID'ni (masalan `-1001234567890`) topasiz.

## 2-qadam: Bepul AI kalitini olish (Groq)

Groq — juda tez va bepul (kunlik yetarlicha limit bilan) AI xizmati.

1. https://console.groq.com ga kiring, ro'yxatdan o'ting.
2. "API Keys" bo'limidan yangi kalit yarating.
3. Kalitni nusxalab oling (`gsk_...` bilan boshlanadi).

*(Rasm generatsiyasi uchun alohida kalit kerak emas — Pollinations.ai butunlay ochiq va bepul.)*

## 3-qadam: GitHub'da repository yaratish

1. https://github.com da yangi (bo'sh) repository yarating, masalan `uznews-bot`.
2. Shu papkadagi barcha fayllarni o'sha repo'ga yuklang (GitHub saytida "Upload files" orqali ham bo'ladi, yoki `git push` bilan).

## 4-qadam: Maxfiy kalitlarni qo'shish (GitHub Secrets)

Repo ichida: **Settings → Secrets and variables → Actions → New repository secret**

Quyidagi 3 ta secret'ni qo'shing:

| Nomi | Qiymati |
|---|---|
| `BOT_TOKEN` | BotFather bergan token |
| `CHANNEL_ID` | Kanal username yoki ID (masalan `@mening_kanalim`) |
| `GROQ_API_KEY` | Groq'dan olgan kalit |

## 5-qadam: Ishga tushirish

- **Avtomatik**: workflow har 30 daqiqada o'zi ishga tushadi (`.github/workflows/post_news.yml` ichida sozlangan).
- **Qo'lda tekshirish uchun**: repo'ning **Actions** bo'limiga kiring → "Yangiliklarni joylash" → **Run workflow** tugmasini bosing.
- Jarayon logini o'sha yerda (Actions → oxirgi run) ko'rishingiz mumkin — xato bo'lsa shu yerda ko'rinadi.

## Sozlash imkoniyatlari

- **`config.py`** ichida:
  - `RSS_SOURCES` — manbalar ro'yxati. Yangi sayt qo'shish uchun o'sha saytning RSS havolasini toping (odatda `sayt.uz/rss` yoki sayt "footer"ida "RSS" havolasi bo'ladi) va ro'yxatga qo'shing.
  - `MAX_NEWS_PER_RUN` — har safar nechta yangilik joylansin.
  - `GROQ_MODEL` — boshqa Groq modelini tanlash imkoniyati.
- **`.github/workflows/post_news.yml`** ichida `cron: "*/30 * * * *"` qatorini o'zgartirib, chastotani sozlashingiz mumkin (masalan har soatda: `"0 * * * *"`).

## Muhim eslatmalar

- **Mualliflik huquqi**: bot yangilikni so'zma-so'z ko'chirmaydi, AI orqali qayta yozadi va manba havolasini pastda ko'rsatadi. Baribir har bir manbaning foydalanish shartlarini (ayrim saytlar materiallarni ko'chirishga cheklov qo'yishi mumkin) o'zingiz tekshiring — bu texnik emas, huquqiy masala.
- **GitHub Actions bepul limiti**: shaxsiy (public) repolarda Actions cheksiz bepul; private repoda oyiga 2000 daqiqagacha bepul — 30 daqiqalik jadval bilan bemalol yetadi.
- **Groq bepul limiti**: kunlik so'rovlar soni cheklangan, lekin oddiy yangiliklar kanali uchun yetarli. Agar limitdan chiqib ketsa, bot avtomatik ravishda AI'siz (oddiy formatda) matnni joylaydi — botning ishi to'xtamaydi.
- **Rasm sifatsiz yoki mos kelmasa**: `ai_rewrite.py` ichidagi `SYSTEM_PROMPT`ni tahrirlab, image_prompt uslubini o'zgartirishingiz mumkin.

## Keyingi rivojlantirish g'oyalari

- Boshqa Telegram kanallardan (masalan raqobatchi yangilik kanallaridan) post olish uchun **Telethon** kutubxonasi orqali "userbot" qo'shish mumkin (buning uchun https://my.telegram.org dan bepul `API_ID`/`API_HASH` olinadi). Aytsangiz, shu qismini ham qo'shib beraman.
- Duplikat (bir xil voqea, turli manbadan) yangiliklarni AI orqali aniqlab birlashtirish.
- Kategoriya bo'yicha filtrlash (masalan faqat siyosat yoki faqat sport).
