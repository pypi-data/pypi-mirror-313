import os
from .configuration import ConfigurationManager
from .models import (
    session as m_session,
    user as m_user,
)
from .models.database import DatabaseManager
from sqlalchemy.inspection import inspect
from .utils.aws_secrets_manager import SecretsManagerClient
import json


class Dataflow:
    def __init__(self):
        self.dataflow_config = ConfigurationManager('/dataflow/app/config/dataflow.cfg')
        self.dataflow_database_url = self.dataflow_config.get_config_value('database', 'database_url')

        self.dataflow_db_instance = DatabaseManager(self.dataflow_database_url)
        self.dataflow_db = next(self.dataflow_db_instance.get_session())

        self.secrets_manager = SecretsManagerClient('us-east-1')

        m_user.Base.metadata.create_all(bind=self.dataflow_db_instance.get_engine())
        m_session.Base.metadata.create_all(bind=self.dataflow_db_instance.get_engine())

    def auth(self, session_id: str):
        """Find user by session_id in dataflow database."""
        try:
            query = self.dataflow_db.query(m_session.Session_table)
            session = query.filter(m_session.Session_table.session_id == session_id).first()
            if session is None:
                return False

            user_data = self.dataflow_db.query(m_user.User).filter(m_user.User.user_id == session.user_id).first()
            if user_data is None:
                return False
            
            user_dict = {"user_name": user_data.user_name, "name": f"{user_data.first_name} {user_data.last_name}", "email": user_data.email, "role": user_data.role}
            return user_dict
        
        except Exception as e:
            return False
    
    def variable(self, variable_name: str):
        """Get variable value from secrets manager."""
        try:
            host_name = os.environ["HOSTNAME"]
            user_name = host_name.replace("jupyter-","")
            
            vault_path = "variables"
            variable_data =  self.secrets_manager.get_secret_by_key(vault_path, user_name, variable_name)
            return variable_data['value']
            
        except Exception as e:
            return None
        
    def connection(self, conn_id: str):
        """Get connection details from secrets manager."""
        try:
            host_name = os.environ["HOSTNAME"]
            user_name=host_name.replace("jupyter-","")
            
            vault_path = "connections"
            secret = self.secrets_manager.get_secret_by_key(vault_path, user_name, conn_id)

            conn_type = secret['conn_type'].lower()
            username = secret['login']
            password = secret.get('password', '')
            host = secret['host']
            port = secret['port']
            database = secret.get('schemas', '')

            user_info = f"{username}:{password}@" if password else f"{username}@"
            db_info = f"/{database}" if database else ""

            connection_string = f"{conn_type}://{user_info}{host}:{port}{db_info}"

            extra = secret.get('extra', '')
            if extra:
                try:
                    extra_params = json.loads(extra)
                    if extra_params:
                        extra_query = "&".join(f"{key}={value}" for key, value in extra_params.items())
                        connection_string += f"?{extra_query}"
                except json.JSONDecodeError:
                    # If 'extra' is not valid JSON, skip adding extra parameters
                    pass

            connection_instance = DatabaseManager(connection_string)
            return next(connection_instance.get_session())
        
        except Exception as e:
            return None
