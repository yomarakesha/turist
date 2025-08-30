from flask import request, jsonify
from app import app, db, mail
from app.models import City, Hotel, Excursion, Contact, Attraction, Banner
from flask_login import login_required, current_user
from flask import redirect, url_for, render_template
from flask_mail import Message
import os

@app.route("/")
def home_redirect():
    return redirect(url_for("login"))  # login — имя функции-обработчика

# Cities
@app.route("/api/cities", methods=["GET"])
def get_cities():
    search = request.args.get('search')
    query = City.query
    if search:
        search_pattern = f"%{search}%"
        query = query.filter((City.name_ru.ilike(search_pattern)) | (City.name_en.ilike(search_pattern)))
    cities = query.all()
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify([c.to_dict(include_relations=include_relations) for c in cities])





@app.route("/api/cities/<int:city_id>", methods=["GET"])
def get_city(city_id):
    city = City.query.get_or_404(city_id)
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify(city.to_dict(include_relations=include_relations))

# Hotels
@app.route("/api/hotels", methods=["GET"])
def get_hotels():
    city_id = request.args.get('city_id')
    search = request.args.get('search')
    query = Hotel.query
    if city_id:
        query = query.filter_by(city_id=city_id)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter((Hotel.name_ru.ilike(search_pattern)) | (Hotel.name_en.ilike(search_pattern)))
    hotels = query.all()
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify([h.to_dict(include_relations=include_relations) for h in hotels])





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
    search = request.args.get('search')
    query = Excursion.query
    if city_id:
        query = query.filter_by(city_id=city_id)
    if excursion_type:
        query = query.filter_by(type=excursion_type)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter((Excursion.name_ru.ilike(search_pattern)) | (Excursion.name_en.ilike(search_pattern)))
    excursions = query.all()
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify([e.to_dict(include_relations=include_relations) for e in excursions])





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
    search = request.args.get('search')
    query = Attraction.query
    if city_id:
        query = query.filter_by(city_id=city_id)
    if attraction_type:
        query = query.filter_by(type=attraction_type)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter((Attraction.name_ru.ilike(search_pattern)) | (Attraction.name_en.ilike(search_pattern)))
    attractions = query.all()
    include_relations = request.args.get('include_relations', 'false').lower() == 'true'
    return jsonify([a.to_dict(include_relations=include_relations) for a in attractions])





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





@app.route("/api/banners/<int:banner_id>", methods=["GET"])
def get_banner(banner_id):
    banner = Banner.query.get_or_404(banner_id)
    return jsonify(banner.to_dict())

# Contact Requests


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

# Контактные формы
@app.route("/api/contact", methods=["POST"])
def submit_contact():
    try:
        data = request.get_json()
        
        # Валидация данных
        if not data or not all(key in data for key in ['name', 'email', 'comment']):
            return jsonify({'error': 'Не все обязательные поля заполнены'}), 400
        
        name = data['name'].strip()
        email = data['email'].strip()
        comment = data['comment'].strip()
        
        if not name or not email or not comment:
            return jsonify({'error': 'Все поля должны быть заполнены'}), 400
        
        # Создание записи в базе данных
        contact = Contact(
            name=name,
            email=email,
            comment=comment
        )
        
        db.session.add(contact)
        db.session.commit()
        
        # Отправка email
        try:
            msg = Message(
                subject=f'Новое сообщение от {name}',
                recipients=[app.config['CONTACT_EMAIL']],
                body=f"""
Новое сообщение с сайта:

Имя: {name}
Email: {email}
Сообщение:
{comment}

Дата: {contact.created_at.strftime('%d.%m.%Y %H:%M:%S')}
                """.strip()
            )
            
            mail.send(msg)
            
            # Обновляем статус отправки
            contact.is_sent = True
            db.session.commit()
            
        except Exception as e:
            # Если email не отправился, все равно сохраняем в базе
            app.logger.error(f'Ошибка отправки email: {str(e)}')
        
        return jsonify({
            'message': 'Сообщение успешно отправлено!',
            'contact_id': contact.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Ошибка обработки контактной формы: {str(e)}')
        return jsonify({'error': 'Произошла ошибка при отправке сообщения'}), 500

@app.route("/api/contact", methods=["GET"])
def get_contacts():
    """Получение списка контактных сообщений (для администратора)"""
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return jsonify([contact.to_dict() for contact in contacts])