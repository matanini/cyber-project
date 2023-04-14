#  Create the database
#  Create tables - Users, Clients
#  add user to Users table
#  check password
import re
import sqlite3
from config import DBFILE, PASSWORD_POLICY

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



def previous_password_validation(user_id:int,new_pass:str):
    user=get_user_by_user_id(user_id=user_id)
    print(user)
    # for pass in user[]

