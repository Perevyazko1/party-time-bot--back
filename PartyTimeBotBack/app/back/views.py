from datetime import datetime
from .models import CustomUser,PartyEvent, UserCabinet, UserDate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import (PartyEventSerializer)
from django.db import IntegrityError


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

        # Создаем событие
        event = PartyEvent.objects.create(
            about_event=about_event if about_event is not None else "",
            type_event=type_event if type_event is not None else "",
            img_event=img_event if img_event else None
        )
        created = True  # При вызове create объект всегда создается

        # Формируем ответ
        result = {
            'result': f"Успешно {'создано' if created else 'обновлено'} событие!",
            'id_party': str(event.id_party),  # Возвращаем UUID в виде строки
        }

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'result': f'Ошибка обновления данных, перепроверьте данные! {e}'}
        )
@api_view(['POST'])
def create_cabinet_user(request):
    try:
        # Получаем данные из запроса
        telegram_id = request.data.get('telegram_id')
        event_id = request.data.get('event_id')

        if not telegram_id or not event_id:
            return Response({'error': 'telegram_id and event_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, существует ли пользователь с таким telegram_id
        user, created = CustomUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'username': f'telegram_{telegram_id}',  # Задаем уникальное имя пользователя
                'telegram_name': request.data.get('telegram_name', ''),
                'first_name': request.data.get('first_name', ''),
                'last_name': request.data.get('last_name', ''),
                'img_url': request.data.get('img_url', ''),

            }
        )

        if created:
            print(f"Создан новый пользователь с telegram_id: {telegram_id}")

        # Проверяем, существует ли событие
        try:
            event = PartyEvent.objects.get(id_party=event_id)
        except PartyEvent.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        # Создаем экземпляр UserCabinet
        user_cabinet, created_cabinet = UserCabinet.objects.get_or_create(
            user=user,
            event=event
        )

        if created_cabinet:
            print(f"Создан кабинет пользователя для user: {user} и event: {event}")

        return Response({
            'message': 'UserCabinet created successfully',
            'user_id': user.id,
            'event_id': event.id_party,
            'cabinet_id': user_cabinet.id

        }, status=status.HTTP_201_CREATED)

    except IntegrityError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def add_date(request):
    try:
        best_dates = request.data.get('best_dates', [])
        worst_dates = request.data.get('worst_dates', [])
        user_cabinet_id = request.data.get('user_cabinet_id')

        try:
            user_cabinet = UserCabinet.objects.get(id=user_cabinet_id)
        except UserCabinet.DoesNotExist:
            return Response(
                {'error': 'UserCabinet не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

            # Создаем или обновляем запись UserDate
        user_date, created = UserDate.objects.update_or_create(
            user_cabinet=user_cabinet,
            defaults={
                'best_dates': best_dates,
                'worst_dates': worst_dates
            }
        )

        # Формируем ответ
        return Response(
            {
                'message': 'Данные успешно сохранены',
                'user_date': {
                    'id': user_date.id,
                    'user_cabinet_id': user_cabinet_id,
                    'best_dates': user_date.best_dates,
                    'worst_dates': user_date.worst_dates,
                }
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': f'Ошибка при обработке данных: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


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
    
# def get_queryset(self):
#     user = self.request.user
#     event = self.request.event
#     return UserCabinet.objects.filter(user=user, event=event)
#
#
# @api_view(['POST'])
# def add_date(request):
#     about_event = request.data.get('about_event')
#     type_event = request.data.get('type_event')