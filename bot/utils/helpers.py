from datetime import datetime


def format_lead_info(lead: dict) -> str:
    """Lead ma'lumotlarini formatlash"""
    print(f"utils/helpers.py lead : {lead}")
    user_id = lead.get('id', '---')
    name = lead.get('full_name', '---')
    phone = lead.get('phone_number', '---')
    business = lead.get('business_name', '---')
    call_time = lead.get('call_time', '---')
    status = lead.get('status_led', '---')
    service_type = lead.get('service_type', '---')
    user_comment = lead.get('user_comment', '---')

    text = f"🆔 ID: {user_id}\n"
    text += f"👤 Ism: {name}\n"
    text += f"📞 Telefon: {phone}\n"
    text += f"🏢 Biznes: {business}\n"
    text += f"🕒 Qo'ng'iroq vaqti: {call_time}\n"
    text += f"📌 Status: {status}\n"
    text += f"🛠️ Hizmat turi: {service_type}\n"
    text += f"💬 Izoh: : {user_comment}"


    return text


def validate_date(date_str: str) -> bool:
    """Sana formatini tekshirish (YYYY.MM.DD)"""
    if date_str.lower() == 'skip':
        return True

    try:
        datetime.strptime(date_str, '%Y.%m.%d')
        return True
    except ValueError:
        return False


def format_date(date_str: str) -> str:
    """Sanani formatlash"""
    if date_str.lower() == 'skip':
        return None

    try:
        date_obj = datetime.strptime(date_str, '%Y.%m.%d')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return None