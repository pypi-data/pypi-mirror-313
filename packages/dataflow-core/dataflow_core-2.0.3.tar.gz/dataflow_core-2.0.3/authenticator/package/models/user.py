"""models.py"""
from sqlalchemy import Column, Integer, String, LargeBinary, Enum
from sqlalchemy.ext.declarative import declarative_base

#instance for create declarative base
Base=declarative_base()

class User(Base):
    """
    Table USER
    """

    __tablename__='USER'

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_name = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    role = Column(Enum('admin', 'user', name='role_field'), nullable=False)
    image = Column(LargeBinary)
    active = Column(Enum('N', 'Y', name='active_field'), nullable=False, server_default=str("N"))
    password = Column(String, nullable=False)