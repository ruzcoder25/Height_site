from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Contacts
from decouple import config
import requests

BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")
CHAT_ID = config("TELEGRAM_CHAT_ID")


@receiver(post_save, sender=Contacts)
def send_telegram_notification(sender, instance, created, **kwargs):
    if not created:
        return

    # Lead tartib raqami (model ID)
    lead_number = instance.id

    text = (
        f"🆕 <b>{lead_number} - Lead</b>\n\n"
        f"👤 Ism: <b>{instance.full_name}</b>\n"
        f"📞 Telefon: <b>{instance.phone_number}</b>\n"
        f"🏢 Biznes: {instance.business_name}\n"
        f"🛠 Xizmat: {instance.service_type}\n"
        f"🔵 Holat: {instance.status_led}\n"
        f"⏰ Qo‘ng‘iroq vaqti: {instance.call_time}\n"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print("Telegramga yuborishda xatolik:", e)
