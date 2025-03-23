from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import os

TOKEN = "8053119583:AAEk2_DTDRqta2_gPuZ83DZkcebwyZ1nKPM"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://politburg-bot.onrender.com{WEBHOOK_PATH}"

app = Flask(__name__)
bot = Bot(token=TOKEN)

telegram_app = ApplicationBuilder().token(TOKEN).build()


# === Хэндлеры ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("PolitBurgBot активен. Швыряй команды.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Вот что я умею:\n/start\n/help\n/post")

async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ Здесь будет реализация постинга.")


# === Webhook ===
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        telegram_app.update_queue.put(update)
        return "OK", 200
    return "Invalid request", 400


if __name__ == "__main__":
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("help", help_command))
    telegram_app.add_handler(CommandHandler("post", post_command))

    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url=WEBHOOK_URL,
    )

