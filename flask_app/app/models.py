from sqlalchemy import DECIMAL
from sqlalchemy.dialects.postgresql import UUID
import uuid
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship
from app import db 


metadata = db.metadata
DEFAULT_STRING_VALUE = 100


class UUIDMixin:
    """Inherit to add uuid primary key column to a model."""
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class User(UUIDMixin, UserMixin, db.Model): 
    first_name = db.Column(db.String(DEFAULT_STRING_VALUE), nullable=False)
    last_name = db.Column(db.String(DEFAULT_STRING_VALUE), nullable=False)
    surname = db.Column(db.String(DEFAULT_STRING_VALUE))
    username = db.Column(db.String(DEFAULT_STRING_VALUE), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(DEFAULT_STRING_VALUE), nullable=False, unique=True)
    roles = relationship("Role", secondary="roles_for_users", back_populates="users")

class Role(UUIDMixin, db.Model):
    name = db.Column(db.String(DEFAULT_STRING_VALUE), nullable=False)
    users = relationship("User", secondary="roles_for_users", back_populates="roles")


class RolesForUsers(UUIDMixin, db.Model):
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.id'))


class Categories(UUIDMixin, db.Model):
    name = db.Column(db.String(DEFAULT_STRING_VALUE), unique=True)
    supercategory_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'categories.id', ondelete='SET NULL'), nullable=True)


class Orders(UUIDMixin, db.Model):
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = name = db.Column(db.String(DEFAULT_STRING_VALUE))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'user.id', ondelete='SET NULL'), nullable=True)


class Products(UUIDMixin, db.Model):
    name = db.Column(db.String(DEFAULT_STRING_VALUE))
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'categories.id', ondelete='SET NULL'), nullable=True)
    weight = db.Column(db.Float, nullable=True)
    description = db.Column(db.String, nullable=True)
    composition = db.Column(db.String, nullable=True)
    storage_conditions = db.Column(db.String(DEFAULT_STRING_VALUE), nullable=True)
    number = db.Column(db.Integer, nullable=True)
    price = db.Column(DECIMAL(precision=10, scale=2), nullable=False)
    prod_status = db.Column(db.String(DEFAULT_STRING_VALUE))
    image_path = db.Column(db.String(DEFAULT_STRING_VALUE))


class OrdersToProducts(UUIDMixin, db.Model):
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'products.id', ondelete='SET NULL'), nullable=True)
    number = db.Column(db.Integer)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'orders.id', ondelete='CASCADE'), nullable=True)
