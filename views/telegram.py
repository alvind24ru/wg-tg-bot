import time

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

	def send_config_text(self, chat_id, text, username) -> None:
		self._tgbot.send_message(chat_id, text[0], reply_markup=main_board)
		self._tgbot.send_document(chat_id, text[1], reply_markup=main_board, visible_file_name=f'{username}.conf')
		self._tgbot.send_photo(chat_id, text[2], reply_markup=main_board)

	def send_file(self, chat_id, file) -> None:
		self._tgbot.send_document(chat_id, file, reply_markup=main_board)

	def send_backup(self, chat_id, file) -> None:
		self._tgbot.send_document(chat_id, file, reply_markup=main_board,
		                          visible_file_name=f'Backup {time.ctime()}.zip')

	def send_statistics(self, chat_id, statistics) -> None:
		if len(statistics) > 2:
			self._tgbot.send_message(chat_id, f'Ваш VPN адрес: {statistics[0][15:]}\n'
			                                  f'Последнее подключение: {statistics[1][20:]}\n'
			                                  f'Трафик: {statistics[2][12:]}', reply_markup=main_board)
		else:
			self._tgbot.send_message(chat_id, 'Статистика не собрана!', reply_markup=main_board)

	def send_admin_list_commands(self, chat_id):
		self._tgbot.send_message(chat_id, '/admin Выводит все команды администратора\n'
		                                  '/backup получение архива с конфигом, который потом можно будет восстановить\n'
		                                  '/restore восстановление конфига из .zip архива. Необходимо писать в ответ к загруженному конфигу\n'
		                                  '/set_admin (октет) делает администратором пользователя, чей последний октет адреса указан\n'
		                                  '/all_stats получение списка всех пользователей и их статистики\n'
		                                  '/del (октет) удаляет пользователя, чей последний октет адреса указан\n'
		                                  '/restart_wg перезапуск VPN службы\n')

	def send_all_statistics(self, chat_id, all_statistics, all_users):
		for user in all_users:
			self._tgbot.send_message(chat_id, f'full name: {user.full_name}\n'
			                                  f'username: {user.username}\n'
			                                  f'ip: {user.ip_address}\n'
			                                  f'is admin: {user.is_admin}')
		self._tgbot.send_message(chat_id, all_statistics)

	def send_alert(self, chats_id, from_user):
		for chat_id in chats_id:
			self._tgbot.send_message(chat_id, f'Сообщение о неработающем VPN от {from_user}')


telegram = TelegramView(bot)
