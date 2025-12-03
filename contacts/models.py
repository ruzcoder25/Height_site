from django.db import models


class ServiceTypeChoices(models.TextChoices):
    WEB_SITE = 'web site', 'Web Site'
    WEB_DASTURLASH = 'web dasturlash', 'Web Dasturlash'
    MOBIL_DASTURLASH = 'mobil va desctop ilovalar', 'Mobil Va Desctop Ilovalar'
    TELEGRAM_BOT = 'telegram bot', 'Telegram Bot'


class StatusChoices(models.TextChoices):
    NEW_LED = 'new led', 'New Led'
    LATER = 'later', 'Later'
    FAILED = 'failed', 'Failed'


class CallTimeChoices(models.TextChoices):
    MORNING = "09-12", "Ertalab 9 dan 12 gacha"
    MIDDAY = "12-15", "12 dan 15 gacha"
    AFTERNOON = "15-18", "15 dan 18 gacha"
    EVENING = "18-21", "18 dan 21 gacha"
    ANY_TIME = "any", "Istalgan vaqtda"

class Contacts(models.Model):
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    business_name = models.CharField(max_length=200)
    user_comment = models.TextField(blank=True, null=True)
    service_type = models.CharField(
        max_length=50,
        choices=ServiceTypeChoices.choices,
        blank=True, null=True
    )
    status_led = models.CharField(
        max_length=50,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW_LED
    )
    call_time = models.CharField(
        max_length=50,
        choices=CallTimeChoices.choices,
        default=CallTimeChoices.ANY_TIME
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contacts'
        ordering = ('-created_at',)

    def __str__(self):
        return self.full_name

