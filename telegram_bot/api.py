import aiohttp
from decouple import config

BOT_HOST = config("BOT_HOST")  # .env dan olinadi
BASE_URL = f"{BOT_HOST}/api/v1/contacts/"



async def server_alive() -> bool:
    """Server ishlayotganini tekshiradi"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL) as resp:
                return resp.status in (200, 301, 302)
    except:
        return False



async def get_new_leads():
    """Yangi leadlarni olish"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL + "new_leds/") as resp:
                if resp.status == 200:
                    return await resp.json()
                return {"success": False, "message": f"Server javobi: {resp.status}"}

    except aiohttp.ClientConnectorError:
        return {"success": False, "message": "❌ Serverga ulanish imkoni yo'q. Backend ishga tushganini tekshiring."}
    except Exception as e:
        return {"success": False, "message": f"❗ Kutilmagan xatolik: {e}"}


async def get_later_leads():
    """Qayta qo'ng'iroq uchun qoldirilgan leadlar"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL + "later/") as resp:
                if resp.status == 200:
                    return await resp.json()
                return {"success": False, "message": f"Server javobi: {resp.status}"}

    except aiohttp.ClientConnectorError:
        return {"success": False, "message": "❌ Serverga ulanish imkoni yo'q"}
    except Exception as e:
        return {"success": False, "message": f"❗ Xatolik: {e}"}



async def update_lead(
        lead_id: int,
        status_led: str = None,
        user_comment: str = None,
        call_time: str = None
):
    """Lead malumotlarini update qilish"""

    payload = {}
    if status_led: payload["status_led"] = status_led
    if user_comment: payload["user_comment"] = user_comment
    if call_time: payload["call_time"] = call_time

    if not payload:
        return {"success": False, "message": "⚠ Yangilash uchun maydon berilmagan"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.patch(f"{BASE_URL}{lead_id}/", json=payload) as resp:
                if resp.status in (200, 204):
                    return {"success": True, "message": "✅ Lead muvaffaqiyatli yangilandi"}
                return {"success": False, "message": f"❌ Xato! Server status: {resp.status}"}

    except aiohttp.ClientConnectorError:
        return {"success": False, "message": "🔌 Serverga ulanib bo‘lmadi"}
    except Exception as e:
        return {"success": False, "message": f"❗ Xatolik: {e}"}
