from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = "8053119583:AAEk2_DTDRqta2_gPuZ83DZkcebwyZ1nKPM"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://politburg-bot.onrender.com{WEBHOOK_PATH}"

app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# Хэндлеры
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я здесь. Что дальше?")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start\n/help\n/post")

async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ Постинг ещё не подключен.")

# Добавление хэндлеров
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(CommandHandler("post", post_command))

# Обработка вебхука
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK", 200

# Запуск
if __name__ == "__main__":
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url=WEBHOOK_URL
    )

# Запуск Flask-сервера
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
