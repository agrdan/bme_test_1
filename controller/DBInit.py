from model.BmeEntity import BmeEntity
from helper import db

class DBInit:

    def __init__(self):
        db.create_all()