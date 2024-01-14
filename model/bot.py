from model.db.db import db
from custom_exceptions import AdminException
from model.wg import wg, WireGuard


class Bot:
    def __init__(self):
        self._database = db
        self._AdminException = AdminException
        self._wg = WireGuard

    def user_is_admin_or_exception(self, user_id) -> None:
        if not self._database.user_is_admin(user_id):
            raise self._AdminException

    def create_config(self, user_id: int, full_name: str, username: str, chat_id: int) -> None:
        ip_address = self.get_free_ip_address()
        _is_admin = False
        #Первый пользователь админ
        if len(self._database.get_all_ip_addresses()) == 0:
            _is_admin = True
        self._database.create_new_user(user_id, full_name, username, chat_id, _is_admin, ip_address)
        self._wg.add_peer(username, ip_address)

    def get_free_ip_address(self) -> str:
        all_addresses = self._database.get_all_ip_addresses()
        if len(all_addresses) == 0: return '10.0.0.2'
        for i in range(2, 255):
            if f'10.0.0.{i}' not in all_addresses[0]:
                return f'10.0.0.{i}'
        raise Exception('Не найдено ни одного IP адреса')

    def get_all_clients(self) -> list:
        return self._database.get_all_users()

    def get_all_statistics(self) -> list:
        return self._wg.get_all_statistics()

    def get_statistics(self, user_id: int) -> str:
        ip = self._database.get_ip_by_user_id(user_id)
        stat = self._wg.get_statistics(ip)
        return stat

    def get_all_configs(self) -> list:
        ...

    def get_config(self, user_id: int) -> list:
        result = []
        filename = self._database.get_username_by_userid(user_id)
        result.append(self._wg.get_config_text(filename))
        result.append(self._wg.get_config_file(filename))
        result.append(self._wg.get_config_qrcode(filename))
        return result

    def get_config_file(self, user_id: int): ...

    def get_config_qrcode(self, user_id: int): ...

    def delete_client(self, last_octet: int) -> None:
        username = self._database.get_username_from_ip(f'10.0.0.{last_octet}')
        self._database.delete_user_by_ip_address(f'10.0.0.{last_octet}')
        self._wg.delete_peer(f'10.0.0.{last_octet}', username)

    def get_userid_by_ip(self, ip_address: str):
        user = self._database.get_user_by_ip_address(ip_address)
        if user is not None:
            return user.id
        else:
            return None

    def user_is_created(self, user_id: int) -> bool:
        user = self._database.get_user(user_id)
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
models_tg_bot = Bot()
