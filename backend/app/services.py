import httpx
import os
import app.security as security
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config.config import MAX_LOGIN_ATTEMPTS
import dotenv

mail_secrets = dotenv.dotenv_values(".env")
DB_URL = os.getenv("DB_URL")

async def get_app_data(key: str):
    url = f"{DB_URL}/app/?key={key}"
    response = httpx.get(url, timeout=None)
    return response.json()['value']

async def get_user_by_username(username: str, secure_mode):
    data = {"mode": 'username','ident': username, "secure_mode": secure_mode}
    url = f"{DB_URL}/users"
    response = httpx.post(url, json=data, timeout=None)
    if response.status_code == 200:
        return response.json()['user']
    else:
        return None

async def get_user_by_email(email: str, secure_mode:bool):
    data = {"mode": 'email','ident': email, "secure_mode": secure_mode}
    url = f"{DB_URL}/users"
    response = httpx.post(url, json=data, timeout=None)
    if response.status_code == 200:
        return response.json()['user']
    else:
        return None

async def get_user_by_user_id(user_id: int, secure_mode: bool):
    data = {"mode": 'user_id','ident': user_id, "secure_mode": secure_mode}
    url = f"{DB_URL}/users"
    response = httpx.post(url, json=data, timeout=None)
    if response.status_code == 200:
        return response.json()['user']
    else:
        return None

async def get_all_clients():
    url = f"{DB_URL}/clients/"
    response = httpx.get(url, timeout=None)
    return response.json()

async def create_new_user(username: str, password: str, email: str, secure_mode: bool):
    salt = await get_app_data("salt")
    hashed_password = security.hash_password(salt, password)
    url = f"{DB_URL}/users/create/"
    data = {"username": username, "password": hashed_password, "email": email, "secure_mode": secure_mode}
    response = httpx.post(url, 
        json=data, timeout=None)
    if response.status_code == 200:
        return response.json()['user']
    else:
        return None

async def create_new_client(name: str, email: str, phone: str, city: str, secure_mode: bool):
    url = f"{DB_URL}/clients/create/"
    data = {"name": name, "email": email, "phone": phone, "city": city, "secure_mode": secure_mode}
    response = httpx.post(url, json=data, timeout=None)
    if response.status_code == 200:
        return response.json()['client']
    else:
        return None
    

async def login(username: str, password: str, login_attempts_data: dict, secure_mode: bool):
    if login_attempts_data['no_of_attempts'] > MAX_LOGIN_ATTEMPTS:
        return {'status' : 'error', 'message': 'Account locked, too many login attempts.'}
    salt = await get_app_data("salt")
    hashed_password = security.hash_password(salt, password)
    url = f"{DB_URL}/users/login/"
    res = httpx.post(url, json={'username': username, 'password': hashed_password, 'secure_mode':secure_mode}, timeout=None)
    if res.status_code == 200:
        user = res.json()['user']
        return {'status' : "success", "user" :user}
    else:
        return {"status": "error", "message": "Invalid credentials", 'is_locked': login_attempts_data['no_of_attempts'] == MAX_LOGIN_ATTEMPTS}
    
    
async def change_password(username: str, old_password: str, new_password: str, secure_mode: bool):
    salt = await get_app_data("salt")
    hashed_old_password = security.hash_password(salt, old_password)
    hashed_new_password = security.hash_password(salt, new_password)
    url = f"{DB_URL}/users/change_password/"
    res = httpx.post(url, json={'username': username, 'hashed_old_password': hashed_old_password, 'hashed_new_password': hashed_new_password, "secure_mode":secure_mode}, timeout=None)
    if res.status_code == 200:
        return {'status' : "success"}
    elif res.status_code == 404:
        return {"status": "error", "message": "User not found"}
    elif res.status_code == 401:
        return {"status": "error", "message": "Invalid credentials"}
    elif res.status_code == 409:
        return {"status": "error", "message": "New password cannot be the same as an older one"}
    else:
        return {"status": "error", "message": "Unknown error"}

async def reset_password(email:str, password: str,secure_mode):
    user = await get_user_by_email(email, secure_mode)
    if user is None:
        return {"status": "error", "message": "User not found"}
    salt = await get_app_data("salt")
    hashed_password = security.hash_password(salt, password)
    url = f"{DB_URL}/users/reset_password/"
    res = httpx.post(url, json={'email': email, 'password': hashed_password, "secure_mode":secure_mode}, timeout=None)
    if res.status_code == 200:
        return {"status": "success", "message": "Password reset successfully"}
    else:
        return {"status": "error", "message": res.json()['detail'],'res_code': res.status_code}


async def forgot_password(email: str, secure_mode: bool):
    user = await get_user_by_email(email, secure_mode)
    if user is None:
        return {"status": "error", "message": "User not found", 'res_code': 404}
    
    # generate a random token and send it to the user's email
    # the token will be used to reset the password
    token = security.generate_token()
    res = await send_forgot_password(email, token)
    if res['status'] == "success":
        # save the token in the database
        url = f"{DB_URL}/users/save_token/"
        res = httpx.post(url, json={'email': user['email'], 'token': token, 'secure_mode':secure_mode}, timeout=None)
        if res.status_code == 200:
            return {"status": "success", "message": "Password reset token sent to your email"}
        else:
            return {"status": "error", "message": res.json()['detail'],'res_code': res.status_code}
    elif res['status'] == "error":
        return {"status": "error", "message": res['message'] ,'res_code': res.status_code}
    

async def send_forgot_password(email, token):
    # TODO: make the email better
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
        MAIL_USERNAME=mail_secrets['MAIL_USERNAME'],
        MAIL_PASSWORD=mail_secrets['MAIL_PASSWORD'],
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
    
async def increment_login_attempts(username):
    url = f"{DB_URL}/increment_login_attempts"
    res_increment_login_attempts = httpx.post(url, json={'username': username}, timeout=None)
    res_increment_login_attempts = res_increment_login_attempts.json()
    return res_increment_login_attempts['login_attempts_data']

async def validate_token(token):
    url = f"{DB_URL}/users/validate_token/"
    res = httpx.post(url, json={'token': token}, timeout=None)
    if res.status_code == 200:
        return {"status": "success", "message": "Token is valid"}
    elif res.status_code == 404:
        return {"status": "error", "message": "Token not found", 'res_code': 404}
    elif res.status_code == 401:
        return {"status": "error", "message": "Token is invalid", 'res_code': 401 }
    else:
        return {"status": "error", "message": "Unknown error", 'res_code':500}