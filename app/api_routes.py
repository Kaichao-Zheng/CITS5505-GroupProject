import sqlalchemy as sa
from sqlalchemy import func
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app, url_for, send_file, redirect, flash, g
from flask_login import current_user, login_user, login_required, logout_user

from app.db_models import db, Product, Merchant, PriceData, Share, User
from app.forms import RegistrationForm
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.utils import allowed_file
import csv, os, io
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from collections import defaultdict

api_bp = Blueprint('api', __name__)

@api_bp.route('/merchants', methods=['GET'])
def get_all_merchants():
    merchants = Merchant.query.all()
    return jsonify([{"id": m.id, "name": m.name} for m in merchants])

@api_bp.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']

    merchant_id = request.form.get('merchant_id')
    if not merchant_id:
        return jsonify({"error": "Missing merchant_id"}), 400

    if file and file.filename.endswith('.csv'):
        try:
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csvreader = csv.DictReader(stream)

            for row in csvreader:
                product_id = row['product_id']
                price = float(row['price'])
                date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                new_price = PriceData(
                    product_id=product_id,
                    price=price,
                    date=date,
                    merchant_id=merchant_id
                )
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
    data         = request.get_json(force=True)
    print('DEBUG /share received >>>', data)
    product_id   = data.get('product_id')
    sender_id    = data.get('sender_id')
    receiver_ids = data.get('receiver_ids', [])
    emails       = data.get('emails', [])

    shares_to_add = []
    skipped_emails = []

    # 1. Add shares for each receiver ID
    for rid in receiver_ids:
        shares_to_add.append(
            Share(product_id=product_id,
                  sender_id=sender_id,
                  receiver_id=rid)
        )

    # 2. Lookup users by email; add share if user exists, otherwise skip
    for email in emails:
        user = User.query.filter_by(email=email).first()
        if user:
            shares_to_add.append(
                Share(product_id=product_id,
                      sender_id=sender_id,
                      receiver_id=user.id)
            )
        else:
            skipped_emails.append(email)

    # 3. Bulk insert into database
    try:
        if shares_to_add:
            db.session.add_all(shares_to_add)
            db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(message='Database error', detail=str(e)), 500

    # 4. Return result, including any skipped emails
    result = {'status': 'shared'}
    if skipped_emails:
        result['skipped_emails'] = skipped_emails

    return jsonify(result), 201


@api_bp.route('/share/notifications', methods=['GET'])
@login_required
def share_notifications():
    # Get all shares where the current user is the receiver and not yet notified
    shares = (
        Share.query
             .filter_by(receiver_id=current_user.id, notified=False)
             .order_by(Share.date_shared.asc())
             .all()
    )

    notifs = []
    for s in shares:
        notifs.append({
            "share_id":     s.id,
            "sender_name":  s.sender.username,
            "product_id":   s.product.id,
            "product_name": s.product.name,
            "date_shared":  s.date_shared.isoformat()
        })
        # mark as notified
        s.notified = True

    db.session.commit()
    return jsonify(notifs), 200

@api_bp.route('/price_trend/<int:product_id>', methods=['GET'])
def get_price_trend(product_id):
        #all price data for the product, including merchant info
    price_entries = db.session.query(PriceData, Merchant.name)\
        .join(Merchant, PriceData.merchant_id == Merchant.id)\
        .filter(PriceData.product_id == product_id)\
        .order_by(PriceData.date.asc())\
        .all()

    #organize data as per merchant name
    merchant_data = defaultdict(list)
    for price, merchant_name in price_entries:
        merchant_data[merchant_name].append({
            'date': price.date.strftime('%Y-%m-%d'),
            'value': price.price
        })

    # Final format
    result = [
        {'label': merchant_name, 'data': data}
        for merchant_name, data in merchant_data.items()
    ]
    return jsonify(result)

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

@api_bp.route('/product/exists/<int:product_id>', methods=['GET'])
def check_product_exists(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "exists": True,
            "product": {
                "id": product.id,
                "name": product.name
            }
        })
    else:
        return jsonify({"exists": False, "product": None})

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
@api_bp.route('/profile', methods=['GET'])
@jwt_required()  # using Flask-JWT-Extended for JWT authentication
def get_user_profile():
    current_user = get_jwt_identity()  # get current user from JWT token
    user = User.query.get(current_user['id'])
    return jsonify({"username": user.username, "email": user.email})
'''   