from fastapi import FastAPI, Request, HTTPException, Form, status
import app.services as services
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.config.config import DATE_TIME_FORMAT

class User(BaseModel):
    username: str
    email: str

class UserPassword(User):
    password: str

class Client(BaseModel):
    name: str
    email: str
    phone: str
    city: str


app = FastAPI(title="DB")

@app.on_event("startup")
async def startup_event():
    await services.init_app()

@app.get('/test')
async def test(client_id: str, mode : bool):
   return await services.get_client_by_id(client_id, mode)

@app.get('/drop_table')
async def drop_table():
    q = "DROP TABLE `login_attempts`"
    await services.exec_insert_query(q)
    await services.create_database()

@app.get("/app/")
async def get_app_value(request: Request, key: str):
    val = await services.get_app_data(key)
    return {"key":key, "value": val[0][0]}

@app.get("/users/all")
async def get_all_users(request: Request):
    users_list = []
    users = await services.get_all_users()
    for user in users:
        users_list.append({
            "user_id": user[0], 
            "username": user[1], 
            "email": user[3]
            })
    return users_list

@app.post("/users")
async def get_user(request: Request):
    data = await request.json()
    mode = data['mode']
    ident = data['ident']
    secure_mode = data['secure_mode']

    if mode == "email":
        user = await services.get_user_by_email(ident, secure_mode)
    elif mode == "user_id":
        user = await services.get_user_by_user_id(ident)
    elif mode == "username":
        user = await services.get_user_by_username(ident, secure_mode)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
    if user:
        return {"status": "success", "user": {"user_id": user[0][0], "username": user[0][1], "email": user[0][3]}}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
@app.get("/clients/")
async def get_clients(request: Request):
    clients_list = []
    clients = await services.get_all_clients()
    for client in clients:
        clients_list.append({
            "client_id": client[0], 
            "name": client[1], 
            "email": client[2], 
            "phone": client[3], 
            "city": client[4]
            })
    return clients_list

@app.post("/users/create/")
async def create_user(request:Request):
    data = await request.json()
    # user = user['user']
    username = data['username']
    password = data['password']
    email = data['email']
    secure_mode = data['secure_mode']
    user_username = await services.get_user_by_username(username, secure_mode)
    user_email = await services.get_user_by_email(email, secure_mode)

    if user_username or user_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    else:
        await services.create_new_user(username, password, email, secure_mode)
        return {"status": "success", "user": {"username": username, "email": email}}
    
@app.post("/clients/create/")
async def create_client(request: Request):
    data = await request.json()
    name = data['name']
    email = data['email']
    phone = data['phone']
    city = data['city']
    secure_mode = data['secure_mode']
    client = await services.get_client_by_email(email, secure_mode)
    if client:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Client already exists")
    else:
        await services.create_new_client(name, email, phone, city, secure_mode)
        return {"status": "success", "client": {"name": name, "email": email, "phone": phone, "city": city}}

@app.post("/users/login/")
async def login(request: Request):
    data = await request.json()
    username = data['username']
    password = data['password']
    secure_mode = data['secure_mode']
    user = await services.get_user_by_username(username, secure_mode)
    if user:
        if user[0][2] == password:
            await services.delete_login_attempt(username)
            return {"status": "success", "user" :{"user_id": user[0][0], "username": user[0][1], "email": user[0][3]}}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
@app.post("/users/change_password/")
async def change_password(request: Request):
    data = await request.json()
    username = data['username']
    hashed_old_password = data['hashed_old_password']
    hashed_new_password = data['hashed_new_password']
    secure_mode = data['secure_mode']
    
    user = await services.get_user_by_username(username, secure_mode)
    if user:
        if user[0][2] == hashed_old_password:
            password_history = user[0][-1].split(",")
            if services.check_old_passwords(hashed_new_password, password_history):
                password_history.append(hashed_new_password)
                await services.change_password(username, hashed_new_password, password_history, secure_mode)
                return {"status": "success"}
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="New password cannot be the same as an older one")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
@app.post("/users/reset_password/")
async def reset_password(request: Request):
    data = await request.json()
    email = data['email']
    password = data['password']
    secure_mode = data['secure_mode']

    user = await services.get_user_by_email(email, secure_mode)
    
    if user:
        token_data = services.get_token_data_by_mail(email)
        if len(token_data) > 0:
            if datetime.strptime(token_data[0][2], DATE_TIME_FORMAT) < datetime.now():
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        password_history = user[0][-1].split(",")
        if services.check_old_passwords(password, password_history):
            password_history.append(password)
            await services.reset_password(email, password, password_history, secure_mode)
            return {"status": "success"}
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="New password cannot be the same as an older one")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.post("/users/save_token/")
async def save_token(request: Request):
    data = await request.json()
    email = data['email']
    token = data['token']
    secure_mode = data['secure_mode']
    user = await services.get_user_by_email(email, secure_mode)
    if user:
        await services.save_new_token(email, token)
        return {"status": "success"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    

@app.post('/users/validate_token/')
async def validate_token(request: Request):
    data = await request.json()
    token = data['token']
    token_data = await services.get_token_data_by_token(token)

    if len(token_data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")
    else:
        if datetime.strptime(token_data[0][2], DATE_TIME_FORMAT) < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        else:
            return {"status": "success"}

@app.post("/increment_login_attempts")
async def increment_login_attempts(request: Request):
    data = await request.json()
    username = data['username']
    user_login_attempts = await services.increment_login_attempts(username)
    
    login_attempts_data = {'username' : username, 'no_of_attempts' : user_login_attempts[2], 'last_attempt': user_login_attempts[3]}
    return {"status": "success", 'login_attempts_data':login_attempts_data}
