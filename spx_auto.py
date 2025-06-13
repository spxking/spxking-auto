import requests
import time
import os
import openai
from telegram import Bot

# إعدادات
symbol = "SPX500"
interval = 180  # كل 3 دقائق
openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("CHAT_ID")

bot = Bot(token=telegram_token)

def fetch_price():
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=.INX&interval=1min&apikey=demo"
    try:
        r = requests.get(url)
        data = r.json()
        latest = list(data["Time Series (1min)"].values())[0]
        return float(latest["4. close"])
    except Exception as e:
        return None

def analyze(price):
    msg = f"🔍 Webhook Signal:\nSymbol: {symbol}\nPrice: {price}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "أنت مساعد مالي ذكي، حلل السوق وقرر: شراء، بيع، أو انتظار."},
            {"role": "user", "content": msg}
        ]
    )
    reply = response["choices"][0]["message"]["content"]
    return reply

def send_alert(message):
    bot.send_message(chat_id=chat_id, text=message)

while True:
    price = fetch_price()
    if price:
        recommendation = analyze(price)
        send_alert(f"📊 السعر: {price}\n📣 التوصية: {recommendation}")
    time.sleep(interval)