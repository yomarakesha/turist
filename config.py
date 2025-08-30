import os

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    
    # Настройки для отправки email
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'syyahathyzmatlary@gmail.com'  # Ваш Gmail
    MAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')  # Пароль приложения Gmail
    MAIL_DEFAULT_SENDER = 'syyahathyzmatlary@gmail.com'
    
    # Адрес для получения контактных сообщений
    CONTACT_EMAIL = 'syyahathyzmatlary@gmail.com'
