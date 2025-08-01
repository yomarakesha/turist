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

excursion_attraction = db.Table('excursion_attraction',
    db.Column('excursion_id', db.Integer, db.ForeignKey('excursion.id'), primary_key=True),
    db.Column('attraction_id', db.Integer, db.ForeignKey('attraction.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_ru = db.Column(db.String(50), nullable=False)
    name_en = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(200))
    excursions = db.relationship('Excursion', backref='city', lazy=True)
    
    def to_dict(self, include_relations=False):
        data = {
            'id': self.id,
            'name_ru': self.name_ru,
            'name_en': self.name_en,
            'image': self.image
        }
        
        if include_relations:
            data['hotels'] = [hotel.to_dict() for hotel in self.hotels]
            data['excursions'] = [excursion.to_dict() for excursion in self.excursions]
            data['attractions'] = [attraction.to_dict() for attraction in self.attractions]
            
        return data

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_ru = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description_ru = db.Column(db.Text)
    description_en = db.Column(db.Text)
    image = db.Column(db.String(200))
    rating = db.Column(db.Float)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    excursions = db.relationship('Excursion', secondary=hotel_excursion, backref='hotels')
    city = db.relationship('City', backref='hotels')
    
    def to_dict(self, include_relations=False):
        data = {
            'id': self.id,
            'name_ru': self.name_ru,
            'name_en': self.name_en,
            'price': self.price,
            'description_ru': self.description_ru,
            'description_en': self.description_en,
            'image': self.image,
            'rating': self.rating,
            'city': {
                'id': self.city.id,
                'name_ru': self.city.name_ru,
                'name_en': self.city.name_en,
                'image': self.city.image
            } if self.city else None
        }
        
        if include_relations:
            data['excursions'] = [excursion.to_dict() for excursion in self.excursions]
            
        return data

class Excursion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_ru = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    description_ru = db.Column(db.Text)
    description_en = db.Column(db.Text)
    price = db.Column(db.Integer)
    image = db.Column(db.String(200))
    type = db.Column(db.String(50), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    duration_hours = db.Column(db.Float)
    attractions = db.relationship('Attraction', secondary=excursion_attraction, backref='excursions')
    
    def to_dict(self, include_relations=False):
        data = {
            'id': self.id,
            'name_ru': self.name_ru,
            'name_en': self.name_en,
            'description_ru': self.description_ru,
            'description_en': self.description_en,
            'price': self.price,
            'image': self.image,
            'type': self.type,
            'duration_hours': self.duration_hours,
            'city': {
                'id': self.city.id,
                'name_ru': self.city.name_ru,
                'name_en': self.city.name_en,
                'image': self.city.image
            } if self.city else None
        }
        
        if include_relations:
            data['attractions'] = [attraction.to_dict() for attraction in self.attractions]
            data['hotels'] = [hotel.to_dict() for hotel in self.hotels]
            
        return data

class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_ru = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    description_ru = db.Column(db.Text)
    description_en = db.Column(db.Text)
    type = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(200))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    city = db.relationship('City', backref='attractions')
    
    def to_dict(self, include_relations=False):
        data = {
            'id': self.id,
            'name_ru': self.name_ru,
            'name_en': self.name_en,
            'description_ru': self.description_ru,
            'description_en': self.description_en,
            'type': self.type,
            'image': self.image,
            'city': {
                'id': self.city.id,
                'name_ru': self.city.name_ru,
                'name_en': self.city.name_en,
                'image': self.city.image
            } if self.city else None
        }
        
        if include_relations:
            data['excursions'] = [excursion.to_dict() for excursion in self.excursions]
            
        return data



class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'image': self.image
        }