import telebot
from config import API_TOKEN
from model.db import database_setup

bot = telebot.TeleBot(API_TOKEN)





class Test:
    @bot.message_handler(content_types=['text'], commands=['help'])
    def help(message):
        bot.send_message(message.chat.id, "sfsfsf")


    @bot.message_handler(content_types=['text'])
    def echo_message(message):
        bot.reply_to(message, message.text)
        print(message.chat.id)
        print(message.from_user.id)


bot.infinity_polling()