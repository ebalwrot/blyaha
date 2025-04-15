import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("API_KEY")

SYMBOLS = {
    "sp500": "SPX",
    "nas100": "NDX"
}

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я бот для расчёта лота по индексам.\n\n"
        "Используй команду:\n"
        "/lot индекс депозит риск стоплосс\n\n"
        "Пример:\n"
        "/lot sp500 1000 2 20"
    )

async def lot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        _, symbol, deposit, risk, stop_loss = update.message.text.strip().split()
        deposit = float(deposit)
        risk = float(risk)
        stop_loss = float(stop_loss)

        if symbol not in SYMBOLS:
            await update.message.reply_text("⚠️ Поддерживаются только: sp500 и nas100")
            return

        price = get_price(SYMBOLS[symbol])
        if not price:
            await update.message.reply_text("❌ Ошибка получения цены с API.")
            return

        risk_amount = deposit * (risk / 100)
        point_value = 0.01  # Это может меняться у разных брокеров
        lot = round(risk_amount / (stop_loss * point_value), 2)

        await update.message.reply_text(
            f"📊 Индекс: {symbol.upper()}\n"
            f"💰 Цена: {price}\n"
            f"💼 Депозит: ${deposit}\n"
            f"📉 Риск: {risk}%\n"
            f"📏 Стоп-лосс: {stop_loss} пунктов\n"
            f"✅ Рекомендуемый лот: {lot}"
        )
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("⚠️ Проверь формат команды. Пример: /lot sp500 1000 2 20")

def get_price(symbol: str):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        response = requests.get(url).json()
        return float(response['price'])
    except:
        return None

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lot", lot))
    app.run_polling()
