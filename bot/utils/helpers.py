# bot/utils/helpers.py
def format_lead_info(lead: dict) -> str:
    """Lead ma'lumotlarini chiroyli formatlash"""
    user_id = lead.get('id', '---')
    name = lead.get('full_name', '---')
    phone = lead.get('phone_number', '---')
    business = lead.get('business_name', '---')
    status = lead.get('status_led', '---')
    service_type = lead.get('service_type', '---')
    user_comment = lead.get('user_comment', '---')
    operator_comment = lead.get('operator_comment', '---')

    text = (
        f"🆔 ID: {user_id}\n"
        f"👤 Ism: {name}\n"
        f"📞 Telefon: {phone}\n"
        f"🏢 Biznes: {business}\n"
        f"📌 Status: {status}\n"
        f"🛠️ Hizmat turi: {service_type}\n"
        f"💬 User izohi: {operator_comment}\n"
        f"💬 Operator izohi: {user_comment}\n"
    )
    return text
