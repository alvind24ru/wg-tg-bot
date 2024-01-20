from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(255))
    username = Column(String(255))
    chat_id = Column(Integer, nullable=False)
    is_admin = Column(Boolean, default=False)
    ip_address = relationship('Ip_addresses')


class Ip_addresses(Base):
    __tablename__ = 'ip_addresses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(20))
    user_id = Column(Integer, ForeignKey('users.id'))


engine = create_engine('sqlite:///database/wireguard.db')
Base.metadata.create_all(engine)
