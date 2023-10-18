from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    description = db.Column(db.String(140), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)

