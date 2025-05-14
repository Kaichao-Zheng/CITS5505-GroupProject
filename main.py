# Defined in .flaskenv as the entry point for the Flask application

from app import create_app, db
from app.db_models import migrate
from instance.config import DeploymentConfig, TestConfig

'''Switch to normal database `instance/site.db`'''
flaskApp = create_app(DeploymentConfig)
migrate.init_app(flaskApp, db)

'''Switch to in-memory database for testing'''
# testApp = create_app(TestConfig)                  # flask-migrate is unnecessary when testing with in-memory database