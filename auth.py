from flask import Blueprint, render_template, redirect, url_for, request, flash
from dbinit import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    if (not email) or (not password):
        flash("Неверная почта или пароль.")
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        flash("Неверная почта или пароль.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    return redirect(url_for("main.index"))

@auth.route("/signup")
def signup():
    return render_template("signup.html")

@auth.route("/signup", methods=["POST"])
def sigup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    if (not email) or (not name) or (not password):
        flash("Все поля должны быть заполнены.")
        return redirect(url_for("auth.signup"))

    user = User.query.filter_by(email=email).first()

    if user:
        flash("Такой адрес уже существует.")
        return redirect(url_for("auth.signup"))
    
    new_user = User(email=email, name=name, password=generate_password_hash(password, method="pbkdf2:sha256"))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))