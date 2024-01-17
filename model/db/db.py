from email.headerregistry import Address
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.db.database_setup import User, Base, Ip_addresses


class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        engine = create_engine(db_url)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self._session = DBSession()

    def reload_session(self):
        engine = create_engine(self.db_url)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self._session = DBSession()

    def create_new_peer(self, user_id: int, full_name: str, username: str, chat_id: int,
                        is_admin: bool = False, ip_address: str = '') -> None:
        new_user = User(id=user_id, full_name=full_name, username=username, chat_id=chat_id, is_admin=is_admin)
        ip = Ip_addresses(address=ip_address, user_id=user_id)
        self._session.add(new_user)
        self._session.add(ip)
        self._session.commit()
        self._session.close()

    def get_all_ip_addresses(self) -> list:
        """Возвращает все уже назначенные ip адреса"""
        all_ip_addresses = self._session.query(Ip_addresses.address).all()
        return [i[0] for i in all_ip_addresses]

    def get_all_users(self) -> list:
        all_users = self._session.query(User).all()
        return all_users

    def get_username_by_user_id(self, user_id: int) -> str:
        user = self._session.query(User).filter_by(id=user_id).first()
        return user.username

    def get_username_by_ip(self, ip: str) -> str:
        """Args:ip (str): example: 10.0.0.1"""
        address = self._session.query(Ip_addresses).filter_by(address=ip).first()
        user = self._session.query(User).filter_by(ip_address=address.user_id).first()
        return user.username

    def delete_user_by_user_id(self, user_id: int) -> None:
        user = self._session.query(User).filter_by(id=user_id).first()
        self._session.delete(user)
        self._session.commit()
        self._session.close()

    def delete_user_by_ip_address(self, ip: str) -> None:
        """Args:ip (str): example: 10.0.0.1"""
        address = self._session.query(Ip_addresses).filter_by(address=ip).first()
        user = self._session.query(User).filter_by(ip_address=address.user_id).first()
        self._session.delete(user)
        self._session.commit()
        self._session.close()

    def get_user_by_ip_address(self, ip: str) -> User:
        """Args:ip (str): example: 10.0.0.1"""
        address = self._session.query(Ip_addresses).filter_by(address=ip).first()
        user = self._session.query(User).filter_by(ip_address=address.user_id).first()
        return user

    def get_user_by_user_id(self, user_id: int) -> User:
        user = self._session.query(User).filter_by(id=user_id).first()
        return user

    def user_is_admin(self, user_id: int) -> bool:
        user = self._session.query(User).filter_by(id=user_id).first()
        return user.is_admin

    def get_ips_by_user_id(self, user_id) -> list:
        addresses = self._session.query(Ip_addresses).filter_by(user_id=user_id).all()
        result = [i.address for i in addresses]
        return result

    def get_admin_chat_id(self) -> list:
        users = self._session.query(User).filter_by(is_admin=True).all()
        result = [i.chat_id for i in users]
        return result

    def create_additional_config(self, user_id, ip_address) -> None:
        ip = Ip_addresses(user_id = user_id, address = ip_address)
        self._session.add(ip)
        self._session.commit()
        self._session.close()

    def delete_ip_address(self, ip_address):
        address = self._session.query(Ip_addresses).filter_by(address=ip_address).first()
        self._session.delete(address)
        self._session.commit()
        self._session.close()


db = Database('sqlite:///wireguard.db')
