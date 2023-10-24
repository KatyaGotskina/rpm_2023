from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DECIMAL
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from config import *


db = SQLAlchemy()


class UUIDMixin:
    """Inherit to add uuid primary key column to a model."""
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class User(UUIDMixin, db.Model):
    first_name = db.Column(db.String(DEFAULT_STRING_VALUE), nullable=False)
    last_name = db.Column(db.String(DEFAULT_STRING_VALUE), nullable=False)
    surname = db.Column(db.String(DEFAULT_STRING_VALUE))
    username = db.Column(db.String(DEFAULT_STRING_VALUE), nullable=False)
    password = db.Column(db.String(DEFAULT_STRING_VALUE), nullable=False)
    email = db.Column(db.String(DEFAULT_STRING_VALUE), nullable=False, unique=True)


class Categories(UUIDMixin, db.Model):
    name = db.Column(db.String(DEFAULT_STRING_VALUE), unique=True)
    supercategory_id = db.Colomn(UUID(as_uuid=True), db.ForeignKey(
        'categories.id'), ondelete='PROTECT', nullable=True)


class Orders(UUIDMixin, db.Model):
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = name = db.Column(db.String(DEFAULT_STRING_VALUE))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'user.id'), ondelete='SET_NULL', nullable=True)


class Products(UUIDMixin, db.Model):
    name = db.Colomn(db.String(DEFAULT_STRING_VALUE))
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'categories.id'), ondelete='PROTECT', nullable=True)
    weight = db.Column(db.Float, nullable=True)
    description = db.Column(db.String, nullable=True)
    composition = db.Column(db.String, nullable=True)
    storage_conditions = db.Colomn(db.String(DEFAULT_STRING_VALUE), nullable=True)
    number = db.Column(db.Integer, nullable=True)
    price = db.Column(DECIMAL(precision=10, scale=2), nullable=False)
    status = db.Column(db.String(DEFAULT_STRING_VALUE))
    image_path = db.Column(db.String(DEFAULT_STRING_VALUE))


class OrdersToProducts(db.Model):
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'products.id'), ondelete='PROTECT', nullable=True)
    number = db.Column(db.Integer)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'orders'), ondelete='CASCADE', nullable=True)
