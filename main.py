import telebot
import os
import sys
from model.db import database_setup
import controllers.bot_telegram_controller
API = os.environ.get('API_TOKEN', "None")
if API is None:
    print("В переменных окружения не обнаружен токен бота")
    sys.exit(1)
bot = telebot.TeleBot(API)


print('Starting...')


# class Test:
#     @bot.message_handler(content_types=['text'], commands=['help'])
#     def help(message):
#         bot.send_message(message.chat.id, "sfsfsf")
#
#
#     @bot.message_handler(content_types=['text'])
#     def echo_message(message):
#         bot.reply_to(message, message.text)
#         print(message.chat.id)
#         print(message.from_user.id)


