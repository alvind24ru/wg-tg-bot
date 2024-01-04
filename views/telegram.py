from main import bot

WELCOME_MESSAGE = 'Hello, world!'


class TelegramView:
    def __init__(self, tgbot):
        self._tgbot = tgbot

    def send_welcome(self, chat_id):
        self._tgbot.send_message(chat_id, WELCOME_MESSAGE)

    def send_message(self, chat_id, text) -> None:
        self._tgbot.send_message(chat_id, text)

    def send_config_text(self, chat_id, text) -> None:
        self._tgbot.send_message(chat_id, text)

    def send_statistics(self, chat_id, statistics) -> None:
        self._tgbot.send_message(chat_id, statistics)


telegram = TelegramView(bot)
