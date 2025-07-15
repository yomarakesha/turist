from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin', email='admin@example.com', password=generate_password_hash('admin'))
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Админ успешно создан: admin / admin")
    else:
        print("⚠️ Админ уже существует")
