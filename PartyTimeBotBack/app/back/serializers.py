from rest_framework import serializers
from back.models import CustomUser, UserCabinet, PartyEvent, Advertising, UserDate, AdvertisingPicture


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id',
                  'last_login',
                  'username',
                  'telegram_name',
                  'telegram_id',
                  'phone',
                  'first_name',
                  'last_name',
                  'birthday',
                  'img_url',
                  ]


class AdvertisingPictureSerializer(serializers.ModelSerializer):
    picture_url = serializers.SerializerMethodField()

    class Meta:
        model = AdvertisingPicture
        fields = ['id', 'picture_url']

    def get_picture_url(self, obj):
        request = self.context.get('request')
        if obj.picture:
            return request.build_absolute_uri(obj.picture.url)
        return None


class AdvertisingSerializer(serializers.ModelSerializer):
    pictures = AdvertisingPictureSerializer(many=True, read_only=True)  # Указываем вложенный сериализатор

    class Meta:
        model = Advertising
        fields = '__all__'


class UserDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDate
        fields = ['id', 'best_dates', 'worst_dates']


class UserCabinetSerializer(serializers.ModelSerializer):
    dates = UserDateSerializer(many=True, read_only=True)  # Связь с UserDate через related_name
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserCabinet
        fields = ['id', 'user', 'dates']  # Добавляем поле 'dates' для связи


class EventsSerializer(serializers.ModelSerializer):
    users = UserCabinetSerializer(many=True, read_only=True)  # Вложенные кабинеты пользователей

    class Meta:
        model = PartyEvent
        fields = ['id_party', 'about_event', 'type_event', 'img_event', 'users', 'id_tg_create_user', 'address',
                  'id_tg_create_user']


class PartyEventSerializer(serializers.ModelSerializer):
    users = UserCabinetSerializer(many=True, read_only=True)  # Вложенные кабинеты пользователей

    class Meta:
        model = PartyEvent
        fields = ['id_party', 'about_event', 'type_event', 'img_event', 'users', 'id_tg_create_user', 'address',
                  'id_tg_create_user']
