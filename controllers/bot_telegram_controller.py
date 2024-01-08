from main import bot
from views.telegram import telegram
from model.bot import models_tg_bot


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


@bot.message_handler(commands=['Статистика всех клиентов'])
def get_all_statistics(message):
    models_tg_bot.user_is_admin_or_exception(message.from_user.id)
    statistics = models_tg_bot.get_all_statistics()
    for statistic in statistics:
        telegram.send_message(message.chat.id, statistic)


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


@bot.message_handler(commands=['Удалить клиента'])
def delete_client(message):
    if message.reply_to_message:
        models_tg_bot.user_is_admin_or_exception(message.from_user.id)
        models_tg_bot.delete_client(message.forward_from.id)
        telegram.send_message(message.chat.id, 'Клиент удален')


@bot.message_handler(commands=['Статистика'])
def get_statistic(message):
    telegram.send_statistic(message.chat.id, models_tg_bot.get_statistics(message.from_user.id))


@bot.message_handler(commands=['Статистика всех клиентов'])
def get_all_statistics(message):
    models_tg_bot.user_is_admin_or_exception(message.from_user.id)
    statistics = models_tg_bot.get_all_statistics()
    for statistic in statistics:
        telegram.send_statistics(message.chat.id, statistic)


@bot.message_handler(commands=['Назначить админом'])
def set_admin(message):
    if message.reply_to_message:
        models_tg_bot.user_is_admin_or_exception(message.from_user.id)
        models_tg_bot.set_admin(message.reply_to_message.from_user.id)
        telegram.send_message(message.chat.id, 'Админ успешно назначен')
    else:
        telegram.send_message(message.chat.id, 'Сообщение не является ответом или пересланным')


@bot.message_handler(content_types=['text'])
def echo_message(message):
    telegram.send_message(message.chat.id, 'Не понимаю')


bot.infinity_polling()