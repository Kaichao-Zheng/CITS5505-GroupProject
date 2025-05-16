import time
from datetime import datetime
import unittest
import multiprocessing
from app import create_app, db
from app.db_models import Product, Merchant, PriceData, Share, User
from instance.config import TestConfig
from flask_login import current_user
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

localHost = "http://127.0.0.1:5000"

class SystemTests(unittest.TestCase):
    # Init test application and database
    def setUp(self):
        testApp = create_app(TestConfig)            # db.create_all() happens here
        self.app_context = testApp.app_context()
        self.app_context.push()
        
        # run the in-memory test server in a separate thread
        self.server_thread = multiprocessing.Process(target=testApp.run)
        self.server_thread.start()
        
        # run a instance of the Chrome broswer
        # self.driver = webdriver.Chrome()      # Chrome always broken in Kai's machine
        self.driver = webdriver.Firefox()
        
        return super().setUp()
    
    # Clean up after each test
    def tearDown(self):
        self.server_thread.terminate()
        self.driver.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        return super().tearDown()
    
    def test_index_access(self):
        self.driver.get(localHost)
        self.assertEqual(self.driver.title, "Price Trend")
    
    def test_register_success(self):
        self.driver.get(localHost)
        time.sleep(1)
        
        register = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Register')
        self.driver.execute_script("arguments[0].click();", register)
        time.sleep(1)
        
        self.driver.find_element(By.NAME, "username").send_keys("kai")
        self.driver.find_element(By.NAME, "email").send_keys("kai@kai.com")
        self.driver.find_element(By.NAME, "password").send_keys("passwd")
        self.driver.find_element(By.NAME, "confirm").send_keys("passwd")
        dropdown = Select(self.driver.find_element(By.NAME, "user_type"))
        dropdown.select_by_value("merchant")
        time.sleep(2)
        register = self.driver.find_element(By.ID, "submit")
        register.click()
        
        toast = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#toastContainer .toast"))
        )
        time.sleep(1)
        self.assertIn("kai", toast.text)

    def test_register_fail(self):
        user = User(id=1, username='kai', user_type='merchant', email='kai@kai.com')
        user.set_password('passwd')
        db.session.add(user)
        db.session.commit()
        
        self.driver.get(localHost)
        time.sleep(1)
        
        register = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Register')
        self.driver.execute_script("arguments[0].click();", register)
        time.sleep(1)
        
        self.driver.find_element(By.NAME, "username").send_keys("kai")
        self.driver.find_element(By.NAME, "email").send_keys("kai@kai.com")
        self.driver.find_element(By.NAME, "password").send_keys("passwd")
        self.driver.find_element(By.NAME, "confirm").send_keys("wrongpasswd")
        time.sleep(2)
        submit = self.driver.find_element(By.ID, "submit")
        submit.click()
        
        time.sleep(2)
        toasts = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#toastContainer .toast"))
        )
        texts = "".join(t.text for t in toasts)
        time.sleep(1)
        self.assertIn("User type is required.", texts)
        self.assertIn("Username is already in use.", texts)
        self.assertIn("Email is already in use.", texts)
        self.assertIn("Passwords do not match.", texts)
        
    def test_login_blank(self):
        self.driver.get(localHost)
        
        login = self.driver.find_element(By.LINK_TEXT, "Login")
        login.click()
        
        login_modal = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "loginModal"))
        )
        submit = login_modal.find_element(By.ID, "submit")
        submit.click()
        
        toast = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#toastContainer .toast"))
        )
        time.sleep(1)
        text = toast.text.lower()
        self.assertIn("username", text)
        self.assertIn("password", text)
        
    def test_login_fail(self):
        user = User(id=1, username='kai', user_type='merchant', email='kai@kai.com')
        user.set_password('passwd')
        db.session.add(user)
        db.session.commit()
        
        self.driver.get(localHost)
        
        login = self.driver.find_element(By.LINK_TEXT, "Login")
        login.click()
        
        login_modal = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "loginModal"))
        )
        
        login_modal.find_element(By.ID, "username").send_keys("kai")
        login_modal.find_element(By.ID, "password").send_keys("wrongpasswd")
        submit = login_modal.find_element(By.ID, "submit")
        time.sleep(1)
        submit.click()
        
        toast = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#toastContainer .toast"))
        )
        time.sleep(1)
        self.assertIn("Invalid username or password.", toast.text)
    
    def test_login_success(self):
        user = User(id=1, username='kai', user_type='merchant', email='kai@kai.com')
        user.set_password('passwd')
        db.session.add(user)
        db.session.commit()
        
        self.driver.get(localHost)
        
        login = self.driver.find_element(By.LINK_TEXT, "Login")
        login.click()
        
        login_modal = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "loginModal"))
        )
        
        login_modal.find_element(By.ID, "username").send_keys("kai")
        login_modal.find_element(By.ID, "password").send_keys("passwd")
        submit = login_modal.find_element(By.ID, "submit")
        time.sleep(2)
        submit.click()
        
        toast = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#toastContainer .toast"))
        )
        time.sleep(1)
        self.assertIn("kai", toast.text)
    
    def test_share_received(self):
        user1 = User(id=1, username='kai', user_type='merchant', email='kai@kai.com')
        user1.set_password('passwd')
        user2 = User(id=2, username='chang', user_type='merchant', email='chang@chang.com')
        user2.set_password('passwd')
        share = Share(id=1, sender_id=1, receiver_id=2, product_id=1, date_shared=datetime.utcnow())
        product = Product(id=1, image_url="1.avif", name="Arnott's Tim Tam Chocolate Biscuits Original | 200g")
        db.session.add_all([user1, user2, share, product])
        db.session.commit()
        
        self.driver.get(localHost)
        
        login = self.driver.find_element(By.LINK_TEXT, "Login")
        login.click()
        
        login_modal = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "loginModal"))
        )
        
        login_modal.find_element(By.ID, "username").send_keys("chang")
        login_modal.find_element(By.ID, "password").send_keys("passwd")
        submit = login_modal.find_element(By.ID, "submit")
        time.sleep(2)
        submit.click()
        
        toast = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#toastContainer .toast"))
        )
        time.sleep(5)
        toast = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#toastContainer .toast"))
        )
        time.sleep(1)
        self.assertIn("You have a new share from", toast.text)
