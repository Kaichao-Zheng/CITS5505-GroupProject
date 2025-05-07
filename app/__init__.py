from flask import Flask, render_template, send_from_directory, g
from app.db_models import db, migrate, login
from app.api_routes import api_bp
import os
from .forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_pyfile('../instance/config.py')
db.init_app(app)
migrate.init_app(app, db)
login.init_app(app)
app.register_blueprint(api_bp, url_prefix='/api')
app.config['UPLOAD_FOLDER'] = 'static/images'

@app.before_request
def before_request():
    g.login_form = LoginForm()
    print("g.login_form initialized")
    g.register_form = RegistrationForm()
    print("g.login_form initialized")

@app.route('/')
def index():
    return render_template('index.html', login_form=g.login_form, register_form=g.register_form)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/product')
def product():
    return render_template('product.html')
