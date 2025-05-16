import unittest
from app import create_app, db
from instance.config import TestConfig
from flask_login import current_user
from app.db_models import Product, Merchant, PriceData, Share, User

class UnitTests(unittest.TestCase):
    # Init test application and database
    def setUp(self):
        testApp = create_app(TestConfig)            # db.create_all() happens here
        self.app_context = testApp.app_context()
        self.app_context.push()
        
        # run an internal Flask test client, not real HTTP requests
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
        response = self.client.post('/register', headers={'Referer': '/'}, data=register_form, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(username='kai').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('passwd'))
        
    def test_register_fail(self):
        user = User(id=1, username='kai', user_type='merchant', email='kai@kai.com')
        user.set_password('passwd')
        db.session.add(user)
        db.session.commit()
        
        register_form = {
            # no csrf field in testing mode
            'username': 'kai',              # Existing
            'email': 'kai@kai.com',         # Existing
            'password': 'passwd',
            'confirm': 'password',          # Inconsistent
            'user_type': '',                # Empty
            'submit': 'Register'
        }
        with self.client as c:
            response = self.client.post('/register', headers={'Referer': '/'}, data=register_form, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_authenticated)
            self.assertIn(b'User type is required', response.data)
            self.assertIn(b'Username is already in use.', response.data)
            self.assertIn(b'Email is already in use.', response.data)
            self.assertIn(b'Passwords do not match.', response.data)
    
    def test_logout(self):
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
            self.assertIn(b'You have been logged out.', response.data)
        
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
            self.assertIn(b'Welcome back, kai !', response.data)
    
    def test_login_fail(self):
        user = User(id=1, username='kai', user_type='merchant', email='kai@kai.com')
        user.set_password('passwd')
        db.session.add(user)
        db.session.commit()
        
        # login fails with incorrect password
        login_form = {
            # no csrf field in testing mode
            'username': 'kai',
            'password': 'wrongpasswd',      # Wrong
            'submit': 'Log in'
        }
        # simulate Flask's request context
        with self.client as c:
            response = c.post('/', headers={'Referer': '/'}, data=login_form, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_authenticated)
            self.assertIn(b'Invalid username or password.', response.data)
        
        # login fails with empty fields
        login_form = {
            # no csrf field in testing mode
            'username': '',                 # Empty
            'password': '',                 # Empty
            'submit': 'Log in'
        }
        # simulate Flask's request context
        with self.client as c:
            response = c.post('/', headers={'Referer': '/'}, data=login_form, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_authenticated)
            self.assertIn(b'Username and password are required.', response.data)
    
    
    def test_api_product_exist(self):
        product = Product(id=1, image_url='1.avif', name="Arnott's Tim Tam Chocolate Biscuits Original | 200g")
        db.session.add(product)
        db.session.commit()
        
        response = self.client.get('/api/product/exists/1')
        self.assertEqual(response.status_code, 200)
        
        product = response.get_json()
        
        self.assertTrue(product['exists'])
        self.assertEqual(product['product']['id'], 1)
        self.assertEqual(product['product']['name'], "Arnott's Tim Tam Chocolate Biscuits Original | 200g")
    
    def test_api_products(self):
        product_1 = Product(id=1, image_url='1.avif', name="Arnott's Tim Tam Chocolate Biscuits Original | 200g")
        product_2 = Product(id=2, image_url='2.avif', name="Arnott's Tim Tam Chocolate Biscuits Double Coat | 200g")
        product_3 = Product(id=3, image_url='3.avif', name="Arnott's Tim Tam Chocolate Biscuits Dark Chocolate | 200g")
        db.session.add_all([product_1, product_2, product_3])
        db.session.commit()
        
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIsInstance(data, list)
        
        product = data[0]
        self.assertEqual(product['product_id'], 1)
        self.assertEqual(product['image_url'], "1.avif")
        self.assertEqual(product['name'], "Arnott's Tim Tam Chocolate Biscuits Original | 200g")
        
        product = data[1]
        self.assertEqual(product['product_id'], 2)
        self.assertEqual(product['image_url'], "2.avif")
        self.assertEqual(product['name'], "Arnott's Tim Tam Chocolate Biscuits Double Coat | 200g")
        
        product = data[2]
        self.assertEqual(product['product_id'], 3)
        self.assertEqual(product['image_url'], "3.avif")
        self.assertEqual(product['name'], "Arnott's Tim Tam Chocolate Biscuits Dark Chocolate | 200g")
        