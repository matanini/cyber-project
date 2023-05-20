import streamlit as st
import re
from config.config import PASSWORD_POLICY
import httpx
import os

BACKEND_URL = os.getenv("BACKEND_URL")

st.set_page_config(page_title="Welcome to Homepage", page_icon=":smiley:")

def init_page():
    if "user" not in st.session_state:
        st.session_state["user"] = None
    _, col_sidebar, _ = st.sidebar.columns([1, 3, 1])
    if st.session_state["user"] is not None:
        col_sidebar.subheader(f"Hello {st.session_state['user']['username']}!")
        if col_sidebar.button("Logout"):
            st.session_state["user"] = None
            st.session_state["logged_out"] = True
            st.experimental_rerun()
    else:
        col_sidebar.write("No user is logged in")
        col_sidebar.write("Go to Login page")

    # Security level
    st.sidebar.divider()
    _, col_sidebar, _ = st.sidebar.columns([1, 2, 1])
    col_sidebar.subheader("Security level")
    st.session_state["security_level"] = col_sidebar.selectbox("Select security level", ["Low", "High"])

    # Logo + ©️
    st.sidebar.divider()
    _, col_sidebar, _ = st.sidebar.columns([1, 5, 1])
    col_sidebar.image("https://i.ibb.co/tKm1VRH/comunication-ltd.png", width=200)
    _, col_sidebar, _ = st.sidebar.columns([1, 3, 1])
    col_sidebar.markdown(
        """
        ©️ Communication LTD
    """
    )


init_page()


if "logged_out" in st.session_state and st.session_state['logged_out']:
    st.session_state['logged_out'] = False
    st.warning("You have been logged out, please log in again.")
    st.stop()


def check_password_strength(password):
    val = True

    if len(password) < PASSWORD_POLICY["MIN_LENGTH"]:
        st.info(f'length should be at least {PASSWORD_POLICY["MIN_LENGTH"]}')
        val = False

    if len(password) > PASSWORD_POLICY["MAX_LENGTH"]:
        st.info(f'length should be not be greater than {PASSWORD_POLICY["MAX_LENGTH"]}')
        val = False

    dig_count = 0
    up_count = 0
    low_count = 0
    spec_count = 0
    for char in password:
        if char.isdigit():
            dig_count += 1
        elif char.isupper():
            up_count += 1
        elif char.islower():
            low_count += 1
        elif char in PASSWORD_POLICY["SPECIAL_CHARACTERS"]:
            spec_count += 1
        else:
            val = False
            st.info(f"Cant use {char} in password")

    if dig_count < PASSWORD_POLICY["MIN_DIGITS"]:
        st.info(f'Password should have at least {PASSWORD_POLICY["MIN_SPECIAL_CHARACTERS"]} numeral')
        val = False

    if up_count < PASSWORD_POLICY["MIN_UPPERCASE_CHARACTERS"]:
        st.info(f'Password should have at least {PASSWORD_POLICY["MIN_UPPERCASE_CHARACTERS"]} uppercase letter')
        val = False

    if low_count < PASSWORD_POLICY["MIN_LOWERCASE_CHARACTERS"]:
        st.info(f'Password should have at least {PASSWORD_POLICY["MIN_LOWERCASE_CHARACTERS"]} lowercase letter')
        val = False

    if spec_count < PASSWORD_POLICY["MIN_SPECIAL_CHARACTERS"]:
        st.info(f'Password should have at least {PASSWORD_POLICY["MIN_DIGITS"]} special symbols')
        val = False

    return val


def check_email(email):
    format = r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$"
    return re.match(format, email)


def check_password_match(password, confirm_password):
    return password == confirm_password


def login(container):
    container.title("Login")
    container.write("Please enter your credentials to proceed")
    username = container.text_input("Username", key="username_login")
    password = container.text_input("Password", key="pass_login", type="password")
    if container.button("Login"):
        data = {"username": username, "password": password}
        url = f"{BACKEND_URL}/login"
        res = httpx.post(url, json=data, timeout=None)
        st.write(res.text)
        if res.status_code:
            # st.session_state['is_connected'] = True
            st.session_state["user"] = res.json()["user"]
            container.success("Login successful")
        else:
            container.error("Login failed, invalid credentials")


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
        if not check_password_strength(password):
            container.error("Password is not strong enough")
        else:
            data = {"username": username, "password": password, "email": email}
            url = f"{BACKEND_URL}/register"

            #  TODO: add cert verification
            res = httpx.post(url, json=data, timeout=None, verify=False)
            st.write(res.text)


st.image("https://i.ibb.co/tKm1VRH/comunication-ltd.png")

st.title("Welcome to Communication LTD")
st.write("Please log in or register to proceed")


tab_login, tab_reg = st.tabs(["Login", "Register"])

with tab_login:
    login(st)
with tab_reg:
    register(st)
