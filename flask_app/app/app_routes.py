from app import app
from .models import Products, Orders, db, OrdersToProducts
from flask import jsonify, request, session, make_response, render_template
from flask_login import current_user
from decimal import Decimal
from .base_func import get_current_user, get_prod_by_id


@app.route('/get_active_products', methods=['GET'])
def get_products():
    products = Products.query.filter(Products.prod_status == 'active')
    products = [{
        'id': product.id,
        'name': product.name,
        'number': product.number,
        'weight': product.weight,
        'price': product.price,
        'image_path': product.image_path} for product in products]
    return jsonify(products), 200


@app.route('/get_archive_products', methods=['GET'])
def get_archive_products():
    products = Products.query.filter(Products.prod_status == 'inactive')
    products = [{
        'id': product.id,
        'name': product.name,
        'weight': product.weight,
        'number': product.number,
        'price': product.price,
        'image_path': product.image_path} for product in products]
    return jsonify(products), 200


@app.route('/make_archive', methods=['POST'])
def make_prod_archive():
    product_id = request.json.get('product_id')
    product = get_prod_by_id(product_id)
    product.prod_status = 'inactive'
    db.session.commit()
    return jsonify({'message': 'edited'}), 200


@app.route('/restore', methods=['POST'])
def make_prod_active():
    product_id = request.json.get('product_id')
    product = get_prod_by_id(product_id)
    product.prod_status = 'active'
    db.session.commit()
    return jsonify({'message': 'edited'}), 200


@app.route('/make_order')
def make_order():
    try:
        user = get_current_user()
        order = Orders(status='created', user_id=user.id)
        db.session.add(order)
        db.session.commit()
        for product_id in session["Cart"]["items"]:
            product = get_prod_by_id(product_id)
            product.number -= session["Cart"]["items"][product_id]['qty']
            db.session.commit()
            if product.number == 0:
                product.prod_status = 'inactive'
            orderToProd = OrdersToProducts(
                product_id=product_id, order_id=order.id, number=session["Cart"]["items"][product_id]['qty'])
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
        'date': order.date,
        'products': [product.image_path for product in order.products]
    } for order in orders]
    return jsonify(orders), 200


@app.route('/add_cookies')
def cookies():
    user = get_current_user()
    res = make_response(render_template('homepage.html', cookie_flag=True))
    res.set_cookie("name", user.first_name, max_age=60 * 60 * 24)
    session['cookie_flag'] = True
    return res


@app.route('/show_cookies')
def show():
    if request.cookies.get("name"):  # проверяем есть ли кука name
        return "Hello " + request.cookies.get("name")
    else:
        return "Кук нет"


@app.route('/delete_cookies')
def delete_cookies():
    res = make_response(render_template('homepage.html', cookie_flag=False))
    res.set_cookie("name", "noname", max_age=0)
    del session['cookie_flag']
    return res


@app.route('/minus_qty/<string:product_id>')
def minus_product_qty(product_id):
    product = get_prod_by_id(product_id)
    session['Cart']['items'][str(product_id)]['qty'] -= 1
    session.modified = True
    num = session['Cart']['items'][str(product_id)]['qty']
    session['Cart']['total'] = Decimal(session['Cart']['total']) - product.price
    return ({'massege': 'not found'}, 204) if num == 0 else ({'num': num, 'total': session['Cart']['total']}, 200)


@app.route('/plus_qty/<string:product_id>')
def plus_product_qty(product_id):
    product = get_prod_by_id(product_id)
    session['Cart']['total'] = Decimal(session['Cart']['total']) + product.price
    session['Cart']['items'][str(product_id)]['qty'] += 1
    session.modified = True
    num = session['Cart']['items'][str(product_id)]['qty']
    result = {'num': num, 'total': session['Cart']['total']}
    return (result, 202) if num == product.number else (result, 200)


@app.route('/check_quatity/<uuid:product_id>')
def check_quatity(product_id):
    product = get_prod_by_id(product_id)
    return ({'massege': 'full'}, 202) if session['Cart']['items'][str(product_id)]['qty'] == product.number else ({'massege': 'good'}, 200)


@app.route('/del_prod_from_cart/<string:product_id>', methods=['DELETE'])
def delete_from_cart(product_id):
    if product_id in session["Cart"]["items"]:
        session['Cart']['total'] = Decimal(session['Cart']['total']) - get_prod_by_id(
            product_id).price * session["Cart"]["items"][product_id]['qty']
        del session["Cart"]["items"][product_id]
        session.modified = True
        return {'massege': 'deleted'}, 204


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('product_id')
    if "Cart" in session:
        if not product_id in session["Cart"]["items"]:
            session["Cart"]["items"][product_id] = {"qty": 1}
            session['Cart']['total'] = Decimal(
                session['Cart']['total']) + get_prod_by_id(product_id).price
            session.modified = True
            return jsonify({'message': 'added'}), 200
        else:
            del session["Cart"]["items"][product_id]
            session['Cart']['total'] = Decimal(
                session['Cart']['total']) - get_prod_by_id(product_id).price
            session.modified = True
            return jsonify({'message': 'deleted'}), 204


@app.route('/get_total')
def get_total():
    return {'total': session['Cart']['total']}, 200


@app.route('/product_availability/<uuid:product_id>')
def check_product_availability(product_id):
    product = get_prod_by_id(product_id)
    return ({'message': 'not found'}, 204) if product.number == 0 else ({'massege': 'good'}, 200)


@app.route('/admin_add_number/<uuid:product_id>', methods=['POST'])
def admin_add_number(product_id):
    product = get_prod_by_id(product_id)
    number = request.json.get('number')
    if not number.isdigit() or (number.startswith('0') and len(number) > 1) or int(number) < 0:
        return {'massege': 'bad'}, 400
    product.number = number
    db.session.commit()
    return {'massege': 'good'}, 200


@app.route('/is_admin')
def is_admin():
    return ({'massege': 'good'}, 200) if 'admin' in [role.name for role in get_current_user().roles] else ({'massege': 'bad'}, 409)

@app.route('/get_prod_num/<uuid:product_id>')
def get_prod_num(product_id):
    return {'number' : session['Cart']['items'][str(product_id)]['qty']}, 200
