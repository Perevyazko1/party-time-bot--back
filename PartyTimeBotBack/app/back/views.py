from django.shortcuts import render
from datetime import datetime
from .models import CustomUser,DateEvent,PartyEvent
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import (PartyEventSerializer)


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
    
    Получение удобных и не удобных дат юзеров
    Получение юзера?
    Получение события



"""


@api_view(['POST'])
def create_user(request):
    try:

        telegram_id = request.data['telegram_id']
        telegram_name = request.data.get('telegram_name')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone = request.data.get('phone')
        birthday = request.data.get('birthday')
        about_me = request.data.get('about_me')

        if not telegram_id:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'result': 'Telegram ID is required'})

        defaults = {}
        if telegram_name is not None:
            defaults['telegram_name'] = telegram_name
        if first_name is not None:
            defaults['first_name'] = first_name
        if last_name is not None:  # Проверка на None, а не на пустую строку
            defaults['last_name'] = last_name
        if birthday is not None:  # Проверка на None, а не на пустую строку
            defaults['birthday'] = birthday
        if phone is not None:  # Проверка на None, а не на пустую строку
            defaults['phone'] = phone
        if about_me is not None:  # Проверка на None, а не на пустую строку
            defaults['about_me'] = about_me

        user, created = CustomUser.objects.update_or_create(
            telegram_id=telegram_id,
            defaults=defaults
        )
        if created:
            result = f'Успешно создан новый пользователь {telegram_id}!'
        else:
            result = f'Успешно обновлен пользователь {telegram_id}!'
        return Response(status=status.HTTP_200_OK, data={'result': result})

    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'result': f'Ошибка обновления данных, перепроверьте данные! {e}'})


@api_view(['PATCH'])
def update_event(request):
    try:
        user_id = request.data.get('telegram_id')
        id_party = request.data['id_party']
        about_event = request.data.get('about_event')
        type_event = request.data.get('type_event')
        img_event = request.FILES.get('img_event')
        user = CustomUser.objects.get(telegram_id=user_id,)
        if not user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'result': 'Telegram ID is required'})
        if not id_party:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'result': 'id_party is required'})

        defaults = {}
        if id_party is not None:
            defaults['id_party'] = id_party
        if about_event is not None:
            defaults['about_event'] = about_event
        if type_event is not None:
            defaults['type_event'] = type_event
        if img_event:
            defaults['img_event'] = img_event
        if user :
            defaults['user'] = user


        event, created = PartyEvent.objects.update_or_create(
            id_party=id_party,
            defaults=defaults
        )
        if created:
            result = {
                'result': f"Успешно {'создано' if created else 'обновлено'} событие!",
                'id_party': str(event.id_party),  # Возвращаем UUID в виде строки
            }
        else:
            result = f'Успешно обновлено событие {created}!'
        return Response(status=status.HTTP_200_OK, data={'result': result})

    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'result': 'User not found'})

    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'result': f'Ошибка обновления данных, перепроверьте данные! {e}'})
@api_view(['POST'])
def create_event(request):
    try:
        about_event = request.data.get('about_event')
        type_event = request.data.get('type_event')
        img_event = request.FILES.get('img_event')



        defaults = {}
        if about_event is not None:
            defaults['about_event'] = about_event
        if type_event is not None:
            defaults['type_event'] = type_event
        if img_event:
            defaults['img_event'] = img_event



        event, created = PartyEvent.objects.create(
            defaults=defaults
        )
        if created:
            result = {
                'result': f"Успешно {'создано' if created else 'обновлено'} событие!",
                'id_party': str(event.id_party),  # Возвращаем UUID в виде строки
            }
        else:
            result = f'Успешно обновлено событие {created}!'
        return Response(status=status.HTTP_200_OK, data={'result': result})



    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'result': f'Ошибка обновления данных, перепроверьте данные! {e}'})


@api_view(['POST'])
def add_date(request):
    try:
        best_dates_str = request.data.getlist('best_dates')
        worst_dates_str = request.data.getlist('worst_dates') # getlist для получения списка дат
        event_id = request.data.get('event_id')

        if not event_id:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'result': 'event_id is required'})

        event = PartyEvent.objects.get(id_party=uuid.UUID(event_id)) #Преобразование event_id в UUID

        if best_dates_str:
            best_dates_objects = []
            for date_str in best_dates_str:
                try:
                    date_obj = DateEvent.objects.get_or_create(date_event=datetime.strptime(date_str, '%Y-%m-%d').date())[0]
                    best_dates_objects.append(date_obj)
                except ValueError:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={'result': 'Invalid best_dates format. Use YYYY-MM-DD'})
            event.best_dates.add(*best_dates_objects)


        if worst_dates_str:
            worst_dates_objects = []
            for date_str in worst_dates_str:
                try:
                    date_obj = DateEvent.objects.get_or_create(date_event=datetime.strptime(date_str, '%Y-%m-%d').date())[0]
                    worst_dates_objects.append(date_obj)
                except ValueError:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={'result': 'Invalid worst_dates format. Use YYYY-MM-DD'})
            event.worst_dates.add(*worst_dates_objects)


        result = f'Успешно обновлено событие {event_id}!'
        return Response(status=status.HTTP_200_OK, data={'result': result})

    except PartyEvent.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'result': 'PartyEvent not found'})
    except ValueError as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'result': f'Ошибка валидации данных: {e}'})
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'result': f'Ошибка обновления данных: {e}'})



@api_view(['GET'])
def get_event(request):
    try:
        # Используем query_params вместо request.data для GET-запроса
        id_party = request.query_params.get('id_party')
        if not id_party:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'result': 'id_party is required'},
            )

        # Получение события
        queryset = PartyEvent.objects.filter(id_party=id_party)
        if not queryset.exists():
            return Response(
                {"error": f"Событие с id_party {id_party} не найдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Сериализация данных
        serializer_party_event = PartyEventSerializer(queryset, many=True)
        return Response(serializer_party_event.data, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response(
            {"error": f"Произошла ошибка: {e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )