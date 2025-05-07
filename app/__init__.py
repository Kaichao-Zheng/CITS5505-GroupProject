from flask import Flask, render_template
from app.db_models import db, migrate, login
from app.api_routes import api_bp

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_pyfile('../instance/config.py')
db.init_app(app)
migrate.init_app(app, db)
login.init_app(app)
app.register_blueprint(api_bp, url_prefix='/api')
app.config['UPLOAD_FOLDER'] = 'static/img/products'    # need Chang's review here

from app import routes