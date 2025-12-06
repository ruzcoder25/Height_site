from rest_framework import serializers
from .models import Contacts

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

class ImportContactsSerializer(serializers.Serializer):
    file = serializers.FileField()