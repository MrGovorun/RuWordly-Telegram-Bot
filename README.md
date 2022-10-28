# RuWordly-Telegram-Bot

## About bot
This is telegram-bot based in aiogram library with two mains functions:

1. Playing in Wordly
2. Helps with solving Wordly in others services

Bot contain dictionary with russian 5-length noun words, but it can be replaced with other launguage words. Dictionary also contain weight of all words, that used for sort output. In your language dictionary you can replace weight on 0.
Current russian list of words made by parsing site https://ru.wiktionary.org with beatifulsoap library and it's not include in that project. You may use your own way to get list of words. Weight is count of words in random free text, and it can be update. For this data I found text in free source, split text on words, get it normal form, found normal form in vocabulary and incriment weight. Weigth used for sort variants in help-mode - rare words in the end of list.

## Install
For install bot get token from Bot-Father, create file 'config' with code:
```python
token = <your token from Bot-Father>
```
Install all libraries from 'requirements.txt' with command:
```
pip install -r requirements.txt
```
Run bot with command:
```
python3 main.py
```

## Localization
If you need localization, you should change 'words.csv' on your vocabulary with the same format ('word,weight'). If you don't have weight, place 1 in vocabularu, but your variants being without sort of rarest. You also need replace text messages in file 'text_message.py'. It containts dict with all messages and buttons names. Change messages based on english key in dict.

## How to use
When you start bot, it ask you mode that you like. There is two mods - wordly game and help with wordly game.

### Wrodly game mode
Bot get one word from vocabulary with non-zero weight (if you don't have weight in your vocabulary, you possible play in hard-mode Wordly with ultra-rare words)
Player input 5-letter noun word. Bot generate code of accordance for than word and generate image with result, that send to user. User have 6 tries. If player don't guess answer, bot send lose message, end game and go to start screen with buttons

### Help with wordly game
Bot wait messages of two types. First message should be 5-letter non words, that user input in wordly game in other system (site or app). Other system show user answer - colored word. User should code that image and send code to bot - it was second message.
Code is easy.  
Grey letters mark as 0,  
white letters as 1,  
yellow letters as 2  

For example:  
![example](https://github.com/MrGovorun/RuWordly-Telegram-Bot/blob/main/example.png "example")   

If all correct, bot send variants sorted with weight. User can choose word from variants or imagine it yourself. Then user put this word in other system and put again word in system answer in bot. Repeat until count of variants should be less than 2.
