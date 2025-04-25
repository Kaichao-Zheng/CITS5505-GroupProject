from app import app
from app.db_models import db

with app.app_context():
    db.create_all()
    print("✅ Database has been created successfully.")
