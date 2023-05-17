#  Create the database
#  Create tables - Users, Clients
#  add user to Users table
#  check password
import re
import sqlite3
from config import DBFILE, PASSWORD_POLICY
import hashlib
import random
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

def create_database():
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `users` (user_id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT NOT NULL, user_password TEXT NOT NULL, user_email TEXT NOT NULL, password_history TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `clients` (client_id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, client_email TEXT, client_phone TEXT, client_city TEXT)")
    conn.commit()
    conn.close()

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

def db_add_new_user(username, hashed_password, email):
    q="INSERT INTO `users` (user_name, user_password, user_email) VALUES (?, ?, ?)"
    exec_insert_query(q, username, hashed_password, email)

def db_check_login(username, password):
    q="SELECT * FROM `users` WHERE user_name=? AND user_password=?"
    return exec_select_query(q, username, password)

# (B) HELPER - GET ALL USERS FROM DATABASE
def get_all_clients():
  q="SELECT * FROM `clients`"
  results = exec_select_query(q)
  return results

def check_valid_email(email):
    format = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}'
    if(re.search(format,email)):
        return True
    else:
        return False
    
def get_user_by_email(email):
    q="SELECT * FROM `users` WHERE user_email=?"
    return exec_select_query(q, email)

def get_user_by_user_id(user_id:int):
    q="SELECT * FROM `users` WHERE user_id=?"
    return exec_select_query(q, user_id)

def get_user_by_username(username):
    q="SELECT * FROM `users` WHERE user_name=?"
    return exec_select_query(q, username)

def password_check(password):
     
    val = True
     
    if len(password) < PASSWORD_POLICY['MIN_LENGTH']:
        print(f'length should be at least {PASSWORD_POLICY["MIN_LENGTH"]}')
        val = False
         
    if len(password) > PASSWORD_POLICY['MAX_LENGTH']:
        print(f'length should be not be greater than {PASSWORD_POLICY["MAX_LENGTH"]}')
        val = False

    dig_count = 0
    up_count = 0
    low_count = 0
    spec_count = 0
    for char in password:
        if char.isdigit():
            dig_count += 1
        elif char.isupper():
            up_count += 1
        elif char.islower():
            low_count += 1
        elif char in PASSWORD_POLICY['SPECIAL_CHARACTERS']:
            spec_count += 1
        else:
            val = False
            print(f'Cant use {char} in password')
        

    if dig_count < PASSWORD_POLICY['MIN_DIGITS']:
        print(f'Password should have at least {PASSWORD_POLICY["MIN_SPECIAL_CHARACTERS"]} numeral')
        val = False
    
    if up_count < PASSWORD_POLICY['MIN_UPPERCASE_CHARACTERS']:
        print(f'Password should have at least {PASSWORD_POLICY["MIN_UPPERCASE_CHARACTERS"]} uppercase letter')
        val = False
    
    if low_count < PASSWORD_POLICY['MIN_LOWERCASE_CHARACTERS']:
        print(f'Password should have at least {PASSWORD_POLICY["MIN_LOWERCASE_CHARACTERS"]} lowercase letter')
        val = False
    
    if spec_count < PASSWORD_POLICY['MIN_SPECIAL_CHARACTERS']:
        print(f'Password should have at least {PASSWORD_POLICY["MIN_DIGITS"]} special symbols')
        val = False

    return val

def create_token():
    r = str(random.randint(0,1_000_000_000)).encode()
    # return a sha1 generated token
    return hashlib.sha1(r).hexdigest()

async def send_reset_email(reset_password_data):
    token = reset_password_data['token']
    email = reset_password_data['email']

    body = f"""
    <html>
        <body>
            <p>Here is your password reset token: {token}</p>
        </body>
    </html>
    """
    # send mail with the token to the user
    message = MessageSchema(
        subject="Password reset token",
        recipients=[email],  # List of recipients, as many as you can pass
        body=body,
        subtype="html"
    )
    conf = ConnectionConfig(
        MAIL_USERNAME='communication.ltd.2023',
        MAIL_PASSWORD="qlqgjhdtxkqwwudi",
        MAIL_FROM='communication.ltd.2023@gmail.com',
        MAIL_PORT=587,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_FROM_NAME="Communication_LTD",
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True)
    
    fm = FastMail(conf)
    await fm.send_message(message)

    return {"message": "Password reset token sent to your email"}


def update_password(user_id:int,new_pass:str):
    pass

def previous_password_validation(user_id:int,new_pass:str):
    user=get_user_by_user_id(user_id=user_id)
    print(user)
    # for pass in user[]

def validate_token(real_token, user_token):
    return real_token == user_token