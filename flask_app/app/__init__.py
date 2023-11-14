from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from app.api import api_bp
from .models import db


app = Flask(__name__)
app.config.from_object('config.DevelopementConfig')


db.init_app(app)
mail = Mail(app)
login_manager = LoginManager(app)
app.register_blueprint(api_bp, url_prefix="/api")

from . import admin_view
from . import app_routes
from . import views