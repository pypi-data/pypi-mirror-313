"""models.py"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

#instance for create declarative base
Base=declarative_base()

class Session_table(Base):
    """
    Table SESSIONS
    """

    __tablename__='SESSION'

    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False, autoincrement=True)
    session_id = Column(String, unique=True, nullable=False)
    user_id = Column(String, nullable=False)    


    