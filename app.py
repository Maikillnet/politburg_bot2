from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
import os
import asyncio

# === Конфигурация ===
TOKEN = "8053119583:AAEk2_DTDRqta2_gPuZ83DZkcebwyZ1nKPM"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://politburg-bot.onrender.com{WEBHOOK_PATH}"

# === Flask-сервер ===
app = Flask(__name__)

# === Telegram Bot ===
application = ApplicationBuilder().token(TOKEN).build()

# === Хэндлеры ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("PolitBurgBot активен. Швыряй команды.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Вот что я умею:\n/start\n/help\n/post\n/exit\n/stats")

async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ Здесь будет реализация постинга.")

async def exit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот не хочет умирать. Но если надо — добавим shutdown.")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Статистика: пока ничего, но скоро будет.")

# === Регистрируем хэндлеры ===
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("post", post_command))
application.add_handler(CommandHandler("exit", exit_command))
application.add_handler(CommandHandler("stats", stats_command))

# === Webhook для Telegram (асинхронный) ===
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

# === Установка Webhook ===
async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)
    print(f"[+] Webhook установлен: {WEBHOOK_URL}")

# === Запуск ===
if __name__ == "__main__":
    asyncio.run(set_webhook())
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


    # Запуск Flask
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

