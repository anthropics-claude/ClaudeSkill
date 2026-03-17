import os
import logging
from pathlib import Path
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# --- Agent Skills loader ---
def load_skills(skills_dir: str = "skills") -> dict[str, str]:
    """Membaca semua SKILL.md dari folder skills/ secara rekursif."""
    skills = {}
    base = Path(skills_dir)
    if not base.exists():
        logger.warning(f"Folder {skills_dir} tidak ditemukan.")
        return skills
    
    for skill_file in base.rglob("SKILL.md"):
        skill_name = skill_file.parent.name or "root"
        skills[skill_name] = skill_file.read_text(encoding="utf-8")
        logger.info(f"Loaded skill: {skill_name}")
    return skills

SKILLS = load_skills()

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    skill_list = ", ".join(SKILLS.keys()) if SKILLS else "Belum ada skill"
    await update.message.reply_text(
        f"Halo! Saya Agent Skills Bot.\n\n"
        f"Skills yang tersedia: {skill_list}\n\n"
        f"Kirim /skill <nama> untuk melihat detail skill,\n"
        f"atau kirim pesan apapun dan saya akan merespons."
    )

async def show_skill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Gunakan: /skill <nama_skill>")
        return
    name = context.args[0].lower()
    if name in SKILLS:
        text = SKILLS[name][:4000]  # Telegram message limit
        await update.message.reply_text(f"📄 Skill: {name}\n\n{text}")
    else:
        await update.message.reply_text(f"Skill '{name}' tidak ditemukan.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # Di sini kamu bisa integrasikan dengan LLM (OpenAI, Gemini, dll.)
    # dan inject skill context ke prompt
    skill_context = "\n---\n".join(
        f"[{k}]\n{v}" for k, v in SKILLS.items()
    )
    # Contoh respons sederhana (ganti dengan panggilan LLM)
    response = (
        f"Saya menerima pesan: \"{user_text}\"\n\n"
        f"Saat ini saya punya {len(SKILLS)} skill(s) yang bisa digunakan.\n"
        f"Untuk integrasi penuh, hubungkan dengan API LLM favorit kamu."
    )
    await update.message.reply_text(response)

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN belum di-set!")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("skill", show_skill))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started via polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
