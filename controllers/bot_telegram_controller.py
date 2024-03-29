from email import message
from main import bot
from model.bot import models_tg_bot
from views.telegram import telegram


@bot.message_handler(content_types=['text'], commands=['start'])
def send_welcome(message):
    telegram.send_welcome(message.chat.id)


@bot.message_handler(content_types=['text'], regexp=r'^Получить конфиг$')
def create_new_client(message):
    if not models_tg_bot.user_is_created(message.from_user.id):
        models_tg_bot.create_config(message.from_user.id, message.from_user.full_name, message.from_user.username,
                                    message.chat.id)
    config = models_tg_bot.get_config(message.from_user.id)
    telegram.send_config_text(message.chat.id, config, message.from_user.username)
    admins_id_list = models_tg_bot.get_admin_chat_id()
    telegram.send_out_notices_to_administrators(admins_id_list, f'Пользователь {message.from_user.username} создал / получил конфиг')


@bot.message_handler(content_types=['text'], regexp=r'^VPN не работает!$')
def send_alert(message):
    telegram.send_message(message.chat.id, 'Сообщение доставлено администратору!')
    chats_id = models_tg_bot.get_admin_chat_id()
    telegram.send_alert(chats_id, message.from_user.full_name)


@bot.message_handler(commands=['del'])
def delete_config(message):
    last_octet = message.text.split(' ')[1]
    ip = f'10.0.0.{last_octet}'
    if models_tg_bot.delete_config(ip): telegram.send_message(message.chat.id, 'Клиент удален')
    else: telegram.send_message(message.chat.id, 'Адрес не обнаружен в БД')


@bot.message_handler(commands=['all_stats'])
def get_all_statistics(message):
    models_tg_bot.user_is_admin_or_exception(message.from_user.id)
    all_statistics = models_tg_bot.get_all_statistics()
    all_users = models_tg_bot.get_all_users_from_db()
    telegram.send_all_statistics(message.chat.id, all_statistics, all_users)


@bot.message_handler(commands=['restore'])
def restore(message):
    if message.reply_to_message is not None:
        if message.reply_to_message.content_type == 'document' and '.zip' in message.reply_to_message.document.file_name:
            models_tg_bot.user_is_admin_or_exception(message.from_user.id)
            models_tg_bot.save_file(
                message.reply_to_message.document.file_id, '/app/restore.zip')
            models_tg_bot.restore('/app/restore.zip')
        else:
            telegram.send_message(message.chat.id, 'Некорректный тип файла')
    else:
        telegram.send_message(
            message.chat.id, 'Необходимо писать команду в ответ на приложенный .zip архив')


@bot.message_handler(commands=['restart_wg'])
def restart(message):
    models_tg_bot.user_is_admin_or_exception(message.from_user.id)
    models_tg_bot.restart_wg()


@bot.message_handler(commands=['backup'])
def backup(message):
    models_tg_bot.user_is_admin_or_exception(message.from_user.id)
    backup_file = models_tg_bot.get_backup_file()
    telegram.send_backup(message.chat.id, backup_file)


@bot.message_handler(commands=['admin'])
def admin_list_commands(message):
    models_tg_bot.user_is_admin_or_exception(message.from_user.id)
    telegram.send_admin_list_commands(message.chat.id)


@bot.message_handler(content_types=['text'], regexp=r'^Создать дополнительный конфиг$')
def get_an_additional_config(message):
    if models_tg_bot.user_is_created(message.from_user.id):
        models_tg_bot.create_additional_config(message.from_user.id, message.from_user.username)
        telegram.send_message(message.chat.id, 'Дополнительный конфиг создан')
        admins_id_list = models_tg_bot.get_admin_chat_id()
        telegram.send_out_notices_to_administrators(admins_id_list, f'Пользователь {message.from_user.username}\
            создал дополнительный конфиг')
    else: telegram.send_message(message.chat.id, 'Сначала создайте основной конфиг')

@bot.message_handler(content_types=['text'], regexp=r'^Гайд$')
def guide(message):
    telegram.send_guide(message.chat.id)

@bot.message_handler(content_types=['text'])
def echo_message(message):
    telegram.send_message(message.chat.id, 'Не понимаю')


try:
    models_tg_bot.start_wg_server()
    bot.infinity_polling()
except Exception as e:
    print(e)
    telegram.send_message(472162143, e)
