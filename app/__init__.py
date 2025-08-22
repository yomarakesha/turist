from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_babel import Babel
from flask_cors import CORS
app = Flask(__name__)
app.config.from_object('config.Config')
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
app.config['BABEL_SUPPORTED_LOCALES'] = ['ru', 'en']
CORS(app,origins=["https://turist-front.vercel.app", "http://localhost:3000"],
     supports_credentials=True,
     resources={r"/api/*": {"origins": ["https://turist-front.vercel.app"]}})

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Инициализация Babel
babel = Babel(app)

from app import routes, models, auth, admin
