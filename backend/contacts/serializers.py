# serializers.py
from rest_framework import serializers
from .models import Contacts, StatusChoices
import re
from django.utils.translation import gettext_lazy as _


class CreateContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = [
            'full_name',
            'phone_number',
            'business_name',
            'service_type',
            'user_comment',
            'source',
        ]

    def validate_full_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(_("Full name cannot be empty."))
        if len(value) > 100:
            raise serializers.ValidationError(_("Full name must not exceed 100 characters."))
        return value

    def validate_status_led(self, value):
        valid_status = [choice.value for choice in StatusChoices]
        if value not in valid_status:
            raise serializers.ValidationError(
                _("Status must be one of: %(statuses)s") % {'statuses': ', '.join(valid_status)}
            )
        return value

    def validate_phone_number(self, value):
        if '-' in value:
            raise serializers.ValidationError(
                _("Phone number should not contain '-' character.")
            )

        cleaned = re.sub(r'[^\d+]', '', value)

        if cleaned.startswith('+'):
            digits = cleaned[1:]
        else:
            digits = cleaned

        if not digits.isdigit():
            raise serializers.ValidationError(
                _("Phone number has incorrect format.")
            )

        if len(digits) < 7 or len(digits) > 15:
            raise serializers.ValidationError(
                _("Phone number length must be between 7 and 15 digits.")
            )

        normalized = '+' + digits
        return normalized


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
                _("Status must be one of: %(statuses)s") % {'statuses': ', '.join(allowed_status)}
            )
        return value


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