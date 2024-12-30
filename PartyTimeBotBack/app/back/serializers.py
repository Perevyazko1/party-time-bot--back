from rest_framework import serializers
from back.models import CustomUser, UserCabinet, PartyEvent, Advertising, UserDate


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'




class PartyEventSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(many=True, read_only=True)

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



class UserDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDate
        fields = ['id', 'user_cabinet', 'best_dates', 'worst_dates']


class UserCabinetSerializer(serializers.ModelSerializer):
    dates = UserDateSerializer(many=True, read_only=True)  # Связь с UserDate через related_name

    class Meta:
        model = UserCabinet
        fields = ['id', 'user', 'event', 'dates']  # Добавляем поле 'dates' для связи
