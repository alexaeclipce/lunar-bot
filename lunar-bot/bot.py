import os
import threading
from flask import Flask
import ephem
from datetime import datetime
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from lunar_days_data import lunar_days

# ===================== Flask сервер =====================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

def run_server():
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_server, daemon=True).start()
# =======================================================

TOKEN = os.environ.get("TOKEN")

FIXED_LAT = 45.0
FIXED_LON = 34.0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

user_stats = set()

lunar_emojis = {
    1: "🕯️", 2: "🌾", 3: "🐆", 4: "🌳", 5: "🦄",
    6: "🦩", 7: "🌬️", 8: "🔥", 9: "🦇", 10: "⛲",
    11: "🗡️", 12: "❤️", 13: "🎡", 14: "📯", 15: "🐍",
    16: "🕊️", 17: "🔔", 18: "🪞", 19: "🕷️", 20: "🦅",
    21: "🐎", 22: "🐘", 23: "🐊", 24: "🐻", 25: "🐚",
    26: "🐸", 27: "🪄", 28: "🌸", 29: "🐙", 30: "🦢"
}

def get_image_path(day):
    """Ищет картинку независимо от регистра JPG/jpg"""
    for ext in ["JPG", "jpg", "JPEG", "jpeg", "png"]:
        path = os.path.join(IMAGES_DIR, f"{day}.{ext}")
        if os.path.exists(path):
            return path
    return None

def get_lunar_day():
    obs = ephem.Observer()
    obs.lat = str(FIXED_LAT)
    obs.lon = str(FIXED_LON)
    obs.date = datetime.utcnow()

    moon = ephem.Moon(obs)
    elong_deg = float(moon.elong) * 180 / 3.141592653589793
    lunar_day = int(elong_deg // 12) + 1
    return max(1, min(lunar_day, 30))

def get_moon_phase():
    obs = ephem.Observer()
    obs.lat = str(FIXED_LAT)
    obs.lon = str(FIXED_LON)
    obs.date = datetime.utcnow()

    moon = ephem.Moon(obs)
    phase_percent = moon.phase

    if phase_percent == 0:
        phase_name = "Новолуние 🌑"
    elif 0 < phase_percent < 50:
        phase_name = "Растущая Луна 🌒"
    elif phase_percent == 50:
        phase_name = "Первая четверть 🌓"
    elif 50 < phase_percent < 99:
        phase_name = "Прибывающая Луна 🌔"
    else:
        phase_name = "Полнолуние 🌕"

    return phase_name, phase_percent

# ===================== handlers =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Текущие лунные сутки"]]
    await update.message.reply_text(
        "Привет! Нажми кнопку ниже.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Текущие лунные сутки":
        lunar_day = get_lunar_day()
        phase_name, phase_percent = get_moon_phase()

        emoji = lunar_emojis.get(lunar_day, "")
        description = lunar_days.get(lunar_day, "")

        caption = (
            f"<b>{lunar_day} лунный день</b>\n"
            f"<b>Фаза Луны:</b> {phase_name} ({phase_percent:.1f}%)"
        )

        image_path = get_image_path(lunar_day)

        if image_path:
            with open(image_path, "rb") as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption=caption,
                    parse_mode="HTML",
                )
        else:
            await update.message.reply_text(caption, parse_mode="HTML")

        await update.message.reply_text(f"{emoji} {description}")
        user_stats.add(update.message.from_user.id)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Пользователей: {len(user_stats)}"
    )

# ===================== run bot =====================
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Bot started...")
    application.run_polling()
