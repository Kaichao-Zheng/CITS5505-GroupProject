import unittest
from app import create_app, db
from app.forms import LoginForm, RegistrationForm
from instance.config import TestConfig
from flask import g
from flask_login import current_user
from app.db_models import Product, Merchant, PriceData, Share, User
import sqlalchemy as sa

class UnitTests(unittest.TestCase):
    # Init test application and database
    def setUp(self):
        testApp = create_app(TestConfig)            # db.create_all() happens here
        self.app_context = testApp.app_context()
        self.app_context.push()
        self.client = testApp.test_client()
        return super().setUp()

    # Clean up after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        return super().tearDown()
    
    def test_index_access(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_register_success(self):
        register_form = {
            # no csrf field in testing mode
            'username': 'kai',
            'email': 'kai@kai.com',
            'password': 'passwd',
            'confirm': 'passwd',
            'user_type': 'merchant',
            'submit': 'Register'
        }
        response = self.client.post('/register', headers={'Referer': '/'}, data=register_form)
        user = User.query.filter_by(username='kai').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('passwd'))
    
    def test_login_success(self):
        user = User(id=1, username='kai', user_type='merchant', email='kai@kai.com')
        user.set_password('passwd')
        db.session.add(user)
        db.session.commit()
        
        login_form = {
            # no csrf field in testing mode
            'username': 'kai',
            'password': 'passwd',
            'submit': 'Log in'
        }
        # simulate Flask's request context
        with self.client as c:
            response = c.post('/', headers={'Referer': '/'}, data=login_form, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(current_user.is_authenticated)
    
    def test_logout_success(self):
        user = User(id=1, username='kai', user_type='merchant', email='kai@kai.com')
        user.set_password('passwd')
        db.session.add(user)
        db.session.commit()
        
        login_form = {
            # no csrf field in testing mode
            'username': 'kai',
            'password': 'passwd',
            'submit': 'Log in'
        }
        
        # simulate Flask's request context
        with self.client as c:
            response = c.post('/', data=login_form, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(current_user.is_authenticated)
            
            response = c.get('/logout', headers={'Referer': '/'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_authenticated)
        
    
    # Add more unit tests here