from fastapi import FastAPI, Request, HTTPException, Form, status, Depends, Response
import app.services as services
from app.config.config import LOGIN_ATTEMPTS
from app.sessions import cookie, SessionData, backend_memory, verifier
from uuid import UUID, uuid4

app = FastAPI(title="Backend")

@app.on_event("startup")
async def startup_event():
    app.session = {}
    app.session["user"] = None
    app.session['is_connected'] = False

@app.post("/create_session/{name}")
async def create_session(name: str, response: Response):

    session = uuid4()
    data = SessionData(username=name)

    await backend_memory.create(session, data)
    cookie.attach_to_response(response, session)

    return f"created session for {name}"


@app.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data


@app.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend_memory.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"
@app.get('/user_connected')
async def user_connected():
    return app.session


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
    res = await services.login(username, password)
    if res['status'] == 'error':
        await services.increment_login_attempts(username)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    elif res['status'] == 'success':
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
