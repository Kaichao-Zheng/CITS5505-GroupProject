from flask import Flask, render_template
from app.db_models import db, migrate, login
from app.api_routes import api_bp

# Refactored Flask App initialization to implement factory pattern
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    # init extensions
    db.init_app(app)
    login.init_app(app)
    
    # register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # create tables if don't exist, especially when testing with an in-memory database
    with app.app_context():
        db.create_all()
        print("Database has been created successfully.")
    
    # set upload path
    app.config['UPLOAD_FOLDER'] = 'static/img/products'    # need Chang's review here
    
    # prevent circular import
    with app.app_context():
        from app.routes import init_routes
        init_routes(app)
    
    return app