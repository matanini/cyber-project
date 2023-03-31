from flask import Flask, render_template, request
import hmac
import hashlib
import os
from secret import SECRET
from database_handler import get_all_clients, db_add_new_user, db_check_login


app = Flask(__name__)


@app.route("/")
def index(name=None):
    return render_template("login.html", name=name)


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    return render_template("forgot_password.html")


@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    return render_template("change_password.html")


@app.route("/intended-change-password", methods=["GET", "POST"])
def intended_change_password():
    return render_template("intended_change_password.html")


@app.route("/check-login", methods=["GET", "POST"])
def check_login():
    username = request.form["username"]
    password = request.form["password"]

    # Hash the password using HMAC
    hashed_password = hmac.new(SECRET, password.encode("utf-8"), hashlib.sha256).hexdigest()

    result = db_check_login(username, hashed_password)
    # If the result is not None, then the login was successful
    if result:
        return get_system_page()
    else:
        return render_template("failure.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    confirm_password = request.form["confirm-password"]
    email = request.form["email"]

    # confirm_password == password ?
    if confirm_password != password:
        pass
    
    # Hash the password using HMAC
    hashed_password = hmac.new(SECRET, password.encode("utf-8"), hashlib.sha256).hexdigest()

    db_add_new_user(username, hashed_password, email)

    return index()


@app.route("/system")
def get_system_page():
    clients = get_all_clients()
    return render_template("system.html", clients=clients)
