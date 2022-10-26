import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from config import token

BOT_TOKEN = token
button_game = KeyboardButton('Играть!')
button_help = KeyboardButton('Помочь с игрой!')

start_buttons = ReplyKeyboardMarkup(resize_keyboard = True,
        one_time_keyboard = True)
start_buttons.add(button_game,button_help)
bot = Bot(token=BOT_TOKEN, parse_mode ='HTML')
dp = Dispatcher(bot=bot)


#print(dir(start_buttons))
#print(start_buttons.values['keyboard'][0][0]['text'])
