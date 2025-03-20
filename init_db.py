from app import app, db
from models import User
from datetime import datetime
from werkzeug.security import generate_password_hash

def init_admin():
    with app.app_context():
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            admin = User(
                email='admin@example.com',
                full_name='Admin User',
                qualification='Administrator',
                dob=datetime.strptime('2000-01-01', '%Y-%m-%d').date(),
                is_admin=True,
                password_hash=generate_password_hash('adminpass')
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    init_admin()