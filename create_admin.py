from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin', email='admin@example.com', password='admin')
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created: admin / admin (plain password)")
    else:
        print("Admin already exists")
