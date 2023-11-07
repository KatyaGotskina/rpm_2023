from flask import Flask, render_template, url_for, request, redirect, make_response, session, flash, get_flashed_messages
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import LoginManager, login_user, login_required, logout_user
from models import User, db, Categories, Products, Orders
from flask_mail import Mail
from sqlalchemy import text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://katya:kbwtq12345F@localhost:5432/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('mail')
# app.config['MAIL_PASSWORD'] = os.environ.get('password')
# app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('mail')
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)

db.init_app(app)


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
            return render_template('homepage.html')
        else:
            flash("Пароль не верен")
            return redirect("/signin")
    return render_template("registration/sign_in.html")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """Регистрация"""

    if request.method == 'POST':
        name = request.form.get('name')
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
        except Exception:  # as err:
            # print(err)
            return "Добавление не удалось"
        return redirect("/signin")
    return render_template('registration/signup.html')


@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/menu')
def menu():
    context = {}
    context['data'] = {}
    categories = list(Categories.query.filter(Categories.supercategory_id == None))
    context['categories'] = categories
    for category in categories:
        products = Products.query.filter(Products.category_id == category.id)
        products = [{
            'name' : product.name, 
            'weight' : product.weight, 
            'price': product.price,
            'image_path' : product.image_path} for product in products]
        context['data'][category.name] = products
    return render_template('menu.html', **context)

@app.route("/filter_category/<uuid:category_id>")
def filter_category(category_id):
    category = Categories.query.get(category_id)
    products = Products.query.filter(Products.category_id == category.id)
    products = [{
        'name' : product.name, 
        'wieght' : product.weight, 
        'price': product.price,
        'image_path' : product.image_path} for product in products]
    return render_template('category_products.html', products=products, categories=Categories.query.all())

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()

@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect("menu.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
