from email.headerregistry import Address
from ipaddress import ip_address, ip_interface
import stat
import string
import time
from views.message import *
from main import bot
from views.boards import main_board, admin_board
from guide.guide_text import GUIDE

welcome_message = """Здесь ты можешь получить один или несколько Wireguard конфиг-файлов."""


class TelegramView:
	def __init__(self, tgbot):
		self._tgbot = tgbot

	def send_welcome(self, chat_id):
		self._tgbot.send_message(chat_id, welcome_message, reply_markup=main_board)

	def send_message(self, chat_id, text) -> None:
		self._tgbot.send_message(chat_id, text, reply_markup=main_board)

	def send_config_text(self, chat_id, text:list[list], username) -> None:
		i = 1
		for config in text:
			self._tgbot.send_message(chat_id, f"```Copy\n{config[0]}```", reply_markup=main_board, parse_mode="MARKDOWN")
			self._tgbot.send_document(chat_id, config[1], reply_markup=main_board, visible_file_name=f'{username[:28]}_{i}.conf')
			self._tgbot.send_photo(chat_id, config[2], reply_markup=main_board)
			i+=1
	def send_file(self, chat_id, file) -> None:
		self._tgbot.send_document(chat_id, file, reply_markup=main_board)

	def send_backup(self, chat_id, file) -> None:
		self._tgbot.send_document(chat_id, file, reply_markup=admin_board,
							visible_file_name=f'Backup {time.ctime()}.zip')

	def send_statistics(self, chat_id: int, statistics: list) -> None:
		if len(statistics) > 0:
			for i in statistics:
				index = i[0].find('/32')
				if len(i) > 2:
					self._tgbot.send_message(chat_id, f'Статистика для адреса: {i[0][15:index]}\n'
													f'Последнее подключение: {i[1][20:]}\n'
													f'Трафик: {i[2][12:]}', reply_markup=main_board)
				else: self._tgbot.send_message(chat_id, f'Статистика для адреса {i[0][15:index]} не собрана!', reply_markup=main_board)
		else: self._tgbot.send_message(chat_id, 'Статистика не собрана!', reply_markup=main_board)

	def send_admin_list_commands(self, chat_id):
		self._tgbot.send_message(chat_id, admin_message, reply_markup=admin_board)

	def send_all_statistics(self, chat_id, all_statistics, all_users):
		for user in all_users:
			ip = [i.address for i in user.ip_address]
			self._tgbot.send_message(chat_id, f'full name: {user.full_name}\n'
			                                  f'username: {user.username}\n'
			                                  f'ip: {ip}\n'
			                                  f'is admin: {user.is_admin}')
		self._tgbot.send_message(chat_id, all_statistics)

	def send_alert(self, chats_id, from_user):
		for chat_id in chats_id:
			self._tgbot.send_message(chat_id, f'Сообщение о неработающем VPN от {from_user}')

	def send_out_notices_to_administrators(self, admins_id_list: list[int], text: str):
		for i in admins_id_list:
			self.send_message(i, text)

	def send_guide(self, chat_id):
		self._tgbot.send_message(chat_id, GUIDE, parse_mode="MARKDOWN")


telegram = TelegramView(bot)
