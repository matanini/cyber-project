import streamlit as st
from config.sidebar import init_page
from security.security import check_password_policy, check_password_match, check_email
import httpx
import os

BACKEND_URL = os.getenv("BACKEND_URL")

st.set_page_config(page_title="Welcome to Homepage", page_icon=":smiley:")

# def init_page():
#     if "user" not in st.session_state:
#         st.session_state["user"] = None
#     _, col_sidebar, _ = st.sidebar.columns([1, 3, 1])
#     if st.session_state["user"] is not None:
#         col_sidebar.subheader(f"Hello {st.session_state['user']['username']}!")
#         if col_sidebar.button("Logout"):
#             st.session_state["user"] = None
#             st.session_state["logged_out"] = True
#             st.experimental_rerun()
#     else:
#         col_sidebar.write("No user is logged in")
#         col_sidebar.write("Go to Login page")

#     # Security level
#     st.sidebar.divider()
#     _, col_sidebar, _ = st.sidebar.columns([1, 2, 1])
#     col_sidebar.subheader("Security level")
#     st.session_state["secure_mode"] = col_sidebar.selectbox("Select security level", ["Low", "High"]) == "High"

#     # Logo + ©️
#     st.sidebar.divider()
#     _, col_sidebar, _ = st.sidebar.columns([1, 5, 1])
#     col_sidebar.image("https://i.ibb.co/tKm1VRH/comunication-ltd.png", width=200)
#     _, col_sidebar, _ = st.sidebar.columns([1, 3, 1])
#     col_sidebar.markdown(
#         """
#         ©️ Communication LTD
#     """
#     )


init_page(st)


if 'user' in st.session_state and st.session_state['user'] is not None:
    st.success("You are logged in.")
    st.stop()

if "logged_out" in st.session_state and st.session_state['logged_out']:
    st.session_state['logged_out'] = False
    st.warning("You have been logged out, please log in again.")
    st.stop()


def login(container):
    container.title("Login")
    container.write("Please enter your credentials to proceed")
    username = container.text_input("Username", key="username_login")
    password = container.text_input("Password", key="pass_login", type="password")
    if container.button("Login"):
        data = {"username": username, "password": password, 'secure_mode': st.session_state["secure_mode"]}
        url = f"{BACKEND_URL}/login"
        res = httpx.post(url, json=data, timeout=None)
        json_res = res.json()
        if res.status_code == 200:
            st.session_state["user"] = json_res["user"]
            
            st.experimental_rerun()
        else:
            container.error(json_res['detail'])


def register(container):

    container.title("Register")
    container.write("Please enter your credentials to proceed")
    username = container.text_input("Username", key="username_reg")
    password = container.text_input("Password", key="pass_reg", type="password")
    confirm_password = container.text_input("Confirm Password", key="confirm_pass_reg", type="password")
    email = container.text_input("Email", key="email_reg")
    if container.button("Register", key="reg_btn"):
        if not check_password_match(password, confirm_password):
            container.error("Passwords do not match")
        if not check_email(email):
            container.error("Invalid email")
        if not check_password_policy(st, password):
            container.error("Password is not strong enough")
        else:
            data = {"username": username, "password": password, "email": email, "secure_mode" : st.session_state["secure_mode"]}
            url = f"{BACKEND_URL}/register"
            res = httpx.post(url, json=data, timeout=None)
            st.write(res.text)


st.image("https://i.ibb.co/tKm1VRH/comunication-ltd.png")

st.title("Welcome to Communication LTD")
st.write("Please log in or register to proceed")


tab_login, tab_reg = st.tabs(["Login", "Register"])

with tab_login:
    login(st)
with tab_reg:
    register(st)
