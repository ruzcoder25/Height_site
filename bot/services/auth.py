import aiohttp
from bot.config import API_LOGIN, SESSION_STORAGE


async def login_user(username: str, password: str) -> dict:
    """
    Foydalanuvchini tizimga kiritish

    Returns:
        dict: {'success': bool, 'token': str, 'role': str, 'message': str}
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    API_LOGIN,
                    json={"username": username, "password": password}
            ) as response:
                print("services/auth.py  respons : ",response)
                if response.status == 200:
                    data = await response.json()
                    return {
                        'success': True,
                        'token': data.get('access_token'),
                        'role': data.get('role', 'USER'),
                        'message': 'Login muvaffaqiyatli'
                    }
                else:
                    return {
                        'success': False,
                        'token': None,
                        'role': None,
                        'message': 'Login yoki parol xato'
                    }
    except Exception as e:
        return {
            'success': False,
            'token': None,
            'role': None,
            'message': f'Xatolik yuz berdi: {str(e)}'
        }


def save_user_session(user_id: int, token: str, role: str):
    """Foydalanuvchi sessiyasini saqlash"""
    SESSION_STORAGE[user_id] = {
        'token': token,
        'role': role,
        'current_lead_index': 0,
        'current_lead_type': None  # 'new' yoki 'later'
    }


def get_user_session(user_id: int) -> dict:
    """Foydalanuvchi sessiyasini olish"""
    return SESSION_STORAGE.get(user_id)


def clear_user_session(user_id: int):
    """Foydalanuvchi sessiyasini o'chirish"""
    if user_id in SESSION_STORAGE:
        del SESSION_STORAGE[user_id]


def is_authenticated(user_id: int) -> bool:
    """Foydalanuvchi tizimga kirganmi tekshirish"""
    return user_id in SESSION_STORAGE