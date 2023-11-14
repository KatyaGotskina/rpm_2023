from flask import Flask
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os, config
from app.api import api_bp


app = Flask(__name__)
app.config.from_object('config.DevelopementConfig')

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)
app.register_blueprint(api_bp, url_prefix="/api")

from . import admin_view
from . import app_routes
from . import views