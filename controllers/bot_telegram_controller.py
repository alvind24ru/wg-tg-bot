from main import bot
from views.telegram import telegram
from model.bot import bot


@bot.message_handler(commands=['start'])
def send_welcome(message):
    telegram.send_welcome(message.chat.id)


@bot.message_handler(commands=['Список клиентов'])
def get_a_list_of_clients(message):
    bot.user_is_admin_or_exception(message.from_user.id)
    list_of_clients = bot.get_all_clients()
    for client in list_of_clients:
        telegram.send_message(message.chat.id, client)


@bot.message_handler(commands=['Статистика'])
def get_statistics(message):
    telegram.send_message(message.chat.id, bot.get_statistics(message.from_user.id))


@bot.message_handler(commands=['Статистика всех клиентов'])
def get_all_statistics(message):
    bot.user_is_admin_or_exception(message.from_user.id)
    statistics = bot.get_all_statistics()
    for statistic in statistics:
        telegram.send_message(message.chat.id, statistic)


@bot.message_handler(commands=['Получить все конфиги'])
def get_all_configs(message):
    bot.user_is_admin_or_exception(message.from_user.id)
    configs = bot.get_all_configs()
    for config in configs:
        telegram.send_config_text(message.chat.id, config)


@bot.message_handler(commands=['Получить конфиг'])
def create_new_client(message):
    if not bot.user_is_created(message.from_user.id):
        bot.create_config(message.from_user.id, message.from_user.full_name, message.from_user.username,
                          message.chat.id)
    config = bot.get_config_text(message.from_user.id)
    telegram.send_config_text(message.chat.id, config)


@bot.message_handler(commands=['Удалить клиента'])
def delete_client(message):
    if message.reply_to_message:
        bot.user_is_admin_or_exception(message.from_user.id)
        bot.delete_client(message.forward_from.id)
        telegram.send_message(message.chat.id, 'Клиент удален')


@bot.message_handler(commands=['Статистика'])
def get_statistic(message):
    telegram.send_statistic(message.chat.id, bot.get_statistics(message.from_user.id))


@bot.message_handler(commands=['Статистика всех клиентов'])
def get_all_statistics(message):
    bot.user_is_admin_or_exception(message.from_user.id)
    statistics = bot.get_all_statistics()
    for statistic in statistics:
        telegram.send_statistics(message.chat.id, statistic)


@bot.message_handler(commands=['Назначить админом'])
def set_admin(message):
    if message.reply_to_message:
        bot.user_is_admin_or_exception(message.from_user.id)
        bot.set_admin(message.reply_to_message.from_user.id)
        telegram.send_message(message.chat.id, 'Админ успешно назначен')
    else:
        telegram.send_message(message.chat.id, 'Сообщение не является ответом или пересланным')
