#  Create the database
#  Create tables - Users, Clients
#  add user to Users table
#  check password

import sqlite3
from config import DBFILE

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