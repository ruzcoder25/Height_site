from django.db import models
from common.models import BaseModel


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
    MORNING =  "09:00-12:00","09-12"
    MIDDAY =  "12:00-15:00","12-15"
    AFTERNOON = "15:00-18:00","15-18"
    EVENING =  "18:00-21:00","18-21"
    ANY_TIME = "Istalgan vaqtda","anytime"

class MonthChoices(models.TextChoices):
    JANUARY = "yanvar", "Yanvar"
    FEBRUARY = "fevtal", "Fevral"
    MARCH = "mart", "Mart"
    APRIL = "aprel", "Aprel"
    MAY = "may", "May"
    JUNE = "iyun", "Iyun"
    JULY = "iyul", "Iyul"
    AUGUST = "avgust", "Avgust"
    SEPTEMBER = "sentabr", "Sentabr"
    OCTOBER = "oktabr", "Oktabr"
    NOVEMBER = "noyabr", "Noyabr"
    DECEMBER = "dekabr", "Dekabr"

class Contacts(BaseModel):
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

    # Oy TextChoices bilan
    month = models.CharField(
        max_length=10,
        choices=MonthChoices.choices,
        blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)

    # Yil avtomatik
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'contacts'
        ordering = ('-created_at',)

    def __str__(self):
        return self.full_name

