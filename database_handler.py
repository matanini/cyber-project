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

    cursor.execute(q,params)
    result = cursor.fetchone()
    
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

# (B) HELPER - GET ALL USERS FROM DATABASE
def get_users():
  q="SELECT * FROM `users`"
  results = exec_select_query(q)
  return results