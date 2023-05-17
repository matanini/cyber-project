from app.config.config import DBFILE

from datetime import datetime, timedelta
import sqlite3
import secrets
import asyncio

def create_database():
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS `users` (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        user_name TEXT NOT NULL UNIQUE,
        user_password TEXT NOT NULL, 
        user_email TEXT NOT NULL UNIQUE,
        password_history TEXT
        )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS `clients` (
        client_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        client_name TEXT, 
        client_email TEXT NOT NULL UNIQUE, 
        client_phone TEXT NOT NULL, 
        client_city TEXT
        )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS `tokens` (
        user_email TEXT PRIMARY KEY, 
        token TEXT NOT NULL UNIQUE, 
        expiry TEXT NOT NULL
        )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS `app` (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        key TEXT NOT NULL UNIQUE, 
        value TEXT NOT NULL
        )""")
    conn.commit()
    conn.close()

def init_app():
    create_database()
    print("Checking salt")
    if len(get_app_data("salt"))==0:
        print("Creating salt")
        set_app_data("salt", secrets.token_hex(32))
    

def set_app_data(key, value):
    q="INSERT INTO `app` (key, value) VALUES (?,?)"
    exec_insert_query(q, key, value)

def get_app_data(key):
    q="SELECT value FROM `app` WHERE key=?"
    value = exec_select_query(q, key)
    return value

def exec_select_query(q,*params):

    # Connect to the database
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    if len(params)>0:
       cursor.execute(q,params)
    else:
       cursor.execute(q)
    result = cursor.fetchall()
    # Close the connection
    conn.close()
    return result

def exec_insert_query(q,*params):

    # Connect to the database
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()

    cursor.execute(q,params)
    conn.commit()
    
    # Close the connection
    conn.close()


def get_all_clients():
  q="SELECT * FROM `clients`"
  results = exec_select_query(q)
  return results

def get_all_users():
    q="SELECT * FROM `users`"
    results = exec_select_query(q)
    return results


def get_client_by_id(client_id:int):
    q="SELECT * FROM `clients` WHERE client_id=?"
    return exec_select_query(q, client_id)

def get_client_by_email(email):
    q="SELECT * FROM `clients` WHERE client_email=?"
    return exec_select_query(q, email)

def get_user_by_email(email):
    q="SELECT * FROM `users` WHERE user_email=?"
    return exec_select_query(q, email)

def get_user_by_user_id(user_id:int):
    q="SELECT * FROM `users` WHERE user_id=?"
    return exec_select_query(q, user_id)

def get_user_by_username(username):
    q="SELECT * FROM `users` WHERE user_name=?"
    return exec_select_query(q, username)

def create_new_user(username, hashed_password, email):
    q="INSERT INTO `users` (user_name, user_password, user_email, password_history) VALUES (?, ?, ?, ?)"
    exec_insert_query(q, username, hashed_password, email, "")

def create_new_client(name, email, phone, city):
    q="INSERT INTO `clients` (client_name, client_email, client_phone, client_city) VALUES (?, ?, ?, ?)"
    exec_insert_query(q, name, email, phone, city)

def update_user(user_id, username, password, email):
    q="UPDATE `users` SET user_name=?, user_password=?, user_email=? WHERE user_id=?"
    exec_insert_query(q, username, password, email, user_id)
    return get_user_by_user_id(user_id)

async def change_password(user_id, password, old_passwords):
    # make sure we don't have more than 10 passwords in the history
    if len(old_passwords)>10:
        old_passwords = old_passwords[:10]

    q="UPDATE `users` SET user_password=?, password_history=? WHERE user_id=?"
    exec_insert_query(q, password, ",".join(old_passwords), user_id)
    return get_user_by_user_id(user_id)

def check_old_passwords(password, old_passwords):
    if len(old_passwords)==0:
        return True
    return password not in old_passwords

async def save_new_token(email, token):
    q="INSERT INTO `tokens` (user_email, token, expiry) VALUES (?, ?, ?)"
    exec_insert_query(q, email, token, datetime.now()+timedelta(minutes=10))
    # start a background task to remove the token after 10 minutes
    # asyncio.create_task(remove_token(token))

async def get_token_by_mail(email):
    q="SELECT token FROM `tokens` WHERE user_email=?"
    return exec_select_query(q, email)

async def get_token_by_token(token):    
    q="SELECT token FROM `tokens` WHERE token=?"
    return exec_select_query(q, token)

async def remove_token(token):
    q="DELETE FROM `tokens` WHERE token=?"
    exec_insert_query(q, token)