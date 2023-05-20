from fastapi import FastAPI, Request, HTTPException, Form, status, Depends, Response
import app.services as services
# from app.sessions import cookie, SessionData, backend_memory, verifier
from uuid import UUID, uuid4

app = FastAPI(title="Backend")


# @app.on_event("startup")
# async def startup_event():
#     pass


# @app.post("/create_session")
# async def create_session(response: Response):

#     session = uuid4()
#     data = SessionData()

#     await backend_memory.create(session, data)
#     cookie.attach_to_response(response, session)

#     return {"status": "success", "session_id": session}


# @app.get("/whoami", dependencies=[Depends(cookie)])
# async def whoami(session_data: SessionData = Depends(verifier)):
#     print(session_data)
#     return session_data



# @app.post("/delete_session")
# async def del_session(response: Response, session_id: UUID = Depends(cookie)):
#     await backend_memory.delete(session_id)
#     cookie.delete_from_response(response)
#     return "deleted session"


# @app.post('/get_session_data')
# async def get_session_data(request: Request):
#     # data = await request.json()
#     # session_id = data['session_id']
#     # session = await backend_memory.read(session_id)
#     # print(session)
#     # print("whoami", whoami())
#     return await whoami()

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
    # print(session_id)
    
    login_attempts_data = await services.increment_login_attempts(username)
    res = await services.login(username, password, login_attempts_data)
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
    
@app.get("/logout")
async def logout(request: Request):
    # await backend_memory.update(whoami(), SessionData())
    return {"status": "success"}

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
async def create_client(request: Request, name: str = Form(...), email: str = Form(...), phone: str = Form(...), city: str = Form(...)):
    client = services.create_new_client(name, email, phone, city)
    if not client:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Client already exists")
    else:
        return {"status": "success"}
   
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
    # TODO: Check if passwords in history!!!!!!!
    res = await services.reset_password(email, password)
    if res['status'] == 'error':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        return res
    
@app.post("/users/validate_token")
async def validate_token(request: Request):
    data = await request.json()
    token = data['token']
    print(token)
    res = await services.validate_token(token)
    print(res)
    if res['status'] == 'error':
        raise HTTPException(status_code=int(res['res_code']), detail=res['message'])
    else:
        return res