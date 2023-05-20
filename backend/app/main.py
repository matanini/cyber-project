from fastapi import FastAPI, Request, HTTPException, Form, status
import app.services as services
from config.config import LOGIN_ATTEMPTS


app = FastAPI(title="Backend")

@app.on_event("startup")
async def startup_event():
    app.session = {}
    app.session["user"] = None
    app.session['is_connected'] = False

    
@app.post('/register')
async def register(request: Request):
    data = await request.json()
    username = data['username']
    password = data['password']
    email = data['email']
    user = await services.create_new_user(username, password, email)
    if user:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data['username']
    password = data['password']
    if 'user_login_counter' not in app.session:
        app.session['user_login_counter'] = 0
    app.session['user_login_counter'] += 1
    if app.session['user_login_counter'] > LOGIN_ATTEMPTS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Too many login attempts")
    res = await services.login(username, password)
    if res['status'] == 'error':
        if app.session['user_login_counter'] == LOGIN_ATTEMPTS:
            pass
            # app.session['login_time'] =
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    elif res['status'] == 'success':
        app.session["user"] = res['user']
        app.session['is_connected'] = True
        del app.session['user_login_counter']
        return {"status": "success", 'user': res['user']}
    
# TODO: DO THIS HERE IN SESSION OR IN DB, SESSION TABLE
# TODO: {user_id:{"login_time":ewww, "login_counter": 0, "is_connected": False, "user": {"user_id": 1, "username": "admin", "email": ""}}

@app.get("/logout")
async def logout(request: Request):
    if not app.session['is_connected']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in")
    
    app.session["user"] = None
    app.session['is_connected'] = False
    return {"status": "success"}

@app.post("/users/change_password")
async def change_password(request: Request, old_password: str = Form(...), new_password: str = Form(...)):
    if not app.session['is_connected']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in")
    
    res = await services.change_password(app.session["user"]["user_id"], old_password, new_password)
    return res
    
@app.post("/clients/create/")
async def create_client(request: Request, name: str = Form(...), email: str = Form(...), phone: str = Form(...), city: str = Form(...)):
    client = services.create_new_client(name, email, phone, city)
    if not client:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Client already exists")
    else:
        return {"status": "success"}
   
@app.post("/uses/forgot_password")
async def forgot_password(request: Request, email: str = Form(...)):
    res = await services.forgot_password(email)
    if res['status'] == 'error':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        return res
    
# @app.post("/users/reset_password")
