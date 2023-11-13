import flask_admin
import flask_login as login
from flask import redirect, url_for
from flask_admin import expose
from models import User
from flask_admin.contrib.sqla import ModelView


class ProtectedIndexView(flask_admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('signin'))
        admin = User.query.get(login.current_user.get_id())
        return super(ProtectedIndexView, self).index()
        #return redirect(url_for('login'))


class ProtectedModelView(ModelView):
    column_hide_backrefs = False

    def is_accessible(self):
        if not login.current_user.is_authenticated:
            return False
        admin = User.query.get(login.current_user.get_id())
        return True