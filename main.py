import logging
from random import choice

import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InputFile

from cls import UserTry, UserGame
from load_words import all_words
from bot_init import bot, dp, start_buttons
from text_message import text_message
from make_picture import create_image

#инициализация логера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#состояние сессии пользователя
user_help = {}
user_game = {}
user_state = {}

@dp.message_handler(commands=['start'])
async def start_screen(message: types.Message):
    logger.info(f'User {message.from_user.full_name} start bot')
    await bot.send_message(message.from_id,
            text_message['button_ask'],
            reply_markup = start_buttons)

@dp.message_handler(commands=['help'])
async def greeting(message: types.Message):
    logger.info(f'{message.from_user.full_name} get help')
    await bot.send_message(message.from_id,
            text_message['help'])

@dp.message_handler(commands=['rules'])
async def rules(message: types.Message):
    logger.info(f'{message.from_user.full_name} get rules')
    await bot.send_message(message.from_id,
            text_message['rules'])

@dp.message_handler(commands=['restart'])
async def restart(message: types.Message):
    logger.info(f'User {message.from_user.full_name} restart the game')
    user_help[message.from_id] = UserTry(all_words)
    user_game[message.from_id] = UserGame(get_word())
    user_state[message.from_id] = 'WAIT'
    await start_screen(message)

def check_state(message: str) -> str:
    if message == start_buttons.values['keyboard'][0][0]['text'].lower():
        logger.info(f'start the game')
        return 'GAME'
    elif message == start_buttons.values['keyboard'][0][1]['text'].lower():
        logger.info(f'start the help')
        return 'HELP'
    logger.info(f'Error message, wait correct command')
    return 'WAIT'

def variants_prepare(variants: set) -> str|None:
    if len(variants) == 1:
        return text_message['correct_answer'].format(list(variants)[0])
    elif len(variants)>1:
        tmp = sorted(variants, key = lambda x: -all_words[x])[:150]
        return ', '.join(tmp)
    return None

def get_word():
    tmp = list(filter(lambda x: x[1]>0, all_words.items()))
    return choice(tmp)[0]


@dp.message_handler()
async def main_logic(message: types.Message):
    user_id = message.from_id
    text = message.text.lower().strip()
    user_name = message.from_user.full_name
    logger.info(f'{user_name} input text "{text}"')
    current_state = user_state.get(user_id, 'WAIT')
    if current_state == 'GAME':
        user_game.setdefault(user_id,UserGame(get_word()))
        logger.info(f'User {user_name}({user_id}) input word {text}')
        logger.info(f'Answer "{user_game[user_id].answer}", try {user_game[user_id].try_number}/6')
        if text in all_words.keys():
            result = user_game[user_id].is_correct(text)
            if result == 'ok':
                await bot.send_message(user_id, text_message['win'])
                await restart(message)
            elif not result:
                await bot.send_message(user_id, 
                        text_message['lose'].format(user_game[user_id].answer))
                await restart(message)
            else:
                create_image(user_id, text, result)
                photo = InputFile(f'images/{user_id}.png')
                await bot.send_photo(user_id, photo=photo)

        else:
            await bot.send_message(user_id, text_message['wrong_word'])
    elif current_state == 'HELP':
        user_help.setdefault(user_id, UserTry(all_words.keys()))
        result = user_help[user_id].next_step(text)
        if result == 'Ok':
            answer = variants_prepare(user_help[user_id].current_result.variants)
            if answer:
                await bot.send_message(user_id, answer)
            else:
                await bot.send_message(user_id, text_message['no_variants'])
                await restart(message)
        else:
            await bot.send_message(user_id, text_message[result])
        if user_help[user_id].need_restart():
            await restart(message)
    else:
        user_state[user_id] = check_state(text)
        if user_state[user_id] == 'WAIT':
            await start_screen(message)
        else:
            await bot.send_message(user_id, text_message['input_word'])


if __name__ == '__main__':
    executor.start_polling(dp,skip_updates = True)
    for i,wrd in user_help.items():
        print(f'{i}:\nWords: {wrd.words}\nAnswers: {wrd.answers}')
        print('*'*20)
