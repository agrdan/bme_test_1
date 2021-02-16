class Configuration:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///analytics.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)