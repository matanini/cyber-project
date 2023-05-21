import streamlit as st
import re
from config.config import PASSWORD_POLICY
from security.security import check_password_policy, check_password_match
import httpx
import os

BACKEND_URL = os.getenv("BACKEND_URL")

st.set_page_config(page_title="Change password", page_icon=":smiley:")

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

# def check_password_strength(password):
#     val = True

#     if len(password) < PASSWORD_POLICY["MIN_LENGTH"]:
#         st.info(f'length should be at least {PASSWORD_POLICY["MIN_LENGTH"]}')
#         val = False

#     if len(password) > PASSWORD_POLICY["MAX_LENGTH"]:
#         st.info(f'length should be not be greater than {PASSWORD_POLICY["MAX_LENGTH"]}')
#         val = False

#     dig_count = 0
#     up_count = 0
#     low_count = 0
#     spec_count = 0
#     for char in password:
#         if char.isdigit():
#             dig_count += 1
#         elif char.isupper():
#             up_count += 1
#         elif char.islower():
#             low_count += 1
#         elif char in PASSWORD_POLICY["SPECIAL_CHARACTERS"]:
#             spec_count += 1
#         else:
#             val = False
#             st.info(f"Cant use {char} in password")

#     if dig_count < PASSWORD_POLICY["MIN_DIGITS"]:
#         st.info(f'Password should have at least {PASSWORD_POLICY["MIN_SPECIAL_CHARACTERS"]} numeral')
#         val = False

#     if up_count < PASSWORD_POLICY["MIN_UPPERCASE_CHARACTERS"]:
#         st.info(f'Password should have at least {PASSWORD_POLICY["MIN_UPPERCASE_CHARACTERS"]} uppercase letter')
#         val = False

#     if low_count < PASSWORD_POLICY["MIN_LOWERCASE_CHARACTERS"]:
#         st.info(f'Password should have at least {PASSWORD_POLICY["MIN_LOWERCASE_CHARACTERS"]} lowercase letter')
#         val = False

#     if spec_count < PASSWORD_POLICY["MIN_SPECIAL_CHARACTERS"]:
#         st.info(f'Password should have at least {PASSWORD_POLICY["MIN_DIGITS"]} special symbols')
#         val = False
    
#     if password in PASSWORD_POLICY["PASSWORD_DICT"]:
#         st.info("Password is too common")
#         val = False

#     return val


# def check_password_match(password, confirm_password):
#     return password == confirm_password


init_page()


if "logged_out" in st.session_state and st.session_state['logged_out']:
    st.session_state['logged_out'] = False
    st.warning("You have been logged out, please log in again.")
    st.stop()


############# CONTENT #############

# Forgot password
if 'user' not in st.session_state or st.session_state['user'] is None:
    def check_email(email):
        format = r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$"
        return re.match(format, email)


    st.warning("You are not logged in, please log in first.")
    st.markdown("""
    If you forgot your password, Please enter your email address below.
    A validation code will be sent to your email address.
    """)
    email = st.text_input("Email address")
    if st.button("Send email"):
        if check_email(email):
            response = httpx.post(f"{BACKEND_URL}/users/forgot_password", json={"email": email}, timeout=None)
            if response.status_code == 200:
                st.success("Email sent successfully.")
                st.session_state['token_sent'] = True 
            else:
                res = response.json()
                st.error(res['message'])
        else:
            st.error("Invalid email address.")
    
    if 'token_sent' in st.session_state and st.session_state['token_sent']:
        st.markdown("""
        Please enter the validation code you received in your email address.
        """)
        token = st.text_input("Validation code")
        if st.checkbox("Validate"):
            response = httpx.post(f"{BACKEND_URL}/users/validate_token", json={"email": email, "token": token}, timeout=None)
            response = response.json()
            if response['status'] == "success":
                st.success("Token validated successfully.")
                st.session_state['token_validated'] = True
            else:
                st.error(response['message'])
        if 'token_validated' in st.session_state and st.session_state['token_validated']:
            form = st.form(key='reset_password_form')
            new_password = form.text_input("New password", type="password")
            confirm_password = form.text_input("Confirm password", type="password")
            if form.form_submit_button("Reset password"):
                if not check_password_match(new_password, confirm_password):
                    st.error("New password and confirm password do not match")
                else:
                    if check_password_policy(st, new_password):
                        response = httpx.post(f"{BACKEND_URL}/users/reset_password", json={
                            "email": email,
                            "password": new_password
                        })
                        st.write(response.text)
                        response = response.json()
                        if response['status'] == 'success':
                            st.success("Password changed successfully")
                            st.session_state['token_validated'] = False
                            st.session_state['token_sent'] = False
                        else:
                            st.error(response['message'])

    # st.session_state['token_validated'] = False
    # st.session_state['token_sent'] = False
    st.stop()




# Change password
else:
    st.header("Change password")
    _, col, _ = st.columns([1, 3, 1])
    with col:
        old_password = st.text_input("Old password", type="password")
        new_password = st.text_input("New password", type="password")
        confirm_password = st.text_input("Confirm new password", type="password")
        if st.button("Change password"):
            if not check_password_match(new_password, confirm_password):
                st.error("New password and confirm password do not match")
            else:
                if check_password_policy(new_password):
                    response = httpx.post(f"{BACKEND_URL}/users/change_password", json={
                        "username": st.session_state["user"]["username"],
                        "old_password": old_password,
                        "new_password": new_password
                    })
                    response = response.json()
                    if response['status'] == 'success':
                        st.success("Password changed successfully")
                    else:
                        st.error(response['message'])
                