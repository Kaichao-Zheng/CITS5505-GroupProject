from flask import Flask, render_template
from app.db_models import db, login, User, Merchant, Upload, Product, PriceData, Share
from app.view_routes import view_bp
from app.api_routes import api_bp
from datetime import date
from sqlalchemy import inspect
import sqlalchemy as sa

# Refactored Flask App initialization to implement factory pattern
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    # init extensions
    db.init_app(app)
    login.init_app(app)
    
    # register blueprints
    app.register_blueprint(view_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # create tables if don't exist, especially when testing with an in-memory database
    with app.app_context():
        inspector = inspect(db.engine)
        if inspector.has_table('user'):
            print("Existing database detected.")
        else:
            db.create_all()
            print("New database created successfully.")
    
    # set upload path
    app.config['UPLOAD_FOLDER'] = 'static/img/products'    # need Chang's review here
    
    # automatically import objects when running `flask shell`
    @app.shell_context_processor
    def make_shell_context():
        return {'sa': sa, 'db': db, 'date': date, 'User': User, 'Merchant': Merchant, 'Upload': Upload, 'Product': Product, 'PriceData': PriceData, 'Share': Share}

    return app