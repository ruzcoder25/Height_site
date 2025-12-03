# import requests
# from decouple import config
#
# BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
# CHAT_ID = config('TELEGRAM_CHAT_ID')
#
# def send_telegram_message(text: str):
#     print('Heeeeeelllll')
#     url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
#     payload = {
#         "chat_id": CHAT_ID,
#         "text": text,
#         "parse_mode": "HTML"
#     }
#     try:
#         requests.post(url, data=payload, timeout=5)
#     except Exception as e:
#         print("Telegram Error:", e)
