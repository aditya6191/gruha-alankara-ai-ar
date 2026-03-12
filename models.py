from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    designs = db.relationship('Design', backref='user', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Design(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_type = db.Column(db.String(50))
    style_preference = db.Column(db.String(50))
    original_image_path = db.Column(db.String(255))
    generated_image_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FurnitureItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    model_3d_path = db.Column(db.String(255))
    category = db.Column(db.String(50))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    furniture_item_id = db.Column(db.Integer, db.ForeignKey('furniture_item.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

