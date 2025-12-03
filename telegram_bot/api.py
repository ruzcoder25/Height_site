import aiohttp
from decouple import config

BOT_HOST = config("BOT_HOST")
BASE_URL = f"{BOT_HOST}/api/v1/contacts/"

async def get_new_leads():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL + "new_leds/") as resp:
            if resp.status == 200:
                return await resp.json()
            return []

async def get_later_leads():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL + "later/") as resp:
            if resp.status == 200:
                return await resp.json()
            return []


async def update_lead(
        lead_id: int,
        status_led: str = None,
        user_comment: str = None,
        call_time: str = None
        ):

    payload = {}
    if status_led is not None:
        payload['status_led'] = status_led
    if user_comment is not None:
        payload['user_comment'] = user_comment
    if call_time is not None:
        payload['call_time'] = call_time

    if not payload:
        return {"success": False, "message": "Yangilash uchun ma'lumot berilmadi"}

    async with aiohttp.ClientSession() as session:
        async with session.patch(f"{BASE_URL}{lead_id}/", json=payload) as resp:
            if resp.status in (200, 204):
                return {"success": True, "message": "Lead yangilandi"}
            return {"success": False, "message": f"Xato: {resp.status}"}
