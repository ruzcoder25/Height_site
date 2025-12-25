from rest_framework import serializers
from .models import Contacts, StatusChoices
import re


# ============================
# CREATE CONTACT (SITE)
# ============================
class CreateContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = [
            'full_name',
            'phone_number',
            'business_name',
            'service_type',
            'status_led',
            'call_time',
        ]

    def validate_full_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Full name bo‘sh bo‘lishi mumkin emas.")
        if len(value) > 100:
            raise serializers.ValidationError("Full name 100 belgidan oshmasligi kerak.")
        return value

    def validate_status_led(self, value):
        valid_status = [choice.value for choice in StatusChoices]
        if value not in valid_status:
            raise serializers.ValidationError(
                f"Status faqat quyidagilardan biri bo‘lishi mumkin: {', '.join(valid_status)}"
            )
        return value

    def validate_phone_number(self, value):
        # O‘zbekiston telefon raqamlari uchun
        pattern = r'^(?:\+?998|0)?9\d{8}$'

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Telefon raqam noto‘g‘ri. Masalan: 991234567, 998991234567, +998991234567"
            )
        return value


# ============================
# LIST / RETRIEVE
# ============================
class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = [
            'id',
            'full_name',
            'phone_number',
            'business_name',
            'user_comment',
            'service_type',
            'status_led',
            'call_time',
            'month',
            'day',
            'year',
            'created_at',
        ]


# ============================
# UPDATE STATUS (CRM)
# ============================
class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = [
            'status_led',
            'user_comment',
            'call_time',
            'month',
            'day',
            'year',
        ]

    def validate_status_led(self, value):
        allowed_status = [
            StatusChoices.LATER.value,
            StatusChoices.FAILED.value,
            StatusChoices.SUCCESS.value,
        ]

        if value not in allowed_status:
            raise serializers.ValidationError(
                f"Status faqat quyidagilardan biri bo‘lishi mumkin: {', '.join(allowed_status)}"
            )
        return value


# ============================
# EXPORT TO EXCEL
# ============================
class ContactExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = [
            "full_name",
            "phone_number",
            "business_name",
            "service_type",
            "status_led",
            "call_time",
            "month",
            "day",
            "year",
            "user_comment",
            "created_at",
        ]
