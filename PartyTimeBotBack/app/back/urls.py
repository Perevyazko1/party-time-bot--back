from django.urls import path

from back.views import create_client, get_slots_reception, get_type_of_work

urlpatterns = [
    path('create_user/', create_user),
    path('create_event/', create_event),
    path('add_date/', add_date),]


"""
    Создание юзера (telegram_name?,telegram_id, date_subscribe,first_name?,last_name?,birthday?,)
    Запись телефона (phone)
    Запись обо мне (about_me)


    Создание события (id_party, type_event)
    Добавление юзеров (user)
    Добавление удобной даты (best_dates)
    Добавление неудобной даты (worst_dates)
    Загрузка картинки (img_event)
    Загрузка описания (about_event)

    Получение рекламных мест(картинка, ссылка на сайт с счетчиком перехода, текст, счетчик просмотров )



"""