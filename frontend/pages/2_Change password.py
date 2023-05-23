from config.sidebar import init_page
from security.security import check_password_policy, check_password_match, check_email

import streamlit as st
import httpx
import os


BACKEND_URL = os.getenv("BACKEND_URL")
st.set_page_config(page_title="Change password", page_icon=":smiley:")
init_page(st)


if "logged_out" in st.session_state and st.session_state['logged_out']:
    st.session_state['logged_out'] = False
    st.warning("You have been logged out, please log in again.")
    st.stop()


############# CONTENT #############

# Forgot password
if 'user' not in st.session_state or st.session_state['user'] is None:
    
    st.warning("You are not logged in, please log in first.")
    st.markdown("""
    If you forgot your password, Please enter your email address below.
    A validation code will be sent to your email address.
    """)
    email = st.text_input("Email address")
    if st.button("Send email"):
        if check_email(email):
            response = httpx.post(f"{BACKEND_URL}/users/forgot_password", json={"email": email, "secure_mode": st.session_state['secure_mode']}, timeout=None)
            if response.status_code == 200:
                st.success("Email sent successfully.")
                st.session_state['token_sent'] = True 
            else:
                st.error(response.json()['detail'])
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
                st.session_state['token_validated'] = False
                
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
                            "password": new_password,
                            "secure_mode": st.session_state['secure_mode']
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
                if check_password_policy(st, new_password):
                    response = httpx.post(f"{BACKEND_URL}/users/change_password", json={
                        "username": st.session_state["user"]["username"],
                        "old_password": old_password,
                        "new_password": new_password,
                        "secure_mode": st.session_state["secure_mode"]
                    })
                    response = response.json()
                    if response['status'] == 'success':
                        st.success("Password changed successfully")
                    else:
                        st.error(response['message'])
                