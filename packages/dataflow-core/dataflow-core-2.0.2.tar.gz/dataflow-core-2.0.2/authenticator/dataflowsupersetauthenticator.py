from flask import redirect, request
from flask_appbuilder.security.views import AuthDBView
from superset.security import SupersetSecurityManager
from flask_appbuilder.security.views import expose
from flask_login import login_user
from .package.configuration import ConfigurationManager
from .package.models.database import DatabaseManager
from .package.models import (
    user as m_user,
    session as m_session
    )

class CustomAuthDBView(AuthDBView):
    def __init__(self):
        self.dataflow_config = ConfigurationManager('/dataflow/app/config/dataflow.cfg')
        self.dataflow_database_url = self.dataflow_config.get_config_value('database', 'database_url')
        self.dataflow_db_instance = DatabaseManager(self.dataflow_database_url)
        self.dataflow_db = next(self.dataflow_db_instance.get_session())
        m_user.Base.metadata.create_all(bind=self.dataflow_db_instance.get_engine())
        m_session.Base.metadata.create_all(bind=self.dataflow_db_instance.get_engine())

    def _get_user_id_from_session(self, session_id):
        query = self.dataflow_db.query(m_session.Session_table).filter(m_session.Session_table.session_id == session_id).first()
        return query.user_id if query!=None else None

    def _get_user_details_from_user_table(self, user_id):
        user_details = self.dataflow_db.query(m_user.User).filter(m_user.User.user_id == user_id).first()
        return user_details if user_details!=None else None
    
    def not_none(self, value):
        return value if value is not None else ""

    @expose('/login/', methods=['GET'])
    def login(self):
        try:
            session_id = request.cookies.get('dataflow_session')
            
            user_id = self._get_user_id_from_session(session_id)
            user_details = self._get_user_details_from_user_table(user_id)
            user = self.appbuilder.sm.find_user(username=user_details.user_name)
            if user:
                login_user(user, remember=False)
            else:
                user = self.appbuilder.sm.add_user(username=self.not_none(user_details.user_name), first_name=self.not_none(user_details.first_name), last_name=self.not_none(user_details.last_name), email=self.not_none(user_details.email), role=self.appbuilder.sm.find_role('Admin'), password=self.not_none(user_details.password))
                if user:
                    login_user(user, remember=False)
                    
            return redirect(self.appbuilder.get_url_for_index)

        except Exception as e:
            return super().login()


class CustomSecurityManager(SupersetSecurityManager):
    authdbview = CustomAuthDBView
    def __init__(self, appbuilder):
        super(CustomSecurityManager, self).__init__(appbuilder)