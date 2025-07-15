from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_babel import Babel  # Добавляем
from flask_cors import CORS
app = Flask(__name__)
app.config.from_object('config.Config')
CORS(app) 
# Настройка языка по умолчанию
app.config['BABEL_DEFAULT_LOCALE'] = 'en'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Инициализация Babel
babel = Babel(app)

from app import routes, models, auth, admin
