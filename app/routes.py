from flask import request, jsonify
from app import app, db
from app.models import City, Hotel, Excursion, ContactRequest
from flask_login import login_required, current_user
from flask import redirect, url_for, render_template
from app.models import Attraction, Banner

@app.route("/")
def home_redirect():
    return redirect(url_for("login"))  # login — имя функции-обработчика

# Cities
@app.route("/api/cities", methods=["GET"])
def get_cities():
    cities = City.query.all()
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify([c.to_dict(include_relations=include_relations) for c in cities])

@app.route("/api/cities", methods=["POST"])
@login_required
def add_city():
    data = request.json
    city = City(name=data['name'], image=data.get('image'))
    db.session.add(city)
    db.session.commit()
    return jsonify({"message": "City added successfully"})

@app.route("/api/cities/<int:city_id>", methods=["PUT"])
@login_required
def update_city(city_id):
    city = City.query.get_or_404(city_id)
    data = request.json
    city.name = data['name']
    city.image = data.get('image', city.image)
    db.session.commit()
    return jsonify({"message": "City updated successfully"})

@app.route("/api/cities/<int:city_id>", methods=["DELETE"])
@login_required
def delete_city(city_id):
    city = City.query.get_or_404(city_id)
    db.session.delete(city)
    db.session.commit()
    return jsonify({"message": "City deleted successfully"})

@app.route("/api/cities/<int:city_id>", methods=["GET"])
def get_city(city_id):
    city = City.query.get_or_404(city_id)
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify(city.to_dict(include_relations=include_relations))

# Hotels
@app.route("/api/hotels", methods=["GET"])
def get_hotels():
    city_id = request.args.get('city_id')
    
    if city_id:
        hotels = Hotel.query.filter_by(city_id=city_id).all()
    else:
        hotels = Hotel.query.all()
    
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify([h.to_dict(include_relations=include_relations) for h in hotels])

@app.route("/api/hotels", methods=["POST"])
@login_required
def add_hotel():
    data = request.json
    hotel = Hotel(
        name=data['name'],
        price=data['price'],
        description=data.get('description'),
        image=data.get('image'),
        rating=data.get('rating'),
        city_id=data['city_id']
    )
    db.session.add(hotel)
    db.session.commit()
    return jsonify({"message": "Hotel added successfully"})

@app.route("/api/hotels/<int:hotel_id>", methods=["PUT"])
@login_required
def update_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    data = request.json
    hotel.name = data['name']
    hotel.price = data['price']
    hotel.description = data.get('description')
    hotel.image = data.get('image')
    hotel.rating = data.get('rating')
    hotel.city_id = data.get('city_id', hotel.city_id)
    db.session.commit()
    return jsonify({"message": "Hotel updated successfully"})

@app.route("/api/hotels/<int:hotel_id>", methods=["DELETE"])
@login_required
def delete_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    db.session.delete(hotel)
    db.session.commit()
    return jsonify({"message": "Hotel deleted successfully"})

@app.route("/api/hotels/<int:hotel_id>", methods=["GET"])
def get_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify(hotel.to_dict(include_relations=include_relations))

# Excursions
@app.route("/api/excursions", methods=["GET"])
def get_excursions():
    city_id = request.args.get('city_id')
    excursion_type = request.args.get('type')
    
    query = Excursion.query
    
    if city_id:
        query = query.filter_by(city_id=city_id)
    if excursion_type:
        query = query.filter_by(type=excursion_type)
    
    excursions = query.all()
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify([e.to_dict(include_relations=include_relations) for e in excursions])

@app.route("/api/excursions", methods=["POST"])
@login_required
def add_excursion():
    data = request.json
    excursion = Excursion(
        name=data['name'],
        description=data.get('description'),
        price=data.get('price'),
        image=data.get('image'),
        type=data.get('type', 'city'),  # city или historical
        city_id=data['city_id'],
        duration_hours=data.get('duration_hours')
    )
    db.session.add(excursion)
    db.session.commit()
    return jsonify({"message": "Excursion added successfully"})

@app.route("/api/excursions/<int:excursion_id>", methods=["PUT"])
@login_required
def update_excursion(excursion_id):
    excursion = Excursion.query.get_or_404(excursion_id)
    data = request.json
    excursion.name = data['name']
    excursion.description = data.get('description')
    excursion.price = data.get('price')
    excursion.image = data.get('image')
    excursion.type = data.get('type', excursion.type)
    excursion.duration_hours = data.get('duration_hours')
    db.session.commit()
    return jsonify({"message": "Excursion updated successfully"})

@app.route("/api/excursions/<int:excursion_id>", methods=["DELETE"])
@login_required
def delete_excursion(excursion_id):
    excursion = Excursion.query.get_or_404(excursion_id)
    db.session.delete(excursion)
    db.session.commit()
    return jsonify({"message": "Excursion deleted successfully"})

@app.route("/api/excursions/<int:excursion_id>", methods=["GET"])
def get_excursion(excursion_id):
    excursion = Excursion.query.get_or_404(excursion_id)
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify(excursion.to_dict(include_relations=include_relations))

# Attractions
@app.route("/api/attractions", methods=["GET"])
def get_attractions():
    city_id = request.args.get('city_id')
    attraction_type = request.args.get('type')
    
    query = Attraction.query
    
    if city_id:
        query = query.filter_by(city_id=city_id)
    if attraction_type:
        query = query.filter_by(type=attraction_type)
    
    attractions = query.all()
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify([a.to_dict(include_relations=include_relations) for a in attractions])

@app.route("/api/attractions", methods=["POST"])
@login_required
def add_attraction():
    data = request.json
    attraction = Attraction(
        name=data["name"],
        description=data.get("description"),
        type=data.get("type", "city"),
        image=data.get("image"),
        city_id=data["city_id"]
    )
    db.session.add(attraction)
    db.session.commit()
    return jsonify({"message": "Attraction added successfully"})

@app.route("/api/attractions/<int:attraction_id>", methods=["PUT"])
@login_required
def update_attraction(attraction_id):
    attraction = Attraction.query.get_or_404(attraction_id)
    data = request.json
    attraction.name = data["name"]
    attraction.description = data.get("description")
    attraction.type = data.get("type", attraction.type)
    attraction.image = data.get("image", attraction.image)
    attraction.city_id = data.get("city_id", attraction.city_id)
    db.session.commit()
    return jsonify({"message": "Attraction updated successfully"})

@app.route("/api/attractions/<int:attraction_id>", methods=["DELETE"])
@login_required
def delete_attraction(attraction_id):
    attraction = Attraction.query.get_or_404(attraction_id)
    db.session.delete(attraction)
    db.session.commit()
    return jsonify({"message": "Attraction deleted successfully"})

@app.route("/api/attractions/<int:attraction_id>", methods=["GET"])
def get_attraction(attraction_id):
    attraction = Attraction.query.get_or_404(attraction_id)
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify(attraction.to_dict(include_relations=include_relations))

# Banners
@app.route("/api/banners", methods=["GET"])
def get_banners():
    banners = Banner.query.all()
    return jsonify([b.to_dict() for b in banners])

@app.route("/api/banners", methods=["POST"])
@login_required
def add_banner():
    data = request.json
    banner = Banner(image=data["image"])
    db.session.add(banner)
    db.session.commit()
    return jsonify({"message": "Banner added successfully"})

@app.route("/api/banners/<int:banner_id>", methods=["DELETE"])
@login_required
def delete_banner(banner_id):
    banner = Banner.query.get_or_404(banner_id)
    db.session.delete(banner)
    db.session.commit()
    return jsonify({"message": "Banner deleted successfully"})

@app.route("/api/banners/<int:banner_id>", methods=["GET"])
def get_banner(banner_id):
    banner = Banner.query.get_or_404(banner_id)
    return jsonify(banner.to_dict())

# Contact Requests
@app.route("/api/contact", methods=["POST"])
def send_contact():
    data = request.json
    contact = ContactRequest(
        name=data['name'],
        email=data['email'],
        message=data['message']
    )
    db.session.add(contact)
    db.session.commit()
    return jsonify({"message": "Contact request sent successfully"})

# Дополнительные удобные endpoints для фронтенда
@app.route("/api/cities/<int:city_id>/hotels", methods=["GET"])
def get_city_hotels(city_id):
    city = City.query.get_or_404(city_id)
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify([hotel.to_dict(include_relations=include_relations) for hotel in city.hotels])

@app.route("/api/cities/<int:city_id>/excursions", methods=["GET"])
def get_city_excursions(city_id):
    city = City.query.get_or_404(city_id)
    excursion_type = request.args.get('type')
    
    excursions = city.excursions
    if excursion_type:
        excursions = [exc for exc in excursions if exc.type == excursion_type]
    
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify([excursion.to_dict(include_relations=include_relations) for excursion in excursions])

@app.route("/api/cities/<int:city_id>/attractions", methods=["GET"])
def get_city_attractions(city_id):
    city = City.query.get_or_404(city_id)
    attraction_type = request.args.get('type')
    
    attractions = city.attractions
    if attraction_type:
        attractions = [attr for attr in attractions if attr.type == attraction_type]
    
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify([attraction.to_dict(include_relations=include_relations) for attraction in attractions])