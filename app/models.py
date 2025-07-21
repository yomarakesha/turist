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
# связь экскурсии и достопримечательностей
excursion_attraction = db.Table('excursion_attraction',
    db.Column('excursion_id', db.Integer, db.ForeignKey('excursion.id'), primary_key=True),
    db.Column('attraction_id', db.Integer, db.ForeignKey('attraction.id'), primary_key=True)
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
    excursions = db.relationship('Excursion', backref='city', lazy=True)

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    rating = db.Column(db.Float)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    excursions = db.relationship('Excursion', secondary=hotel_excursion, backref='hotels')
    city = db.relationship('City', backref='hotels')

class Excursion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    image = db.Column(db.String(200))
    type = db.Column(db.String(50), nullable=False)  # 'historical' или 'city'
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    duration_hours = db.Column(db.Float)  # длительность в часах
    attractions = db.relationship('Attraction', secondary=excursion_attraction, backref='excursions')

class ContactRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50), nullable=False)  # 'historical' или 'city'
    image = db.Column(db.String(200))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    city = db.relationship('City', backref='attractions')


class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200), nullable=False)
