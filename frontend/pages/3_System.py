import streamlit as st
import os
import re
import httpx
from config.sidebar import init_page

BACKEND_URL = os.getenv("BACKEND_URL")

st.set_page_config(page_title="System", page_icon=":smiley:")
init_page(st)
def check_email(email):
        format = r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$"
        return re.match(format, email)
def check_phone(phone):
    format = r"^\+?[0-9]+$"
    return re.match(format, phone)
def check_input(name, email, phone, city):
    if name == "": st.error("Name cannot be empty.")
    if email == "": st.error("Email cannot be empty.")
    if phone == "": st.error("Phone cannot be empty.")
    if city == "": st.error("City cannot be empty.")
    if not check_email(email): st.error("Invalid email format.")


# check if logged in 
if "user" not in st.session_state or st.session_state["user"] is None:
    st.error("You are not logged in.")
    st.stop()
if "client_created" in st.session_state and st.session_state["client_created"]:
    st.session_state["client_created"] = False
    st.success("Client created successfully.")


# Clients tanle
st.header("Clients")
url = f"{BACKEND_URL}/clients/get_all/"
res = httpx.get(url, timeout=None)
clients = res.json()


cols = st.columns(spec=[1,2,2,2,2]) 
cols[1].markdown("**Name**") 
cols[2].markdown("**Email**") 
cols[3].markdown("**Phone**") 
cols[4].markdown("**City**") 

    
for client in clients: 
    row = st.container() 
    cols = row.columns(spec=[1,2,2,2,2]) 
    cols[0].write(client["client_id"]) 
    cols[1].write(client["name"]) 
    cols[2].write(client["email"]) 
    cols[3].write(client["phone"])
    cols[4].write(client["city"]) 

st.divider()
# Create new client
# st.header("Create new client")
expander = st.expander("Create new client")
form = expander.form(key="create_new_client")
name = form.text_input("Name")
email = form.text_input("Email")
phone = form.text_input("Phone")
city = form.text_input("City")
submit = form.form_submit_button("Create new client")
if submit:
    check_input(name, email, phone, city)
    url = f"{BACKEND_URL}/clients/create/"
    data = {"name": name, "email": email, "phone": phone, "city": city, "secure_mode": st.session_state["secure_mode"]}
    res = httpx.post(url, json=data, timeout=None)
    if res.status_code == 200:
        st.session_state['client_created'] = True
        st.experimental_rerun()
    else:
        res = res.json()
        expander.error(res['detail'])