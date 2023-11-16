from flask import render_template, url_for, request, redirect, session, flash, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User, Categories, Products, db
from decimal import Decimal
from app import app, login_manager
from flask_mail import Message
from app import mail
from os import getenv
from dotenv import load_dotenv


load_dotenv()


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    """Авторизация"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            user = User.query.filter(User.username == username).one()
        except:
            flash("Пользователь с указанным логином не найден")
            return redirect("/signin")
        if check_password_hash(user.password, password):
            login_user(user)
            session["Cart"] = {"items": {}, "total": Decimal(0)}
            session.modified = True 
            if 'admin' in [role.name for role in user.roles]:
                return redirect('/admin')
            return render_template('homepage.html', cookie_flag=session.get('cookie_flag'))
        else:
            flash("Пароль не верен")
            return redirect("/signin")
    return render_template("registration/sign_in.html")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """Регистрация"""

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        last_name = request.form.get('last_name')
        surname = request.form.get('surname')
        first_name = request.form.get('first_name')
        email = request.form.get('email')
        password = generate_password_hash(password)
        new_user = User(username=username, password=password, first_name=first_name,
                        last_name=last_name, surname=surname, email=email)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception:
            return "Добавление не удалось"
        return redirect("/signin")
    return render_template('registration/signup.html')


@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html', cookie_flag=session.get('cookie_flag'))

@app.route('/menu')
def menu():
    context = {}
    context['data'] = {}
    categories = list(Categories.query.filter(Categories.supercategory_id == None))
    context['categories'] = categories
    for category in categories:
        products = Products.query.filter(Products.category_id == category.id).filter(Products.prod_status == 'active')
        if not [i for i in products]:
            continue
        products = [{
            'id' : product.id,
            'name' : product.name, 
            'weight' : product.weight, 
            'price': product.price,
            'image_path' : product.image_path} for product in products]
        context['data'][category.name] = products
    context['product_ids'] = [i for i in session["Cart"]["items"]]
    return render_template('menu.html', **context)

@app.route("/filter_category/<uuid:category_id>")
def filter_category(category_id):
    category = Categories.query.get(category_id)
    products = Products.query.filter(Products.category_id == category.id).filter(Products.prod_status == 'active')
    products = [{
        'name' : product.name, 
        'wieght' : product.weight, 
        'price': product.price,
        'image_path' : product.image_path} for product in products]
    return render_template('category_products.html', products=products, categories=Categories.query.all())

@app.route("/cart")
def cart():
    products = [Products.query.get(product_id) for product_id in session["Cart"]["items"]]
    products = [{
            'qty' : session['Cart']['items'][str(product.id)]['qty'],
            'id' : str(product.id),
            'name' : product.name, 
            'weight' : product.weight, 
            'price': product.price,
            'image_path' : product.image_path} for product in products]
    return render_template("cart.html", products=products, total=session['Cart']['total'])

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('product_id')
    if "Cart" in session:
        if not product_id in session["Cart"]["items"]:
            session["Cart"]["items"][product_id] = {"qty": 1}
            session['Cart']['total'] = Decimal(session['Cart']['total']) + Products.query.get(product_id).price
            session.modified = True
            return jsonify({'message': 'added'}), 200
        else:
            del session["Cart"]["items"][product_id]
            session['Cart']['total'] = Decimal(session['Cart']['total']) - Products.query.get(product_id).price
            session.modified = True
            return jsonify({'message': 'deleted'}), 204

@app.route('/del_prod_from_cart/<string:product_id>', methods=['DELETE'])
def delete_from_cart(product_id):
    if product_id in session["Cart"]["items"]:
        del session["Cart"]["items"][product_id]
        session.modified = True
        session['Cart']['total'] = Decimal(session['Cart']['total']) - Products.query.get(product_id).price
        return jsonify({'message': 'deleted'}), 204

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()

@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("menu"), 301)

@app.route('/profile')
def profile():
    user = User.query.get(current_user.get_id())
    full_name =(f'{user.last_name} {user.first_name} {user.surname}')
    return render_template('profile.html', email=user.email, full_name=full_name)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    print(app.config)
    if request.method == 'POST':
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        msg = Message("Клиент оставил обращение на сайте", recipients=[getenv('COMPANY_MAIL')])
        msg.body = f"Номер телефона клиента: {phone}, почта: {email} сообщение от клиента: {message}"
        mail.send(msg)
        return redirect('/homepage')
    return render_template('contact.html') 
