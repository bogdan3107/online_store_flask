from app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    decription = db.Column(db.String(140), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)