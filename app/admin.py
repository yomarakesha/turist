import os
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request
from app import app, db
from app.models import City, Hotel, Excursion, User, Attraction, Banner
from flask_admin.form import Select2Widget
from flask_admin.form.upload import FileUploadField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import SelectField 
from wtforms_sqlalchemy.fields import QuerySelectMultipleField  # добавь наверху

file_path = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class CityModelView(MyModelView):
    form_extra_fields = {
        'image': FileUploadField(
            'Изображение',
            base_path=file_path,
            relative_path='',
            allow_overwrite=False
        )
    }
    form_columns = ['name_ru', 'name_en', 'image']
    column_list = ['name_ru', 'name_en', 'image']
from flask_admin.form import FileUploadField
from flask_admin.contrib.sqla.fields import QuerySelectField
from wtforms.validators import DataRequired
from flask_admin.form.upload import ImageUploadField
from wtforms import validators

from flask_admin.form import FileUploadField
from wtforms_sqlalchemy.fields import QuerySelectField

class HotelModelView(MyModelView):
    form_extra_fields = {
        'city': QuerySelectField(
            'Город',
            query_factory=lambda: City.query.all(),
            get_label='name_ru',
            allow_blank=False
        ),
        'image': FileUploadField(
            'Изображение',
            base_path=file_path,
            allow_overwrite=False
        )
    }

    form_columns = ['name_ru', 'name_en', 'price', 'description_ru', 'description_en', 'image', 'rating', 'city', 'excursions']
    column_list = ['name_ru', 'name_en', 'price', 'rating', 'city']

    column_formatters = {
        'city': lambda v, c, m, p: m.city.name_ru if m.city else ''
    }

    def on_model_change(self, form, model, is_created):
        model.city_id = form.city.data.id

class ExcursionModelView(MyModelView):
    form_extra_fields = {
        'image': FileUploadField('Изображение', base_path=file_path),
        'type': SelectField(
            'Типы экскурсий',
            choices=[('historical', 'Историческая'), ('city', 'Городская')],
            validators=[DataRequired()]
        ),

        'city': QuerySelectField(
            'Город',
            query_factory=lambda: City.query.all(),
            get_label='name_ru',
            allow_blank=False,
            widget=Select2Widget()
        ),
        'attractions': QuerySelectMultipleField(
            'Достопримечательности',
            query_factory=lambda: Attraction.query.all(),
            get_label='name_ru',
            widget=Select2Widget()
        )
    }
    form_columns = ['name_ru', 'name_en', 'description_ru', 'description_en', 'price', 'image', 'type', 'duration_hours', 'city', 'attractions']
    column_list = ['name_ru', 'name_en', 'type', 'price', 'city']

    def on_model_change(self, form, model, is_created):
        model.city_id = form.city.data.id
        model.attractions = form.attractions.data or []

class AttractionModelView(MyModelView):
    form_extra_fields = {
        'image': FileUploadField('Изображение', base_path=file_path),
        'type': SelectField(
            'Тип',
            choices=[('historical', 'Историческая'), ('city', 'Городская')],
            validators=[DataRequired()]
        ),

        'city': QuerySelectField(
            'Город',
            query_factory=lambda: City.query.all(),
            get_label='name_ru',
            allow_blank=False,
            widget=Select2Widget()
        )
    }
    form_columns = ['name_ru', 'name_en', 'description_ru', 'description_en', 'type', 'image', 'city']
    column_list = ['name_ru', 'name_en', 'type', 'city']

    def on_model_change(self, form, model, is_created):
        model.city_id = form.city.data.id


class BannerModelView(MyModelView):
    form_extra_fields = {
        'image': FileUploadField('Изображение', base_path=file_path)
    }
    form_columns = ['image']

admin = Admin(app, name='Админ-панель', template_mode='bootstrap4', index_view=MyAdminIndexView())

admin.add_view(CityModelView(City, db.session))
admin.add_view(HotelModelView(Hotel, db.session))
admin.add_view(ExcursionModelView(Excursion, db.session))
# admin.add_view(AttractionModelView(Attraction, db.session))
admin.add_view(AttractionModelView(Attraction, db.session))
admin.add_view(BannerModelView(Banner, db.session))

admin.add_view(MyModelView(User, db.session))