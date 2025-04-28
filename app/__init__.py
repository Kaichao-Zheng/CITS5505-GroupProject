from flask import Flask
from app.db_models import db
from app.api_routes import api_bp

app = Flask(__name__)
app.config.from_pyfile('../instance/config.py')
db.init_app(app)
app.register_blueprint(api_bp, url_prefix='/api')

from app import routes
