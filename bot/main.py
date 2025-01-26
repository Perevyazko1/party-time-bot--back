import asyncio
import json
import os
import re
import sqlite3 as sq

from aiogram import Bot, Dispatcher
from aiogram import executor
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.web_app_info import WebAppInfo
from dotenv import load_dotenv
from aiogram.utils.markdown import hbold


load_dotenv()
bot = Bot(token=os.getenv('TOKEN_BOT'))
dp = Dispatcher(bot, storage=MemoryStorage())



@dp.message_handler(commands="start")
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    start_data = message.get_args()
    markup.add(types.InlineKeyboardButton("open",web_app=WebAppInfo(url=f"https://perevyazko1.github.io/party-time-bot-front-new/#event/{start_data}")))
    "https://api.telegram.org/file/bot7524073074:AAEOaVQ86O5knm_67Oy3MY-49l2O_fLPVGE/photos/file_0.jpg"
    start_data = message.get_args()  # Получаем данные из параметра start
    if start_data:
        await message.answer(f'Для выбора даты события нажми кнопку.', reply_markup=markup)


@dp.message_handler(commands="create_event")
async def create_event(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("открыть страницу записи",
                                    web_app=WebAppInfo(url=f"https://perevyazko1.github.io/party-time-bot-front-new/#create_event")))
    await message.answer(f'запись 👇', reply_markup=markup)


@dp.message_handler(content_types=['web_app_data'])
async def web_app(message: types.Message):
    data = json.loads(message.web_app_data.data)
    print(data)
    await message.answer(f'https://t.me/time_party_Bot?start={data}')


@dp.message_handler(commands="create_meeting")
async def reply_to_manager(message: types.Message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("открыть форму запроса",
                                    web_app=WebAppInfo(
                                        url=f"https://perevyazko1.github.io/party-time-bot-front-new/")))
    await message.answer(f'Отлично! Теперь нажми кнопку для заполнения формы 👇',
                                          reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp)
