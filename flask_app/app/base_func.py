from .models import User, Products
from flask_login import current_user


def get_current_user():
    return User.query.get(current_user.get_id())


def get_prod_by_id(product_id):
    return Products.query.get(product_id)
