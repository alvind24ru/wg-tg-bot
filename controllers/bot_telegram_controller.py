from main import bot
from views.telegram import telegram
from model.bot import models_tg_bot
import re

@bot.message_handler(content_types=['text'], commands=['start'])
def send_welcome(message):
    telegram.send_welcome(message.chat.id)


@bot.message_handler(regexp=r'^Статистика$')
def get_statistics(message):
    stat = models_tg_bot.get_statistics(message.from_user.id)
    telegram.send_statistics(message.chat.id, stat)


@bot.message_handler(content_types=['text'], regexp=r'^Получить конфиг$')
def create_new_client(message):
    if not models_tg_bot.user_is_created(message.from_user.id):
        models_tg_bot.create_config(message.from_user.id, message.from_user.full_name, message.from_user.username,
                                    message.chat.id)
    config = models_tg_bot.get_config(message.from_user.id)
    telegram.send_config_text(message.chat.id, config, message.from_user.username)


@bot.message_handler(commands=['del'])
def delete_user(message):
    last_octet = message.text.split(' ')[1]
    userid = models_tg_bot.get_userid_by_ip(f'10.0.0.{last_octet}')
    if models_tg_bot.user_is_created(userid):
        models_tg_bot.delete_client(last_octet)
        telegram.send_message(message.chat.id, 'Клиент удален')
    else:
        telegram.send_message(message.chat.id, 'Клиент с данным ip не найден')

@bot.message_handler(commands=['all-stats'])
def get_all_statistics(message):
    models_tg_bot.user_is_admin_or_exception(message.from_user.id)
    statistics = models_tg_bot.get_all_statistics()
    for statistic in statistics:
        telegram.send_statistics(message.chat.id, statistic)


@bot.message_handler(commands=['set-admin'])
def set_admin(message):
    if message.reply_to_message:
        models_tg_bot.user_is_admin_or_exception(message.from_user.id)
        models_tg_bot.set_admin(message.reply_to_message.from_user.id)
        telegram.send_message(message.chat.id, 'Админ успешно назначен')
    else:
        telegram.send_message(message.chat.id, 'Сообщение не является ответом или пересланным')

@bot.message_handler(commands=['restore'])
def restore(message):
    pass

@bot.message_handler(commands=['status'])
def server_status(message):
    pass

@bot.message_handler(commands=['backup'])
def backup(message):
    models_tg_bot.user_is_admin_or_exception(message.from_user.id)
    backup_file = models_tg_bot.get_backup_file()
    telegram.send_file(message.chat.id, backup_file)

@bot.message_handler(commands=['admin'])
def admin_list_commands(message):
    models_tg_bot.user_is_admin_or_exception(message.from_user.id)
    telegram.send_admin_list_commands(message.chat.id)

@bot.message_handler(content_types=['text'])
def echo_message(message):
    telegram.send_message(message.chat.id, f'Не понимаю, chat_id = {message.chat.id}')

try:
    models_tg_bot.start_wg_server()
    bot.infinity_polling()
except Exception as e:
    print(e)
    telegram.send_message(472162143, e)