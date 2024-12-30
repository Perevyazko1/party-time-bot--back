from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
import uuid


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    telegram_name = models.CharField('telegram_name', max_length=100, blank=True)
    telegram_id = models.CharField('telegram_id', max_length=100, unique=True)
    phone = models.CharField('номер телефона', max_length=100, blank=True)
    date_subscribe = models.DateField('дата регистрации', default=timezone.now)
    status_pay = models.CharField('статус оплаты', max_length=100, blank=True)
    name_organization = models.CharField('название организации', max_length=100, blank=True)
    first_name = models.CharField('имя', max_length=100, blank=True)
    last_name = models.CharField('фамилия', max_length=100, blank=True)
    birthday = models.CharField('день рождения', max_length=100, blank=True)
    about_me = models.CharField('обо мне',max_length=100, blank=True)
    img_url = models.CharField('img_url' ,max_length=100, blank=True)


class PartyEvent(models.Model):
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'Событие'

    id_party = models.UUIDField('ID события',primary_key=True, default=uuid.uuid4, editable=False)
    about_event = models.CharField('О событии', max_length=500)
    user = models.ManyToManyField('CustomUser', blank=True, null=True ,related_name='events')


    type_event = models.CharField(max_length=100)
    img_event = models.ImageField(upload_to='event_images/', blank=True, null=True)


class UserCabinet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='event')
    event = models.ForeignKey(PartyEvent, on_delete=models.CASCADE, related_name='users')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'event'], name='unique_user_cabinet')
        ] # Уникальная пара (user, cabinet)

    def __str__(self):
        return f"{self.user} - {self.cabinet}"


class UserDate(models.Model):
    user_cabinet = models.ForeignKey(UserCabinet, on_delete=models.CASCADE, related_name='dates')
    best_dates = ArrayField(
        models.DateField(),
        blank=True,
        default=list
    )
    worst_dates = ArrayField(
        models.DateField(),
        blank=True,
        default=list
    )


    def __str__(self):
        return f"{self.user_cabinet} - {self.date}"


class Notes(models.Model):
    user_cabinet = models.ForeignKey(UserCabinet, on_delete=models.CASCADE, related_name='notes')
    note_user = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.user_cabinet} - {self.date}"



class Advertising(models.Model):
    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Реклама'
    picture = models.ImageField(upload_to='advertising_pictures/')
    link_to_site = models.CharField('Ссылка на сайт', max_length=100)
    header_advertising = models.CharField('Заголовок рекламы', max_length=100)
    text_advertising = models.CharField('Текст рекламы', max_length=500)
    count_view = models.IntegerField(default=0)