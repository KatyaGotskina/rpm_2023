from flask import Flask, render_template, url_for, request, redirect, make_response, session,flash,get_flashed_messages
from werkzeug.security import generate_password_hash, check_password_hash
import os
from models import User, db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///katya.db'
app.secret_key = os.environ.get('secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['MAIL_SERVER'] = "smtp.gmail.com"
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('mail')
# app.config['MAIL_PASSWORD'] = os.environ.get('password')
# app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('mail')

#mail = Mail(app)

db.init_app(app)

# @app.route('/signin', methods=['POST', 'GET'])
# def signin():
#     """Авторизация"""
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         try:
#             user = User.query.filter(User.username == username).one()
#         except:
#             flash("Пользователь с указанным логином не найден")
#             return redirect("/signin")
#         if check_password_hash(user.password, password):

#             return render_template('index.html', username=user.name, )
#         else:
#             flash("Пароль не верен")
#             return redirect("/signin")
#     return render_template("sign_in.html")


# @app.route('/signup', methods=['POST', 'GET'])
# def signup():
#     """Регистрация"""

#     if request.method == 'POST':
#         name = request.form.get('name')
#         username = request.form.get('username')
#         password = request.form.get('password')
#         password = generate_password_hash(password, "sha256")
#         new_user = User(name=name, username=username, password=password)
#         try:
#             db.session.add(new_user)
#             db.session.commit()
#         except:
#             return "ДОбавление не удалось"
#         return redirect("/signin")
#     return render_template('signup.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)