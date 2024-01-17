from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	full_name = Column(String(255))
	username = Column(String(255))
	chat_id = Column(Integer, nullable=False)
	is_admin = Column(Boolean, default=False)
	ip_address = Column(String(255))

engine = create_engine('sqlite:///wireguard.db')
Base.metadata.create_all(engine)

