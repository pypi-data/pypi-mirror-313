"""models/database.py"""
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_engine(self):
        try:
            engine = create_engine(self.db_url)
            return engine
        except SQLAlchemyError as e:
            raise e
        
    def get_session(self):
        try:
            engine = self.get_engine()
            session = sessionmaker(autocommit=False, autoflush=False, bind=engine or create_engine(self.db_url))
            db = session()
            try:
                yield db
            finally:
                db.close()

        except SQLAlchemyError as e:
            raise e
    
    def get_base(self):
        return declarative_base()
