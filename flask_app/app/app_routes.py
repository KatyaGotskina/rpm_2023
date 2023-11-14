from app import app
from .models import Products, Orders, db, User, OrdersToProducts
from flask import jsonify, request, session
from flask_login import current_user
from decimal import Decimal


@app.route('/get_active_products', methods=['GET'])
def get_products():
    products = Products.query.filter(Products.prod_status == 'active')
    products = [{
        'id': product.id,
        'name' : product.name, 
        'weight' : product.weight, 
        'price': product.price,
        'image_path' : product.image_path} for product in products]
    return jsonify(products), 200

@app.route('/get_archive_products', methods=['GET'])
def get_archive_products():
    products = Products.query.filter(Products.prod_status == 'inactive')
    products = [{
        'id': product.id,
        'name' : product.name, 
        'weight' : product.weight, 
        'price': product.price,
        'image_path' : product.image_path} for product in products]
    return jsonify(products), 200

@app.route('/make_archive', methods=['POST'])
def make_prod_archive():
    product_id = request.json.get('product_id')
    product = Products.query.get(product_id)
    product.prod_status = 'inactive'
    db.session.commit()
    return jsonify({'message': 'edited'}), 200

@app.route('/restore', methods=['POST'])
def make_prod_active():
    product_id = request.json.get('product_id')
    product = Products.query.get(product_id)
    product.prod_status = 'active'
    db.session.commit()
    return jsonify({'message': 'edited'}), 200

@app.route('/make_order')
def make_order():
    try:
        user = User.query.get(current_user.get_id())
        order = Orders(status='created', user_id=user.id)
        db.session.add(order)
        db.session.commit()
        for product_id in session["Cart"]["items"]:
            orderToProd = OrdersToProducts(product_id=product_id, order_id=order.id, number=session["Cart"]["items"][product_id]['qty'])
            db.session.add(orderToProd)
        session["Cart"] = {"items": {}, "total": Decimal(0)}
        db.session.commit()
        return jsonify({'message': 'created'}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'message': Exception}), 400

@app.route('/user_orders', methods=['GET'])
def get_user_orders():
    orders = Orders.query.filter(Orders.user_id == current_user.get_id())
    orders = [{
        'date' : order.date,
        'products': [product.image_path for product in order.products]
    } for order in orders]
    return jsonify(orders), 200