from flask import Blueprint, jsonify
from app.models import Categories, Products

api_bp = Blueprint("api", __name__, template_folder="templates", static_folder="static")  # создаем объект Blueprint

@api_bp.route('/get_all_products')
def get_all_prods():
    res = [{
    'name' : product.name, 
    'category' : Categories.query.get(product.category_id).name,
    'weight' : product.weight,
    'description' : product.description,
    'composition' : product.composition, 
    'storage_conditions' : product.storage_conditions,
    'number' : product.number,
    'price' : product.price, 
    'status' : product.prod_status} for product in Products.query.all()]
    return jsonify(res)

@api_bp.route('/get_categories')
def get_categories():
    return jsonify({'category_names' : [cat.name for cat in Categories.query.all()]})