from flask import Flask
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)

# Configure the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///satellite.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Initialize the database
db = SQLAlchemy(app)

from Sates import routes