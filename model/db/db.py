from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.db.database_setup import User, Base

# Сообщаем с какой БД хотим взаимодействовать
engine = create_engine('sqlite:///wireguard.db')

# Что бы создать соединение между определениями класса и таблицами в базе данных,
# используем команду Base.metadata.bind.
Base.metadata.bind = engine

# Экземпляр DBSession() отвечает за все обращения к базе данных
# и представляет «промежуточную зону» для всех объектов,
# загруженных в объект сессии базы данных.
DBSession = sessionmaker(bind=engine)

# Для создания, удаления, чтения или обновления записей в базе данных
# SQLAlchemy предоставляет интерфейс под названием Session
session = DBSession()


class Database:
    def __init__(self, _session):
        self._session = _session

    def create_new_user(self, user_id: int, full_name: str, username: str, chat_id: int, config_filename: str,
                        is_admin: bool = False, ip_address: str = None) -> None:
        new_user = User(id=user_id, full_name=full_name, username=username, chat_id=chat_id, is_admin=is_admin,
                        config_filename=config_filename, ip_address=ip_address)
        self._session.add(new_user)
        self._session.commit()

    def get_all_ip_addresses(self) -> list:
        all_ip_addresses = self._session.query(User.ip_address).all()
        return all_ip_addresses

    def get_all_users(self):
        all_users = self._session.query(User).all()
        return all_users

    def get_config_filename(self, user_id: int) -> str:
        user = self._session.query(User).filter_by(id=user_id).first()
        return user.config_filename

    def get_all_config(self): ...

    def delete_user(self, user_id: int) -> None:
        user = self._session.query(User).filter_by(id=user_id).first()
        self._session.delete(user)
        self._session.commit()

    def get_user(self, user_id: int) -> User:
        user = self._session.query(User).filter_by(id=user_id).first()
        return user

    def user_is_admin(self, user_id: int) -> bool:
        user = self._session.query(User).filter_by(id=user_id).first()
        return user.is_admin


db = Database(session)
