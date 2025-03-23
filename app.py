from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    ContextTypes
)
import os
import asyncio

TOKEN = "твой_токен"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://твой-домен.onrender.com{WEBHOOK_PATH}"

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# === Хэндлеры ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я в сети, брат.")

application.add_handler(CommandHandler("start", start))

# === Webhook ===
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    await application.update_queue.put(Update.de_json(request.get_json(force=True), application.bot))
    return "ok"

# === Запуск ===
if __name__ == "__main__":
    async def run():
        await application.initialize()
        await application.start()
        await application.bot.set_webhook(url=WEBHOOK_URL)
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

    asyncio.run(run())
