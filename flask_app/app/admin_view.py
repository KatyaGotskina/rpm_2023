from flask_login import current_user
from flask import redirect, url_for
from flask_admin import expose
from app.models import User
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, expose, BaseView, AdminIndexView
from app import app
from .models import User, Products, Categories, db


class ProtectedIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('signin'))
        admin = User.query.get(current_user.get_id())
        if 'admin' in [role.name for role in admin.roles]:
            return super(ProtectedIndexView, self).index()
        return redirect(url_for('signin'))


class ProtectedModelView(ModelView):
    column_hide_backrefs = False

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        admin = User.query.get(current_user.get_id())
        if 'admin' in [role.name for role in admin.roles]:
            return True
        return False


class ProductsView(BaseView):
    def is_accessible(self):
        return 'admin' in [role.name for role in User.query.get(current_user.get_id()).roles]

    @expose("/")
    def products(self):
        return self.render('admin/admin.html')

    @expose("/archive")
    def archive_products(self):
        return self.render('admin/archive.html')


admin = Admin(app, index_view=ProtectedIndexView())
admin.add_view(ProductsView(name='work_with_products')) #, endpoint=
admin.add_view(ProtectedModelView(Products, db.session))
admin.add_view(ProtectedModelView(Categories, db.session))