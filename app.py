from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import os
import asyncio

# === Конфиг ===
TOKEN = "8053119583:AAEk2_DTDRqta2_gPuZ83DZkcebwyZ1nKPM"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://politburg-bot.onrender.com{WEBHOOK_PATH}"

# === Flask ===
app = Flask(__name__)

# === Telegram Application ===
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


# === Роут для Telegram Webhook ===
@app.post(WEBHOOK_PATH)
async def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
    except Exception as e:
        print(f"[!] Ошибка во входящем update: {e}")
    return "OK"


# === Установка Webhook один раз ===
@app.before_first_request
def setup_webhook():
    asyncio.get_event_loop().run_until_complete(
        application.bot.set_webhook(WEBHOOK_URL)
    )
    print(f"[+] Webhook установлен: {WEBHOOK_URL}")


# === Добавление хэндлеров ===
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("post", post_command))
application.add_handler(CommandHandler("exit", exit_command))
application.add_handler(CommandHandler("stats", stats_command))


# === Запуск Flask ===
if __name__ == "__main__":
    # Установка вебхука
    asyncio.get_event_loop().run_until_complete(set_webhook())

    # Запуск Flask
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

