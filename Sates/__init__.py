from flask import Flask
from flask_bcrypt import  Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy 
import os
from decouple import config


app = Flask(__name__)

# Configure the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///satellite.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
SECRET_KEY = config('SECRET_KEY')
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
# Initialize the database
db = SQLAlchemy(app)

from Sates import routes