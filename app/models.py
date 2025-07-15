from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

hotel_excursion = db.Table('hotel_excursion',
    db.Column('hotel_id', db.Integer, db.ForeignKey('hotel.id'), primary_key=True),
    db.Column('excursion_id', db.Integer, db.ForeignKey('excursion.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(200))
    hotels = db.relationship('Hotel', backref='city', lazy=True)
    attractions = db.relationship('Attraction', backref='city', lazy=True)

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    rating = db.Column(db.Float)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    excursions = db.relationship('Excursion', secondary=hotel_excursion, backref='hotels')

class Excursion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    image = db.Column(db.String(200))

class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer)
    image = db.Column(db.String(200))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

class ContactRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)