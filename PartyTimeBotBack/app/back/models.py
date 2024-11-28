from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'

    telegram_name = models.CharField('telegram_name', max_length=100)
    telegram_id = models.CharField('telegram_id', max_length=100, unique=True)
    phone = models.CharField('номер телефона', max_length=100)
    date_subscribe = models.DateField('дата регистрации', default=timezone.now)
    status_pay = models.CharField('статус оплаты', max_length=100)
    name_organization = models.CharField('название организации', max_length=100)
    first_name = models.CharField('имя', max_length=100)
    last_name = models.CharField('фамилия', max_length=100)
    birthday = models.CharField('день рождения', max_length=100)
    about_me = models.CharField('обо мне',max_length=100)

    class DateEvent(models.Model):
        class Meta:
            verbose_name = 'Дата события'
            verbose_name_plural = 'Дата события'

        date_event = models.DateField('дата регистрации', default=timezone.now)

    class PartyEvent(models.Model):
        class Meta:
            verbose_name = 'Разновидность работ'
            verbose_name_plural = 'Разновидность работ'

        id_party = models.UUIDField('ID события',primary_key=True, default=uuid.uuid4, editable=False)
        about_event = models.CharField('О событии', max_length=500)
        user = models.ManyToManyField(CustomUser, related_name='events')

        best_dates = models.ManyToManyField(DateEvent)
        worst_dates = models.ManyToManyField(DateEvent)
        type_event = models.CharField(max_length=100)
        img_event = models.ImageField(upload_to='event_images/')

    class Advertising(models.Model):
        class Meta:
            verbose_name = 'Реклама'
            verbose_name_plural = 'Реклама'
        picture = models.ImageField(upload_to='advertising_pictures/')
        link_to_site = models.CharField('Ссылка на сайт', max_length=100)
        header_advertising = models.CharField('Заголовок рекламы', max_length=100)
        text_advertising = models.CharField('Текст рекламы', max_length=500)
        count_view = models.IntegerField(default=0)