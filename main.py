# Defined in .flaskenv as the entry point for the Flask application

from app import create_app, db, migrate
from instance.config import DeploymentConfig, TestConfig

'''Switch to run the real database `instance/site.db`'''
flaskApp = create_app(DeploymentConfig)
migrate.init_app(flaskApp, db)

'''Switch to run a mock database in-memory for testing'''
# testApp = create_app(TestConfig)                  # flask-migrate is unnecessary when testing with in-memory database