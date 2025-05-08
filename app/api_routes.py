import sqlalchemy as sa
from sqlalchemy import func
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app, url_for, send_file, redirect, flash, g
from flask_login import current_user, login_user, login_required, logout_user

from app.db_models import db, Product, Merchant, PriceData, Share, User
from app.forms import RegistrationForm
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

from app.db_models import db, Product, Merchant, PriceData, Share, User
from app.utils import allowed_file
import csv, os

api_bp = Blueprint('api', __name__)


@api_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(request.referrer or url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, user_type=form.user_type.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # Success registration
        login_user(user)        # Auto login
        flash(f'Hi {form.username.data}, welcome to Price Trend !', 'success')
        return redirect(request.referrer)
    else:
        errors = []
        for field in form:
            for err in field.errors:
                errors.append(err)
        if errors:
            if len(errors) == 1:
                msg = f"{errors[0]} is required."
            else:
                msg = f"{', '.join(errors[:-1])} and {errors[-1]} are required."
            flash(f"Registration failed: {msg.capitalize()}", 'danger')
    return redirect(request.referrer)


@api_bp.route('/login', methods=['GET', 'POST'])            # Updated in routes.handle_login_post()
def login():
    form = g.login_form
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        # failed login
        if user is None or not user.check_password(form.password.data):
            flash('Login failed: Invalid username or password', 'danger')
            # return redirect(request.path)
            return redirect(request.referrer)
        # successful login
        login_user(user)
        flash(f'Welcome back, {form.username.data} !', 'success')
        # return redirect(request.path)
        return redirect(request.referrer)
    else:
        errors = []
        for field in form:
            for err in field.errors:
                errors.append(field.label.text)
        if errors:
            if len(errors) == 1:
                msg = f"{errors[0]} is required."
            else:
                msg = f"{', '.join(errors[:-1])} and {errors[-1]} are required."
            flash(f"Login failed: {msg.capitalize()}", 'danger')
    return None


@login_required
@api_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'warning')
    return redirect(request.referrer)


@api_bp.route('/merchants', methods=['GET'])
def get_all_merchants():
    merchants = Merchant.query.all()
    return jsonify([{"id": m.id, "name": m.name} for m in merchants])

@api_bp.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # parse the CSV file and insert data into the database 
        try:
            with open(file_path, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile) 
                for row in csvreader:
                    product_id = row['product_id']
                    price = float(row['price'])
                    date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                    new_price = PriceData(product_id=product_id, price=price, date=date)
                    db.session.add(new_price)
                
                db.session.commit()  

            return jsonify({"message": "File uploaded and data inserted successfully."}), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Invalid file type, only CSV files are allowed."}), 400

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

@api_bp.route('/products', methods=['GET'])
def retrieve_product_data():
    products = Product.query.all()
    return jsonify([{"product_id": p.id, "name": p.name, "image_url": p.image_url} for p in products])

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

#The profile page is not developed yet.
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

@api_bp.route('/api/price_trend/<int:product_id>', methods=['GET'])
def get_price_trend(product_id):
    # search for the product in the database 
    price_data = PriceData.query.filter_by(product_id=product_id).order_by(PriceData.date).all()
    
    if not price_data:
        return jsonify({"error": "No data found for the given product_id"}), 404

    labels = [entry.date.strftime('%Y-%m-%d') for entry in price_data] 
    prices = [entry.price for entry in price_data] 
    # building the dataset for the chart as rrequired by Chart.js
    datasets = [
        {
            "label": f"Price Trend for Product {product_id}",
            "data": [{"date": label, "value": price} for label, price in zip(labels, prices)],
            "borderColor": "green",  
            "fill": False,
            "tension": 0.2
        }
    ]
    return jsonify(datasets)

@api_bp.route('/forecast-data', methods=['GET'])
def forecast_data():
    data = [{"date": str(pd.date), "price": pd.price} for pd in PriceData.query.all()]
    return jsonify(data)
'''
@api_bp.route('/product/<int:product_id>/forecast', methods=['GET'])
def get_price_forecast(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    # using a custom method to predict price forecast 
    forecast_dates, forecast_prices = predict_price_forecast(product_id)  
    img = generate_forecast_chart(forecast_dates, forecast_prices) 
    return send_file(img, mimetype='image/png')'''

#Where to use this function?
@api_bp.route('/product/exists/<int:product_id>', methods=['GET'])
def check_product_exists(product_id):
    exists = Product.query.get(product_id) is not None
    return jsonify({"exists": exists})

#Where to use this function?
@api_bp.route('/product/<int:product_id>/data', methods=['GET'])
def get_data_for_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    result = {}
    for merchant in product.merchants:
        # get the latest price for the product from the merchant 
        latest_price = db.session.query(
            func.max(PriceData.date).label('latest_date'), 
            func.max(PriceData.price).label('latest_price') 
        ).filter(
            PriceData.product_id == product_id,
            PriceData.merchant_id == merchant.id 
        ).first()
        
        if latest_price and latest_price.latest_price is not None:
            result[merchant.name.lower()] = {
                "latest_price": latest_price.latest_price,
                "latest_price_date": latest_price.latest_date.isoformat()
            }
        else:
            result[merchant.name.lower()] = {
                "latest_price": None,
                "latest_price_date": None
            }
'''
@api_bp.route('/register', methods=['POST'])    # Has been implemented in routes.py
def register_user():
    data = request.get_json()
    new_user = User(username=data['username'], password_hash=hash_password(data['password']))
    db.session.add(new_user)                    # doesn't work because the user_type and email are not nullable in db_models.py
    db.session.commit()
    return jsonify({"status": "user created", "username": data['username']})
    
@api_bp.route('/login', methods=['POST'])       # Has been implemented in routes.py
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
'''   