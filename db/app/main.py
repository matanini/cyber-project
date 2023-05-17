from fastapi import FastAPI, Request, HTTPException, Form, status
import app.services as services
from pydantic import BaseModel

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
    services.init_app()

@app.get("/app/")
async def get_app_value(request: Request, key: str):
    val = services.get_app_data(key)[0]
    return {"key":key, "value": val[0]}

@app.get("/users/all")
async def get_all_users(request: Request):
    users_list = []
    users = services.get_all_users()
    for user in users:
        users_list.append({
            "user_id": user[0], 
            "username": user[1], 
            "email": user[3]
            })
    return users_list

@app.get("/users/")
async def get_user(request: Request, mode: str, ident: int|str):
    if mode == "email":
        user = services.get_user_by_email(ident)
    elif mode == "user_id":
        user = services.get_user_by_user_id(ident)
    elif mode == "username":
        user = services.get_user_by_username(ident)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
    if user:
        return {"status": "success", "user": {"user_id": user[0][0], "username": user[0][1], "email": user[0][3]}}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
@app.get("/clients/")
async def get_clients(request: Request):
    clients_list = []
    clients = services.get_all_clients()
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
    user = await request.json()
    user = user['user']
    username = user['username']
    password = user['password']
    email = user['email']

    user_username = services.get_user_by_username(username)
    user_email = services.get_user_by_email(email)

    print(user)
    if user_username or user_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    else:
        services.create_new_user(username, password, email)
        return {"status": "success", "user": {"username": username, "email": email}}
    
@app.post("/clients/create/")
async def create_client(request: Request, name: str, email: str, phone: str, city: str):
    client = services.get_client_by_email(email)
    if client:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Client already exists")
    else:
        services.create_new_client(name, email, phone, city)
        return {"status": "success", "client": {"name": name, "email": email, "phone": phone, "city": city}}

@app.post("/users/login/")
async def login(request: Request):
    data = await request.json()
    username = data['username']
    password = data['password']
                        
    user = services.get_user_by_username(username)
    print(user)
    if user:
        if user[0][2] == password:
            return {"status": "success", "user" :{"user_id": user[0][0], "username": user[0][1], "email": user[0][3]}}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
@app.post("/users/change_password/")
async def change_password(request: Request):
    data = await request.json()
    user_id = data['user_id']
    hashed_old_password = data['hashed_old_password']
    hashed_new_password = data['hashed_new_password']
    user = services.get_user_by_user_id(user_id)
    if user:
        if user[0][2] == hashed_old_password:
            password_history = user[0][-1].split(",")
            if services.check_old_passwords(hashed_new_password, password_history):
                password_history.append(hashed_old_password)
                updated_user = await services.change_password(user_id, hashed_new_password, password_history)
                print(updated_user)
                return {"status": "success"}
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="New password cannot be the same as the old one")


            
            
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    

@app.post("/users/save_token/")
async def save_token(request: Request):
    data = await request.json()
    email = data['email']
    token = data['token']
    user = services.get_user_by_email(email)
    if user:
        await services.save_new_token(email, token)
        return {"status": "success"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
@app.post("/users/verify_token/")
async def verify_token(request: Request):
    data = await request.json()
    token = data['token']
    token_data = await services.get_token_by_token(token)
    if len(token_data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")
    else:
        print(token_data)

