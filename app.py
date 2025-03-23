from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import asyncio
import json

TOKEN = os.getenv("TOKEN", "8053119583:AAEk2_DTDRqta2_gPuZ83DZkcebwyZ1nKPM")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://politburg-bot.onrender.com{WEBHOOK_PATH}"

# Flask
app = Flask(__name__)

# Telegram Application
telegram_app = ApplicationBuilder().token(TOKEN).build()

# === ХЕНДЛЕРЫ ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ PolitBurgBot запущен. Жги команды!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚙️ Я умею:\n/start\n/help\n/post")

async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Постинг будет здесь. В следующей сборке.")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(CommandHandler("post", post_command))

# === WEBHOOK ОБРАБОТЧИК ===
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(json.loads(request.data), telegram_app.bot)
        asyncio.run(telegram_app.process_update(update))
    return "OK", 200
