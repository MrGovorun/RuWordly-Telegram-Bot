from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#import your bot token from config.py
from config import token
#import text for buttons
from text_message import text_message

BOT_TOKEN = token

#buttons initialization
button_game = KeyboardButton(text_message['play_button'])
button_help = KeyboardButton(text_message['help_button'])

#keyboards initialization
start_buttons = ReplyKeyboardMarkup(resize_keyboard = True,
        one_time_keyboard = True)
start_buttons.add(button_game,button_help)

#bot initialization
bot = Bot(token=BOT_TOKEN, parse_mode ='HTML')
dp = Dispatcher(bot=bot)
