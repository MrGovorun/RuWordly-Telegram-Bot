# RuWordly-Telegram-Bot

## About the bot.
This is telegram-bot based in aiogram library with two mains functions:

1. Play in Wordly
2. Help to solve Wordly in other services

This bot contains Dictionary with 5-length russian language nouns, but it can be replaced with other launguage. The Dictionary also contains the weight of all words, that used for sort output. You can replace the weight to 1 in your language dictionary.
The current list of russian words was made by parsing site https://ru.wiktionary.org with script based on Beatifulsoap library and it's not included in this project. You may use your own way to get list of words.The weight - is a count of words in a free random text, and it can be updated by you. For this dictionary I found texts in a free source, then split them on words, got the normal form, and found normal form in dictionary and after that incrimented word's weight. The weigth used to sort words variants in a help-mode. Rare words are placed at the end of the list.

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
If you need to change localization, so you should change 'words.csv' on your vocabulary with the same format ('word,weight'). If you don't have weight, place 1 in vocabulary, but your variants won't be sorted by rarity. You also need replace text messages in file 'text_message.py'. It containts dict with all messages and button names. Change messages based on English key in dict.

## How to use
There are two modes - Wordly game and Help with wordly game. Please choose one of them.

### Wordly game mode
The Bot gets one word from vocabulary with non-zero weight (if you don't have weight in your vocabulary, probably you are playing in a hard-mode Wordly with ultra-rare words).
Player inputs 5-letter noun. The Bot generates code of accordance for that word and generates result image and then send it to player. Player has 6 tries. If player doesn't guess the answer, the bot sends him lose message, ends game and goes to the Start screen with buttons.

### Help with wordly game
The Bot waits for messages of two types. First message should contain 5-letter noun which player inputed in wordly game in other system (site or app). Other system shows user answer - colored word. Player should code that image and send code to the bot - it is a second message.
Code is easy.  
Grey letters mark as 0,  
white letters as 1,  
yellow letters as 2  

For example:  
![example](https://github.com/MrGovorun/RuWordly-Telegram-Bot/blob/main/example.png "example")   

If everything is correct, the bot will send you the variants sorted by weight. Player can choose word from variants or invent it by himself. Repeat it until number of variants would be less than 2.
