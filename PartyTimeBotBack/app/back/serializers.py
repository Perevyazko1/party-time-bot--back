from rest_framework import serializers
from back.models import CustomUser, DateEvent, PartyEvent, Advertising


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class DateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateEvent
        fields = '__all__'


class PartyEventSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(many=True, read_only=True)
    best_dates = DateEventSerializer(many=True, read_only=True)
    worst_dates = DateEventSerializer(many=True, read_only=True)

    class Meta:
        model = PartyEvent
        fields = [
                'id_party',
                'about_event',
                'user',
                'best_dates',
                'worst_dates',
                'type_event'
                  ]

class AdvertisingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertising
        fields = '__all__'