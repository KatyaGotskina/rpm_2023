from app import app
from .models import Products, Orders, db
from flask import jsonify, request


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