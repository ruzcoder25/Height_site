import logging
import aiohttp

from bot.config import (
    API_LEADS_NEW,
    API_LEADS_LATER,
    API_LEADS_UPDATE,
    API_LEADS_COUNT
)

logger = logging.getLogger(__name__)


# ================== COUNTS ==================

async def get_new_leads_count(token: str) -> int:
    """Yangi leadlar sonini olish"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                API_LEADS_COUNT,
                headers={"Authorization": f"Bearer {token}"}
            ) as response:

                if response.status != 200:
                    return 0

                data = await response.json()
                return data.get("data", {}).get("new", 0)

    except Exception:
        logger.exception("get_new_leads_count xatolik")
        return 0


async def get_later_leads_count(token: str) -> int:
    """Later leadlar sonini olish"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                API_LEADS_COUNT,
                headers={"Authorization": f"Bearer {token}"}
            ) as response:

                if response.status != 200:
                    return 0

                data = await response.json()
                return data.get("data", {}).get("later", 0)

    except Exception:
        logger.exception("get_later_leads_count xatolik")
        return 0


# ================== LEADS LIST ==================

async def get_new_leads(token: str) -> list:
    """Yangi leadlarni olish"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                API_LEADS_NEW,
                headers={"Authorization": f"Bearer {token}"}
            ) as response:

                if response.status != 200:
                    return []

                data = await response.json()

                if data.get("success") and isinstance(data.get("data"), list):
                    return data["data"]

                return []

    except Exception:
        logger.exception("get_new_leads xatolik")
        return []


async def get_later_leads(token: str) -> list:
    """Later leadlarni olish"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                API_LEADS_LATER,
                headers={"Authorization": f"Bearer {token}"}
            ) as response:

                if response.status != 200:
                    return []

                data = await response.json()
                return data.get("data", [])

    except Exception:
        logger.exception("get_later_leads xatolik")
        return []


# ================== UPDATE LEAD ==================

async def update_lead(
    token: str,
    lead_id: int,
    status: str | None = None,
    comment: str | None = None,
    call_date: str | None = None
) -> bool:
    """Leadni yangilash"""
    payload = {}
    # print(f"Hello : {API_LEADS_UPDATE}{lead_id}")
    if status:
        payload["status_led"] = status

    if comment:
        payload["user_comment"] = comment

    if call_date:
        payload["call_time"] = call_date
    print(f"services/api.py payload : {payload}")
    if not payload:
        return False

    try:
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                f"{API_LEADS_UPDATE}{lead_id}",
                headers={"Authorization": f"Bearer {token}"},
                json=payload
            ) as response:

                return response.status == 200

    except Exception:
        logger.exception("update_lead xatolik")
        return False
