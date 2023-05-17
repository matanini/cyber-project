import httpx
import os
import app.security as security
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


DB_URL = os.getenv("DB_URL")

async def get_app_data(key: str):
    url = f"{DB_URL}/app/?key={key}"
    response = httpx.get(url, timeout=None)
    return response.json()['value']

async def get_user_by_username(username: str):
    url = f"{DB_URL}/users/?mode=username&ident={username}"
    response = httpx.get(url, timeout=None)
    if response.status_code == 200:
        return response.json()['user']
    else:
        return None

async def get_user_by_email(email: str):
    url = f"{DB_URL}/users/?mode=email&ident={email}"
    response = httpx.get(url, timeout=None)
    if response.status_code == 200:
        return response.json()['user']
    else:
        return None

async def get_user_by_user_id(user_id: int):
    url = f"{DB_URL}/users/?mode=user_id&ident={user_id}"
    response = httpx.get(url, timeout=None)
    if response.status_code == 200:
        return response.json()['user']
    else:
        return None

async def get_all_clients():
    url = f"{DB_URL}/clients/"
    response = httpx.get(url, timeout=None)
    return response.json()

async def create_new_user(username: str, password: str, email: str):
    salt = await get_app_data("salt")
    hashed_password = security.hash_password(salt, password)
    url = f"{DB_URL}/users/create/"
    data = {"username": username, "password": hashed_password, "email": email}
    # for d in data:
    #     print(d, data[d], type(data[d]))
    response = httpx.post(url, 
        json={'user':data}, timeout=None)
    print(response.text)
    if response.status_code == 200:
        return response.json()['user']
    else:
        return None

async def create_new_client(name: str, email: str, phone: str, city: str):
    url = f"{DB_URL}/clients/create/"
    data = {"name": name, "email": email, "phone": phone, "city": city}
    response = httpx.post(url, data=data, timeout=None)
    if response.status_code == 200:
        return response.json()['client']
    else:
        return None
    

async def login(username: str, password: str):
    salt = await get_app_data("salt")
    hashed_password = security.hash_password(salt, password)
    url = f"{DB_URL}/users/login/"
    res = httpx.post(url, json={'username': username, 'password': hashed_password}, timeout=None)
    if res.status_code == 200:
        user = res.json()['user']
        return {'status' : "success", "user" :user}
    else:
        return {"status": "error", "message": "Invalid credentials"}
    
    
async def change_password(user_id: str, old_password: str, new_password: str):
    salt = await get_app_data("salt")
    hashed_old_password = security.hash_password(salt, old_password)
    hashed_new_password = security.hash_password(salt, new_password)
    url = f"{DB_URL}/users/change_password/"
    res = httpx.post(url, json={'user_id': user_id, 'hashed_old_password': hashed_old_password, 'hashed_new_password': hashed_new_password}, timeout=None)
    print(res.text)
    if res.status_code == 200:
        return {'status' : "success"}
    elif res.status_code == 404:
        return {"status": "error", "message": "User not found"}
    elif res.status_code == 401:
        return {"status": "error", "message": "Invalid credentials"}
    elif res.status_code == 409:
        return {"status": "error", "message": "New password cannot be the same as the old one"}
    else:
        return {"status": "error", "message": "Unknown error"}

async def forgot_password(email: str):
    user = await get_user_by_email(email)
    print(user)
    if user is None:
        return {"status": "error", "message": "User not found"}
    
    # generate a random token and send it to the user's email
    # the token will be used to reset the password
    token = security.generate_token()
    res = await send_forgot_password(email, token)
    if res['status'] == "success":
        # save the token in the database
        url = f"{DB_URL}/users/save_token/"
        res = httpx.post(url, json={'email': user['email'], 'token': token}, timeout=None)
        if res.status_code == 200:
            return {"status": "success", "message": "Password reset token sent to your email"}
        else:
            return {"status": "error", "message": "Unknown error"}
    else:
        return {"status": "error", "message": "Unknown error"}
    

async def send_forgot_password(email, token):
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
        recipients=[email],  
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
    try:
        await fm.send_message(message)
        return {"status": "success", "message": "Password reset token sent to your email", "token": token}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
