from flask import Flask, render_template, request, url_for
import hmac
import hashlib
import os
from secret import SECRET

app = Flask(__name__)

@app.route("/")
def index(name = None):
    return render_template('login.html', name=name)

@app.route("/forgot-password", methods=['GET','POST'])
def forgot_password():
    return render_template('forgot_password.html')

@app.route("/change-password", methods=['GET','POST'])
def change_password():
    return render_template('change_password.html')

@app.route("/intended-change-password", methods=['GET','POST'])
def intended_change_password():
    return render_template('intended_change_password.html')

@app.route("/check-login", methods=['GET','POST'])
def check_login():
    username = request.form['username']
    password = request.form['password']
    
    # Generate a random salt
    
    
    # Hash the password using HMAC
    hashed_password = hmac.new(SECRET, password.encode('utf-8'), hashlib.sha256).hexdigest()
    
    # Connect to the database
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    
    # Check if the username and hashed password match
    cursor.execute("SELECT * FROM `users` WHERE user_name=? AND user_password=?", (username, hashed_password))
    result = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    # If the result is not None, then the login was successful
    if result:
        return get_system_page()
    else:
        return render_template('failure.html')


@app.route("/register", methods=['GET','POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm-password']
    email = request.form['email']
    
    # confirm_password == password ?

    # Hash the password using HMAC
    hashed_password = hmac.new(SECRET, password.encode('utf-8'), hashlib.sha256).hexdigest()
    
    # Connect to the database
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    
    # Insert the new user into the database
    cursor.execute("INSERT INTO `users` (user_name, user_password, user_email) VALUES (?, ?, ?)", (username, hashed_password, email))
    conn.commit()
    
    # Close the connection
    conn.close()
    
    return index()


import sqlite3
 

HOST_NAME = "localhost"
HOST_PORT = 80
DBFILE = "users.db"


# (B) HELPER - GET ALL USERS FROM DATABASE
def getusers():
  conn = sqlite3.connect(DBFILE)
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM `users`")
  results = cursor.fetchall()
  conn.close()
  return results


@app.route("/system")
def get_system_page():
  # (C1) GET ALL USERS
  users = getusers()
  # print(users)
  return render_template("system.html", usr=users)