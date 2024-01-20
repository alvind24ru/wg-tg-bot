# from ipaddress import ip_address
# from tkinter.tix import ComboBox
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

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


engine = create_engine('sqlite:///wireguardtest.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 = User(id=1, full_name='testname1', username='test1',
             chat_id=123, is_admin=False)

session.add(user1)
session.commit()
ip = [Ip_addresses(address=ip, user_id=1)
      for ip in ['10.0.0.1', '10.0.0.2', '10.0.0.3']]
session.add_all(ip)
session.commit()
us = session.query(User).filter_by(id=1).first()
print(us.)
