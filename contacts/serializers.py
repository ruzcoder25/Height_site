from rest_framework import serializers
from .models import Contacts, StatusChoices
import re
from datetime import datetime

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
            raise serializers.ValidationError("Full name bo'sh bo'lishi mumkin emas.")
        if len(value) > 100:
            raise serializers.ValidationError("Full name 100 belgidan oshmasligi kerak.")
        return value

    def validate_status_led(self, value):
        valid_status = [choice.value for choice in StatusChoices]
        if value not in valid_status:
            raise serializers.ValidationError(
                f"Status faqat quyidagilardan biri bo'lishi mumkin: {', '.join(valid_status)}")
        return value

    def validate_phone_number(self, value):

        # O'zbekiston raqamlarini qabul qiluvchi regex
        # 9xx yagonal mobil raqam, optional +998 yoki 998 prefiks
        pattern = r'^(?:\+?998|0)?9\d{8}$'

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Telefon raqam noto'g'ri. Masalan: 991234567, 998991234567, +998991234567"
            )
        return value

    # def validate_call_time(self, value):
    #     """
    #     Call time faqat hozirgi yoki keyingi vaqt bo'lishi kerak
    #     """
    #     if value < datetime.now():
    #         raise serializers.ValidationError("Call time hozirgi yoki keyingi vaqt bo'lishi kerak.")
    #     return value

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
        ]

    from rest_framework import serializers
    from datetime import datetime
    from .models import Contacts, StatusChoices

    class UpdateStatusSerializer(serializers.ModelSerializer):
        class Meta:
            model = Contacts
            fields = [
                'status_led',
                'user_comment',
                'call_time',
                'month',
                'day',
                'year'
            ]

        def validate_status_led(self, value):
            allowed_status = [
                StatusChoices.LATER,
                StatusChoices.FAILED,
                StatusChoices.SUCCESS
            ]
            if value not in allowed_status:
                raise serializers.ValidationError(
                    f"Status faqat quyidagilardan biri bo'lishi mumkin: {', '.join(allowed_status)}"
                )
            return value

        def validate_call_time(self, value):
            """
            call_time faqat hozirgi yoki keyingi vaqt bo'lishi kerak
            """
            if value:
                # Agar call_time CharField bo‘lsa, uni datetime ga parse qilish kerak
                try:
                    call_dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    raise serializers.ValidationError("Call time format noto‘g‘ri. Masalan: 'YYYY-MM-DD HH:MM:SS'")

                if call_dt < datetime.now():
                    raise serializers.ValidationError("Call time hozirgi yoki keyingi vaqt bo'lishi kerak.")
            return value

        def validate(self, attrs):
            """
            call_time ga mos ravishda month, day va year tekshirish
            """
            call_time = attrs.get('call_time')
            month = attrs.get('month')
            day = attrs.get('day')
            year = attrs.get('year')

            if call_time:
                call_dt = datetime.strptime(call_time, "%Y-%m-%d %H:%M:%S")

                if month and month != str(call_dt.month):
                    raise serializers.ValidationError("Month call_time ga mos kelishi kerak.")
                if day and day != call_dt.day:
                    raise serializers.ValidationError("Day call_time ga mos kelishi kerak.")
                if year and year != call_dt.year:
                    raise serializers.ValidationError("Year call_time ga mos kelishi kerak.")

            return attrs


# class ImportContactsSerializer(serializers.Serializer):
#     file = serializers.FileField()


class ContactExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = [
            "full_name", "phone_number", "business_name",
            "service_type", "status_led", "call_time", "month",
            "day", "year", "user_comment", "created_at"
        ]