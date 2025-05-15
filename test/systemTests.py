import random
import time
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

    # Add more unit tests here