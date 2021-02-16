from helper import db

class BmeEntity(db.Model):

    __tablename__ = 'analytics'

    id = db.Column(db.Integer(), primary_key=True)
    temperature = db.Column(db.Float())
    gas = db.Column(db.Integer())
    humidity = db.Column(db.Float())
    pressure = db.Column(db.Float())
    time = db.Column(db.String(20))