from ast import boolop
from urllib import request

from custom_exceptions import AdminException
from main import bot as telebot
from model.db.db import db
from model.wg import WireGuard


class Bot:
    def __init__(self):
        self._database = db
        self._AdminException = AdminException
        self._wg = WireGuard
        self._bot = telebot

    def user_is_admin_or_exception(self, user_id) -> None:
        if not self._database.user_is_admin(user_id):
            raise self._AdminException

    def create_config(self, user_id: int, full_name: str, username: str, chat_id: int) -> None:
        """Создает нового пользователя, первый созданный пользователь по умолчанию явдяется админом"""
        ip_address = self.get_free_ip_address()
        __is_admin = False
        if len(self._database.get_all_ip_addresses()) == 0:
            __is_admin = True
        self._database.create_new_peer(user_id, full_name, username, chat_id, __is_admin, ip_address)
        self._wg.add_peer(ip_address)

    def get_free_ip_address(self) -> str:
        all_addresses = self._database.get_all_ip_addresses()
        if len(all_addresses) == 0:
            return '10.0.0.2'
        for i in range(2, 255):
            if f'10.0.0.{i}' not in all_addresses:
                return f'10.0.0.{i}'
        raise Exception('Не найдено ни одного свободного IP-адреса')

    def get_all_users(self) -> list:
        return self._database.get_all_users()

    def get_all_statistics(self) -> str:
        return self._wg.get_all_statistics()

    def get_statistics(self, user_id: int) -> list[list]:
        ip = self._database.get_ips_by_user_id(user_id)
        result = [self._wg.get_statistics(i) for i in ip]
        return result

    def get_config(self, user_id: int) -> list[list]:
        result = []
        ips = self._database.get_ips_by_user_id(user_id)
        for i in ips:
            p = []
            p.append(self._wg.get_config_text(i))
            p.append(self._wg.get_config_file(i))
            p.append(self._wg.get_config_qrcode(i))
            result.append(p)
        return result

    def get_config_file(self, user_id: int): ...

    def get_config_qrcode(self, user_id: int): ...

    def delete_config(self, ip: str) -> bool:
        all_addresses = self._database.get_all_ip_addresses()
        if ip in all_addresses:
            self._database.delete_ip_address(ip)
            self._wg.delete_peer(ip)
            return True
        else: return False

    def get_userid_by_ip(self, ip_address: str):
        user = self._database.get_user_by_ip_address(ip_address)
        if user is not None:
            return user.id
        else:
            raise Exception('Пользователь с указанным id не найден')

    def user_is_created(self, user_id: int) -> bool:
        user = self._database.get_user_by_user_id(user_id)
        if user is not None:
            return True
        else:
            return False

    def start_wg_server(self) -> None:
        self._wg.start_wg_server()

    def get_backup_file(self) -> bytes:
        self._wg.create_backup()
        with open('/etc/wireguard/backup.zip', 'rb') as f:
            return f.read()

    def get_all_users_from_db(self):
        return self._database.get_all_users()

    def restart_wg(self):
        self._wg.restart()

    def get_admin_chat_id(self) -> list:
        return self._database.get_admin_chat_id()

    def save_file(self, file_id, path):
        fid = self._bot.get_file(file_id).file_id
        url = self._bot.get_file_url(fid)
        request.urlretrieve(url, path)

    def restore(self, file_path):
        self._wg.restore_config(file_path)

    def create_additional_config(self, user_id, username) -> None:
        ip_address = self.get_free_ip_address()
        self._database.create_additional_config(user_id=user_id, ip_address=ip_address)
        name = f'{username}' + f'{ip_address[7:]}'
        self._wg.add_peer(ip = ip_address)

models_tg_bot = Bot()
