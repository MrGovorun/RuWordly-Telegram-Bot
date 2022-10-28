import logging
from random import choice

from aiogram import types, executor
from aiogram.types import InputFile

#import classes with structures for game and heling mod
from cls import UserTry, UserGame
#load_words load all words from csv file
from load_words import all_words
#bot_init make bot and buttons initialization
from bot_init import bot, dp, start_buttons
#text_message contains dict with all messages for easy replacment text
from text_message import text_message
#make_picture create folder with pics and generate new pics for game-mode
from make_picture import create_image

#logger initialization
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#users condition variables 
user_help = {}
user_game = {}
user_state = {}

@dp.message_handler(commands=['start'])
async def start_screen(message: types.Message):
    """Function for start command. Show two buttons - play and help"""
    logger.info(f'User {message.from_user.full_name} start bot')
    await bot.send_message(message.from_id,
            text_message['button_ask'],
            reply_markup = start_buttons)

@dp.message_handler(commands=['help'])
async def greeting(message: types.Message):
    """Function send message with information about bot"""
    logger.info(f'{message.from_user.full_name} get help')
    await bot.send_message(message.from_id,
            text_message['help'])

@dp.message_handler(commands=['rules'])
async def rules(message: types.Message):
    """Function send rules of wordly for game-mode"""
    logger.info(f'{message.from_user.full_name} get rules')
    await bot.send_message(message.from_id,
            text_message['rules'])

@dp.message_handler(commands=['restart'])
async def restart(message: types.Message):
    """Function change user current session to start position"""
    logger.info(f'User {message.from_user.full_name} restart the game')
    user_help[message.from_id] = UserTry(all_words)
    user_game[message.from_id] = UserGame(get_word())
    user_state[message.from_id] = 'WAIT'
    await start_screen(message)

def check_state(message: str) -> str:
    """Function compare input message with text ob buttons and return result in mode notation"""
    if message == start_buttons.values['keyboard'][0][0]['text'].lower():
        logger.info(f'start the game')
        return 'GAME'
    elif message == start_buttons.values['keyboard'][0][1]['text'].lower():
        logger.info(f'start the help')
        return 'HELP'
    logger.info(f'Error message, wait correct command')
    return 'WAIT'

def variants_prepare(variants: set) -> str|None:
    """Function get set of words, that may be answer in help-mode. It returns string with message about single answer, or text message with variants, sorted by word scores in vocabulary file"""
    if len(variants) == 1:
        return text_message['correct_answer'].format(list(variants)[0])
    elif len(variants)>1:
        tmp = sorted(variants, key = lambda x: -all_words[x])[:150]
        return ', '.join(tmp)
    return None

def get_word() -> str:
    """Function return random word from words list, that have non-zero scorein main vocabulary"""
    tmp = list(filter(lambda x: x[1]>0, all_words.items()))
    return choice(tmp)[0]


@dp.message_handler()
async def main_logic(message: types.Message):
    """Function with main logic. Parse all messages, check mode (game or help), check corectness inpput command and words with functions in classes"""
    #parse common variables for easy-read code
    user_id = message.from_id
    text = message.text.lower().strip()
    user_name = message.from_user.full_name
    logger.info(f'{user_name} input text "{text}"')
    #initial state for first message in session
    current_state = user_state.get(user_id, 'WAIT')
    #block of logic game-mode
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
    #block of logic help-mode
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
    #block of logic for buttons message or incorrect message
    else:
        user_state[user_id] = check_state(text)
        if user_state[user_id] == 'WAIT':
            await start_screen(message)
        else:
            await bot.send_message(user_id, text_message['input_word'])


if __name__ == '__main__':
    #start bot
    executor.start_polling(dp,skip_updates = True)
