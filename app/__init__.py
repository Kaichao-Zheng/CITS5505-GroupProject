from flask import Flask
from app.db_models import db, migrate
from app.api_routes import api_bp

app = Flask(__name__)
app.config.from_pyfile('../instance/config.py')
db.init_app(app)            # Delayed database binding in db_models.py
migrate.init_app(app, db)   # Delayed migration bindging in db_models.py
app.register_blueprint(api_bp, url_prefix='/api')

from app import routes
