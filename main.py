from fastapi import FastAPI, Request, HTTPException, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import hmac
import hashlib

from secret import SECRET
import services 


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/forgot-password", response_class=HTMLResponse)
def forgot_password(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})
# render_template("forgot_password.html")


@app.get("/change-password", response_class=HTMLResponse)
def change_password(request: Request):
    return templates.TemplateResponse("change_password.html", {"request": request}) 
# render_template("change_password.html")


@app.get("/intended-change-password", response_class=HTMLResponse)
def intended_change_password(request: Request):
    return templates.TemplateResponse("intended_change_password.html", {"request": request})
    # render_template("intended_change_password.html")


@app.post("/check-login", response_class=HTMLResponse)
async def check_login( request: Request, username: str = Form(...), password: str = Form(...)):
    if not services.get_user_by_username(username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username do not exist")

    # Hash the password using HMAC
    hashed_password = hmac.new(SECRET, password.encode("utf-8"), hashlib.sha256).hexdigest()

    result = services.db_check_login(username, hashed_password)
    # If the result is not None, then the login was successful
    if result:
        return RedirectResponse(url="/system", status_code=status.HTTP_200_OK)
    else:
        return templates.TemplateResponse("failure.html", {"request": request})


@app.post("/register", response_class=HTMLResponse)
def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
             ):

    if not services.check_valid_email(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email")
    
    if services.get_user_by_email(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    if services.get_user_by_username(username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    # TODO: Check if the password is strong enough

    # Check if the passwords match
    if confirm_password != password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Hash the password using HMAC
    hashed_password = hmac.new(SECRET, password.encode("utf-8"), hashlib.sha256).hexdigest()

    # Add the user to the database
    services.db_add_new_user(username, hashed_password, email)

    # Redirect to the homepage
    return RedirectResponse(url="/", status_code=status.HTTP_201_CREATED)


@app.get("/system", response_class=HTMLResponse)
def get_system_page(request: Request = None):
    clients = services.get_all_clients()
    return templates.TemplateResponse("system.html", {"request": request, "clients": clients}) 

