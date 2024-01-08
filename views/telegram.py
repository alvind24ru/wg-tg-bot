from main import bot
from views.boards import main_board
WELCOME_MESSAGE = 'Привет, я бот, можешь получить wireguard конфиг.'


class TelegramView:
    def __init__(self, tgbot):
        self._tgbot = tgbot

    def send_welcome(self, chat_id):
        self._tgbot.send_message(chat_id, WELCOME_MESSAGE, reply_markup=main_board)

    def send_message(self, chat_id, text) -> None:
        self._tgbot.send_message(chat_id, text, reply_markup=main_board)

    def send_config_text(self, chat_id, text) -> None:
        self._tgbot.send_message(chat_id, text[0], reply_markup=main_board)
        self._tgbot.send_document(chat_id, text[1], reply_markup=main_board, caption='Ваш конфиг файл в документе:')
        self._tgbot.send_photo(chat_id, text[2], reply_markup=main_board)

    def send_file(self, chat_id, file) -> None:
        self._tgbot.send_document(chat_id, file, reply_markup=main_board)

    def send_statistics(self, chat_id, statistics) -> None:
        self._tgbot.send_message(chat_id, f'Ваша статистика: {statistics}', reply_markup=main_board)


telegram = TelegramView(bot)
