from main import bot
from views.telegram import telegram
from model.bot import models_tg_bot
import re

@bot.message_handler(content_types=['text'], commands=['start'])
def send_welcome(message):
    telegram.send_welcome(message.chat.id)


@bot.message_handler(commands=['Список клиентов'])
def get_a_list_of_clients(message):
    models_tg_bot.user_is_admin_or_exception(message.from_user.id)
    list_of_clients = models_tg_bot.get_all_clients()
    for client in list_of_clients:
        telegram.send_message(message.chat.id, client)


@bot.message_handler(regexp=r'^Статистика$')
def get_statistics(message):
    telegram.send_statistics(message.chat.id, models_tg_bot.get_statistics(message.from_user.id))


@bot.message_handler(commands=['Получить все конфиги'])
def get_all_configs(message):
    models_tg_bot.user_is_admin_or_exception(message.from_user.id)
    configs = models_tg_bot.get_all_configs()
    for config in configs:
        telegram.send_config_text(message.chat.id, config)


@bot.message_handler(content_types=['text'], regexp=r'^Получить конфиг$')
def create_new_client(message):
    if not models_tg_bot.user_is_created(message.from_user.id):
        models_tg_bot.create_config(message.from_user.id, message.from_user.full_name, message.from_user.username,
                                    message.chat.id)
    config = models_tg_bot.get_config(message.from_user.id)
    telegram.send_config_text(message.chat.id, config)


@bot.message_handler(commands=['del'])
def delete_user(message):
    last_octet = message.text.split(' ')[1]
    userid = models_tg_bot.get_userid_by_ip(f'10.0.0.{last_octet}')
    if models_tg_bot.user_is_created(userid):
        models_tg_bot.delete_client(last_octet)
        telegram.send_message(message.chat.id, 'Клиент удален')
    else:
        telegram.send_message(message.chat.id, 'Клиент с данным ip не найден')

@bot.message_handler(commands=['run'])
def start_wg(message):
    # models_tg_bot.user_is_admin_or_exception(message.from_user.id)
    models_tg_bot.start_wg_server()


@bot.message_handler(commands=['Статистика'])
def get_statistic(message):
    telegram.send_statistic(message.chat.id, models_tg_bot.get_statistics(message.from_user.id))


@bot.message_handler(content_types=['text'], regexp=r'^Статистика всех клиентов$')
def get_all_statistics(message):
    models_tg_bot.user_is_admin_or_exception(message.from_user.id)
    statistics = models_tg_bot.get_all_statistics()
    for statistic in statistics:
        telegram.send_statistics(message.chat.id, statistic)


@bot.message_handler(content_types=['text'], regexp=r'^Назначить админом$')
def set_admin(message):
    if message.reply_to_message:
        models_tg_bot.user_is_admin_or_exception(message.from_user.id)
        models_tg_bot.set_admin(message.reply_to_message.from_user.id)
        telegram.send_message(message.chat.id, 'Админ успешно назначен')
    else:
        telegram.send_message(message.chat.id, 'Сообщение не является ответом или пересланным')

@bot.message_handler(commands=['backup'])
def backup(message):
    models_tg_bot.user_is_admin_or_exception(message.from_user.id)
    backup_file = models_tg_bot.get_backup_file()
    telegram.send_file(message.chat.id, backup_file)



@bot.message_handler(content_types=['text'])
def echo_message(message):
    telegram.send_message(message.chat.id, f'Не понимаю, chat_id = {message.chat.id}')

try:
    bot.infinity_polling()
except Exception as e:
    print(e)
    telegram.send_message(472162143, str(e))