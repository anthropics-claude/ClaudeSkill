# Agent Skills Telegram Bot

Telegram Bot berbasis Python yang menggunakan konsep **Agent Skills** dari [agentskills.io](http://agentskills.io).

## Fitur
- Load skills secara dinamis dari folder `skills/`.
- Perintah `/start` untuk melihat daftar skill.
- Perintah `/skill <nama>` untuk melihat detail skill.
- Menangani pesan teks biasa dengan konteks skill.

## Setup Lokal

1. Clone repository ini.
2. Buat virtual environment dan install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # atau venv\Scripts\activate di Windows
   pip install -r requirements.txt
   ```
3. Copy `.env.example` ke `.env` dan isi `TELEGRAM_BOT_TOKEN`.
4. Jalankan bot:
   ```bash
   python bot.py
   ```

## Deployment

### Railway
1. Hubungkan repo GitHub ke Railway.
2. Tambahkan variabel `TELEGRAM_BOT_TOKEN`.

### Scalingo
1. Hubungkan repo GitHub ke Scalingo.
2. Tambahkan variabel `TELEGRAM_BOT_TOKEN`.
3. Pastikan worker dijalankan: `scalingo scale worker:1 web:0`.
