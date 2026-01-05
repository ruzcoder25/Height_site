# models.py
from django.db import models
from common.models import BaseModel
from django.utils.translation import gettext_lazy as _


class ServiceTypeChoices(models.TextChoices):
    CONSULTATION = 'consultation', _('Consultation')
    WEBSITE = 'website', _('Website')
    LANDING_PAGE = 'landing_page', _('Landing Page')
    MOBILE_APP = 'mobile_app', _('Mobile Application')
    ERP = 'erp_system', _('ERP System')
    TELEGRAM_BOT = 'telegram_bot', _('Telegram Bot')
    SUPPORT_BOT = 'support_bot', _('Support Bot')


class StatusChoices(models.TextChoices):
    NEW_LED = 'new_led', _('New Lead')
    LATER = 'later', _("Call Back Later")
    FAILED = 'failed', _('Service Not Needed')
    SUCCESS = 'success', _('Using Our Services')


class SourceChoices(models.TextChoices):
    INSTAGRAM = 'instagram', _('Via Instagram')
    GOOGLE = 'google', _('Via Google')
    FRIENDS = 'friends', _('Via Friends')
    TELEGRAM = 'telegram', _('Via Telegram')


class CallTimeChoices(models.TextChoices):
    MORNING = "09:00-12:00", _("09:00-12:00")
    MIDDAY = "12:00-15:00", _("12:00-15:00")
    AFTERNOON = "15:00-18:00", _("15:00-18:00")
    EVENING = "18:00-21:00", _("18:00-21:00")
    ANY_TIME = "anytime", _("Call Anytime")


class MonthChoices(models.TextChoices):
    JANUARY = "yanvar", _("January")
    FEBRUARY = "fevral", _("February")
    MARCH = "mart", _("March")
    APRIL = "aprel", _("April")
    MAY = "may", _("May")
    JUNE = "iyun", _("June")
    JULY = "iyul", _("July")
    AUGUST = "avgust", _("August")
    SEPTEMBER = "sentabr", _("September")
    OCTOBER = "oktabr", _("October")
    NOVEMBER = "noyabr", _("November")
    DECEMBER = "dekabr", _("December")


class Contacts(BaseModel):
    full_name = models.CharField(max_length=200, verbose_name=_('Full Name'))
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone Number'))
    business_name = models.CharField(max_length=200, verbose_name=_('Business Name'))
    user_comment = models.TextField(blank=True, null=True, verbose_name=_('User Comment'))
    operator_comment = models.TextField(blank=True, null=True, verbose_name=_('Operator Comment'))
    source = models.CharField(
        max_length=20,
        choices=SourceChoices.choices,
        null=True,
        blank=True,
        verbose_name=_('Source')
    )
    service_type = models.CharField(
        max_length=50,
        choices=ServiceTypeChoices.choices,
        blank=True, null=True,
        verbose_name=_('Service Type')
    )
    status_led = models.CharField(
        max_length=50,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW_LED,
        verbose_name=_('Lead Status')
    )
    call_time = models.CharField(
        max_length=50,
        choices=CallTimeChoices.choices,
        default=CallTimeChoices.ANY_TIME,
        verbose_name=_('Call Time')
    )
    month = models.CharField(
        max_length=10,
        choices=MonthChoices.choices,
        blank=True, null=True,
        verbose_name=_('Month')
    )
    day = models.IntegerField(blank=True, null=True, verbose_name=_('Day'))
    year = models.IntegerField(blank=True, null=True, verbose_name=_('Year'))

    class Meta:
        db_table = 'contacts'
        ordering = ('-created_at',)
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    def __str__(self):
        return self.full_name