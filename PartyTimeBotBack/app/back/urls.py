from django.urls import path

from back.views import create_user, create_event, get_event,create_cabinet_user, add_date, get_advertising, get_advertising_item

urlpatterns = [
    path('create_user/', create_user),
    path('create_event/', create_event),
    path('get_event/', get_event),
    path('create_cabinet_user/', create_cabinet_user),
    path('add_date/', add_date),
    path('get_advertising/', get_advertising),
    path('get_advertising_item/<int:id>/', get_advertising_item),
]


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