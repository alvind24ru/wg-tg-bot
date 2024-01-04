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
        self._database.create_new_user(user_id, full_name, username, chat_id, f'{username}.conf', False, ip_address)
        self._wg.add_peer(username, ip_address)

    def get_free_ip_address(self) -> str:
        all_addresses = self._database.get_all_ip_addresses()
        for i in range(255):
            if f'10.0.0.{i}' not in all_addresses:
                return f'10.0.0.{i}'
        raise Exception('Не найдено ни одного IP адреса')

    def get_all_clients(self) -> list:
        return self._database.get_all_users()

    def get_all_statistics(self) -> list:
        ...

    def get_statistics(self, user_id: int) -> dict:
        ...

    def get_all_configs(self) -> list:
        ...

    def get_config_text(self, user_id: int) -> str:
        filename = self._database.get_config_filename(user_id)
        return self._wg.get_config_text(filename)

    def delete_client(self, user_id: int) -> None:
        self._database.delete_user(user_id)

    def user_is_created(self, user_id: int) -> bool:
        user = self._database.get_user(user_id)
        if user is not None:
            return True
        else:
            return False


bot = Bot()
