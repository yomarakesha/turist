import os
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request
from app import app, db
from app.models import City, Hotel, Excursion, Attraction, ContactRequest, User
from flask_admin.form import Select2Widget
from flask_admin.form.upload import FileUploadField
from wtforms_sqlalchemy.fields import QuerySelectField

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
    form_columns = ['name', 'image']

class HotelModelView(MyModelView):
    form_extra_fields = {
        'city': QuerySelectField(
            'Город',
            query_factory=lambda: City.query.all(),
            get_label='name',
            allow_blank=False,
            widget=Select2Widget()
        ),
        'image': FileUploadField(
            'Изображение',
            base_path=file_path,
            relative_path='',
            allow_overwrite=False
        )
    }
    form_columns = ['name', 'price', 'description', 'image', 'rating', 'city']

    def on_model_change(self, form, model, is_created):
        model.city_id = form.city.data.id

class ExcursionModelView(MyModelView):
    form_extra_fields = {
        'image': FileUploadField(
            'Изображение',
            base_path=file_path,
            relative_path='',
            allow_overwrite=False
        )
    }
    form_columns = ['name', 'description', 'price', 'image']

class AttractionModelView(MyModelView):
    form_extra_fields = {
        'image': FileUploadField(
            'Изображение',
            base_path=file_path,
            relative_path='',
            allow_overwrite=False
        )
    }
    form_columns = ['name', 'price', 'image', 'city_id']

admin = Admin(app, name='Админ-панель', template_mode='bootstrap4', index_view=MyAdminIndexView())

admin.add_view(CityModelView(City, db.session))
admin.add_view(HotelModelView(Hotel, db.session))
admin.add_view(ExcursionModelView(Excursion, db.session))
admin.add_view(AttractionModelView(Attraction, db.session))
admin.add_view(MyModelView(ContactRequest, db.session))
admin.add_view(MyModelView(User, db.session))