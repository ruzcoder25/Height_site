import os
from dotenv import load_dotenv

# .env faylini yuklash
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Bot token
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# API endpoints
API_BASE_URL = os.getenv("API_BASE_URL", "http://host.docker.internal:8000/api/v1")
API_LOGIN = f"{API_BASE_URL}/accounts/login/"
API_LEADS_NEW = f"{API_BASE_URL}/contacts/new_leds/"
API_LEADS_LATER = f"{API_BASE_URL}/contacts/later/"
API_LEADS_UPDATE = f"{API_BASE_URL}/contacts/"
API_LEADS_COUNT = f"{API_BASE_URL}/contacts/counts/"

# Redis yoki session ma'lumotlari
# Bu yerda foydalanuvchi tokenlarini saqlash uchun
SESSION_STORAGE = {}