from .package.configuration import ConfigurationManager
from .package.models.database import DatabaseManager
from .package.models import (
    user as m_user,
    session as m_session
    )

from typing import Any, Callable
from airflow.www.security import FabAirflowSecurityManagerOverride

class DataflowAirflowAuthenticator(FabAirflowSecurityManagerOverride):
    def __init__(self, wsgi_app: Callable) -> None:
        self.wsgi_app = wsgi_app

        # Dataflow database configuration
        self.dataflow_config = ConfigurationManager('/dataflow/app/config/dataflow.cfg')
        self.dataflow_database_url = self.dataflow_config.get_config_value('database', 'database_url')

        self.dataflow_db_instance = DatabaseManager(self.dataflow_database_url)
        self.dataflow_db = next(self.dataflow_db_instance.get_session())

        # Airflow database configuration
        self.airflow_config = ConfigurationManager('airflow.cfg')
        self.airflow_database_url = self.airflow_config.get_config_value('database', 'sql_alchemy_conn')
        
        self.airflow_db_instance = DatabaseManager(self.airflow_database_url)
        self.airflow_db = next(self.airflow_db_instance.get_session())

        m_user.Base.metadata.create_all(bind=self.dataflow_db_instance.get_engine())
        m_session.Base.metadata.create_all(bind=self.dataflow_db_instance.get_engine())

    def __call__(self, environ: dict, start_response: Callable) -> Any:

        path = environ.get('PATH_INFO', '')
        if not path == '/login/':
            return self.wsgi_app(environ, start_response)

        try:
            # Extracting browser cookies
            cookies = environ.get('HTTP_COOKIE', '')
            user_session_id = None
            parts = cookies.split('; ')
            for part in parts:
                if part.startswith('dataflow_session='):
                    user_session_id = part
                    break

            if user_session_id is None:
                raise Exception("No session id found")
            
            user_session_id = user_session_id.split('=')[1]

            # Retrieving user details
            user_data = self.find_dataflow_user(user_session_id)

            if user_data is None:
                raise Exception("No user found for the dataflow_session id")
            
            user = self.find_user(user_data.user_name)

            if not user:
                user_role = self.find_role(user_data.role.title())
                user = self.add_user(username=user_data.user_name, first_name=self.not_none(user_data.first_name), last_name=self.not_none(user_data.last_name), email=self.not_none(user_data.email), role=user_role, password=self.not_none(user_data.password))

            environ['REMOTE_USER'] = user.username
            self.write_user_id(user_data.user_id)
            return self.wsgi_app(environ, start_response)

        except Exception as e:
            return self.wsgi_app(environ, start_response)
    
    def not_none(self, value):
        return value if value is not None else ""
    
    def find_dataflow_user(self, user_session_id):
        """Find user by session_id in dataflow database."""
        query = self.dataflow_db.query(m_session.Session_table)
        session = query.filter(m_session.Session_table.session_id == user_session_id).first()
        if session is None:
            return None

        user_data = self.dataflow_db.query(m_user.User).filter(m_user.User.user_id == session.user_id).first()
        if user_data is None:
            return None
        
        return user_data

    def find_user(self, username=None):
        """Find user by username or email."""
        return self.airflow_db.query(self.user_model).filter_by(username=username).one_or_none()

    def find_role(self, role):
        """Find a role in the database."""
        return self.airflow_db.query(self.role_model).filter_by(name=role).one_or_none()

    def add_user(self, username, first_name, last_name, email, role, password=""):
        """Create a user."""
        user = self.user_model()
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.active = True
        user.roles = role if isinstance(role, list) else [role]
        user.password = password
        self.airflow_db.add(user)
        self.airflow_db.commit()
        return user

    def write_user_id(self, user_id):
        """
        Write the given user_id to a file named dataflow_user_id.txt.
        
        Args:
            user_id (str): The user ID to be written to the file.
        """
        file_name = 'dataflow_user_id.txt'
        with open(file_name, 'w') as file:
            file.write(str(user_id))

        