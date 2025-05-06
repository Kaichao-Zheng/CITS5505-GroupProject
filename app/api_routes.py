
from flask import Blueprint, request, jsonify, current_app, url_for
import os
from app.db_models import db, Product, Merchant, PriceData, Share, User
from datetime import datetime
from werkzeug.security import check_password_hash 
from flask import send_file
from app.utils import allowed_file 

api_bp = Blueprint('api', __name__)

@api_bp.route('/merchants', methods=['GET'])
def get_all_merchants():
    merchants = Merchant.query.all()
    return jsonify([{"id": m.id, "name": m.name} for m in merchants])

@api_bp.route('/product/exists/<int:product_id>', methods=['GET'])
def check_product_exists(product_id):
    exists = Product.query.get(product_id) is not None
    return jsonify({"exists": exists})

@api_bp.route('/upload', methods=['POST'])
def insert_data_bulk():
    data = request.get_json()
    for entry in data:
        new_price = PriceData(
            product_id=entry['product_id'],
            price=entry['price'],
            date=datetime.strptime(entry['date'], '%Y-%m-%d').date()
        )
        db.session.add(new_price)
    db.session.commit()
    return jsonify({"status": "success", "inserted": len(data)})

@api_bp.route('/products', methods=['GET'])
def retrieve_product_data():
    products = Product.query.all()
    return jsonify([{"product_id": p.id, "name": p.name, "image_url": p.image_url} for p in products])

@api_bp.route('/product/<int:product_id>/data', methods=['GET'])
def get_data_for_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    result = {}
    for merchant in product.merchants:
        merchant_name = merchant.name.lower()
        result[merchant_name] = []
        for price in product.prices:
            result[merchant_name].append({
                "date": price.date.isoformat(),
                "price": price.price
            })
    return jsonify(result)

@api_bp.route('/share', methods=['POST'])
def insert_share():
    data = request.get_json()
    new_share = Share(
        product_id=data['product_id'],
        sender_id=data['sender_id'],
        receiver_id=data['receiver_id']
    )
    db.session.add(new_share)
    db.session.commit()
    return jsonify({"status": "shared"})

@api_bp.route('/shared/<int:user_id>', methods=['GET'])
def get_shared_data(user_id):
    shares = Share.query.filter_by(receiver_id=user_id).all()
    result = []
    for share in shares:
        product = Product.query.get(share.product_id)
        sender = User.query.get(share.sender_id)
        result.append({
            "product_id": product.id,
            "name": product.name,
            "sender": sender.username
        })
    return jsonify(result)
    
@api_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    new_user = User(username=data['username'], password_hash=hash_password(data['password']))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "user created", "username": data['username']})
    
@api_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        # using JWT for authentication 
        token = generate_jwt(user)  # custom method to generate JWT token
        return jsonify({"status": "success", "token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@api_bp.route('/profile', methods=['GET'])
@jwt_required()  # using Flask-JWT-Extended for JWT authentication
def get_user_profile():
    current_user = get_jwt_identity()  # get current user from JWT token
    user = User.query.get(current_user['id'])
    return jsonify({"username": user.username, "email": user.email})
    
@api_bp.route('/product/<int:product_id>/price-trend', methods=['GET'])
def get_price_trend(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    # suppose we have a method to generate a price trend chart 
    price_data = PriceData.query.filter_by(product_id=product_id).all()
    dates = [price.date for price in price_data]
    prices = [price.price for price in price_data]
    img = generate_price_trend_chart(dates, prices)  # custom method to generate chart 
    return send_file(img, mimetype='image/png')  

@api_bp.route('/product/<int:product_id>/forecast', methods=['GET'])
def get_price_forecast(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    # using a custom method to predict price forecast 
    forecast_dates, forecast_prices = predict_price_forecast(product_id)  
    img = generate_forecast_chart(forecast_dates, forecast_prices) 
    return send_file(img, mimetype='image/png')

@api_bp.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # getting the URL for the uploaded image 
        image_url = url_for('static', filename='images/' + file.filename) 

        # save the image URL to the database 
        product_id = request.form['product_id']
        product = Product.query.get(product_id)
        if product:
            product.image_url = image_url 
            db.session.commit()

        return jsonify({"message": "File uploaded successfully", "image_url": image_url})
    return jsonify({"error": "Invalid file type"}), 400