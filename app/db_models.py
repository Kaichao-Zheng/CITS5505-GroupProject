
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()

# Association Table: Merchant <-> Product (Many-to-Many)
merchant_products = db.Table('merchant_products',
    db.Column('merchant_id', db.Integer, db.ForeignKey('merchant.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50))
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'), nullable=True)
    user_type = db.Column(db.String(20), nullable=False)  # 'Merchant' or 'Customer'
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    merchant = db.relationship('Merchant', backref='employees')
    uploads = db.relationship('Upload', backref='uploader', lazy=True)
    sent_shares = db.relationship('Share', foreign_keys='Share.sender_id', backref='sender', lazy=True)
    received_shares = db.relationship('Share', foreign_keys='Share.receiver_id', backref='receiver', lazy=True)

class Merchant(db.Model):
    __tablename__ = 'merchant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', secondary=merchant_products, backref='merchants')

class Upload(db.Model):
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    img_path = db.Column(db.String(100), default='img/mock-image.png')
    prices = db.relationship('PriceData', backref='product', lazy=True)
    image_url = db.Column(db.String(200), nullable=True)

class PriceData(db.Model):
    __tablename__ = 'price_data'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

class Share(db.Model):
    __tablename__ = 'share'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    date_shared = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product')
