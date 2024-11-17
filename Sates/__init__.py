from flask import Flask
from flask_bcrypt import  Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)

# Configure the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///satellite.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY']= '9200cd4bb68d616a50925a5c'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
# Initialize the database
db = SQLAlchemy(app)

from Sates import routes