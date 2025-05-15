from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

# Refactored Flask App initialization to implement factory pattern
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    # init extensions
    db.init_app(app)
    login.init_app(app)
    
    # register blueprints
    from app.view_routes import view_bp
    from app.api_routes import api_bp
    app.register_blueprint(view_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # create tables if don't exist, especially when testing
    from sqlalchemy import inspect
    with app.app_context():
        inspector = inspect(db.engine)
        if inspector.has_table('user'):
            print("Existing database detected.")
        else:
            db.create_all()
            # print("New database created successfully.")     # Will pollute the testing output
    
    # set upload path
    app.config['UPLOAD_FOLDER'] = 'static/img/products'    # need Chang's review here
    
    # automatically import objects when running `flask shell`
    import sqlalchemy as sa
    from datetime import date
    from app.db_models import User, Merchant, Upload, Product, PriceData, Share
    @app.shell_context_processor
    def make_shell_context():
        return {'sa': sa, 'db': db, 'date': date, 'User': User, 'Merchant': Merchant, 'Upload': Upload, 'Product': Product, 'PriceData': PriceData, 'Share': Share}

    return app