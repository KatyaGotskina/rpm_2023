from flask import Flask, render_template, url_for, request, redirect, make_response, session, flash, get_flashed_messages, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import User, db, Categories, Products, Orders
from flask_mail import Mail
from decimal import Decimal
from flask_admin import Admin, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from api import api_bp


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

app.register_blueprint(api_bp, url_prefix="/api")  # регистрируем blueprint api в нашем приложении

class ProductsView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated # change to check role

    @expose("/")
    def products(self):
        return self.render('admin.html')

admin = Admin(app) 
admin.add_view(ProductsView(name='work_with_products'))
admin.add_view(ModelView(Products, db.session))   #How to protect?
admin.add_view(ModelView(Categories, db.session))

@app.route('/get_products', methods=['GET'])
def get_products():
    products = Products.query.all()
    products = [{
        'name' : product.name, 
        'weight' : product.weight, 
        'price': product.price,
        'image_path' : product.image_path} for product in products]
    return jsonify(products), 200

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
            return render_template('homepage.html')
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
    products = Products.query.filter(Products.category_id == category.id)
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
            print()
            print()
            print()
            print()
            print(session['Cart']['total'], type(session['Cart']['total']))
            print(type(Products.query.get(product_id).price))
            #session['Cart']['total'] += Products.query.get(product_id).price
            session.modified = True
            return jsonify({'message': 'added'}), 200
        else:
            del session["Cart"]["items"][product_id]
            #session['Cart']['total'] -= Products.query.get(product_id).price
            session.modified = True
            return jsonify({'message': 'deleted'}), 204

@app.route('/del_prod_from_cart/<string:product_id>', methods=['DELETE'])
def delete_from_cart(product_id):
    if product_id in session["Cart"]["items"]:
        print(session["Cart"]["items"])
        del session["Cart"]["items"][product_id]
        session.modified = True
        #session['Cart']['total'] += Products.query.get(product_id).price
        return jsonify({'message': 'deleted'}), 204

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()

@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("menu"), 301)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
