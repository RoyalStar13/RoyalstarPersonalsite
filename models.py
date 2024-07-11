from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=True)
