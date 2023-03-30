# (A) INIT
# (A1) LOAD MODULES
from flask import Flask, render_template, request, make_response
import sqlite3
 
# (A2) FLASK SETTINGS + INIT
HOST_NAME = "localhost"
HOST_PORT = 80
DBFILE = "users.db"
app = Flask(__name__)
# app.debug = True


# (B) HELPER - GET ALL USERS FROM DATABASE
def getusers():
  conn = sqlite3.connect(DBFILE)
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM `users`")
  results = cursor.fetchall()
  conn.close()
  return results

# (C) DEMO PAGE - SHOW USERS IN TABLE
@app.route("/")
def index():
  # (C1) GET ALL USERS
  users = getusers()
  # print(users)
 
  # (C2) RENDER HTML PAGE
  return render_template("users.html", usr=users)
 
# (D) START
if __name__ == "__main__":
  app.run(HOST_NAME, HOST_PORT)