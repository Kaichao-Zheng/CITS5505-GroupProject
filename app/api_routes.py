
from flask import Blueprint, request, jsonify
from app.db_models import db, Product, Merchant, PriceData, Share, User
from datetime import datetime

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
    return jsonify([{"product_id": p.id, "name": p.name} for p in products])

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
