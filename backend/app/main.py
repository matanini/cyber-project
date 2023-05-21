from fastapi import FastAPI, Request, HTTPException, Form, status, Depends, Response
import app.services as services
# from app.sessions import cookie, SessionData, backend_memory, verifier
from uuid import UUID, uuid4

app = FastAPI(title="Backend")


# @app.on_event("startup")
# async def startup_event():
#     pass

@app.post('/register')
async def register(request: Request):
    data = await request.json()
    username = data['username']
    password = data['password']
    email = data['email']
    secure_mode = data['secure_mode']

    user = await services.create_new_user(username, password, email, secure_mode)
    if user:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data['username']
    password = data['password']
    secure_mode = data['secure_mode']
    
    login_attempts_data = await services.increment_login_attempts(username)
    res = await services.login(username, password, login_attempts_data, secure_mode)
    if res['status'] == 'error':
        if res['message'] == 'Account locked, too many login attempts.':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account locked, cannot login right now")
        if res['is_locked']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials, account locked")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    elif res['status'] == 'success':
        return {"status": "success", 'user': res['user']}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
    
# @app.get("/logout")
# async def logout(request: Request):
#     return {"status": "success"}

@app.post("/users/change_password")
async def change_password(request: Request):
    data = await request.json()
    username = data['username']
    old_password = data['old_password']
    new_password = data['new_password']

    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in")
        
    res = await services.change_password(username, old_password, new_password)
    return res
    
@app.post("/clients/create/")
async def create_client(request: Request):
    data = await request.json()
    name = data['name']
    email = data['email']
    phone = data['phone']
    city = data['city']
    secure_mode = data['secure_mode']
    print("backend create_client", name, email, phone, city, secure_mode)
    client = await services.create_new_client(name, email, phone, city, secure_mode)
    if not client:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Client already exists")
    else:
        return {"status": "success"}
   
@app.get("/clients/get_all/")
async def get_all_clients(request: Request):
    clients = await services.get_all_clients()
    return clients

@app.post("/users/forgot_password")
async def forgot_password(request: Request):
    data = await request.json()
    email = data['email']

    res = await services.forgot_password(email)
    if res['status'] == 'error':
        raise HTTPException(status_code=int(res['res_code']), detail=res['message'])
    else:
        return res
    
@app.post("/users/reset_password")
async def reset_password(request: Request):
    data = await request.json()
    email = data['email']
    password = data['password']

    res = await services.reset_password(email, password)
    print("reset_password", res)
    # if res['status'] == 'error':
    #     raise HTTPException(status_code=res['res_code'], detail=res['message'])
    # else:
    return res
    
@app.post("/users/validate_token")
async def validate_token(request: Request):
    data = await request.json()
    token = data['token']

    res = await services.validate_token(token)
    return res