import requests

TELEGRAM_TOKEN = "8614576306:AAHeGBKSK3KC5DI6rFEyOgf-KLHUAL13Glc"
CHAT_ID = "156610060"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    return response.json()

result = send_telegram("🧪 Test riuscito! Il bot funziona correttamente.")
print(result)
