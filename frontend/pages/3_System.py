from config.sidebar import init_page
from security.security import check_input

import streamlit as st
import streamlit.components.v1 as components
import httpx
import os


BACKEND_URL = os.getenv("BACKEND_URL")

st.set_page_config(page_title="System", page_icon=":smiley:", layout="wide")
init_page(st)


# check if logged in 
if "user" not in st.session_state or st.session_state["user"] is None:
    st.error("You are not logged in.")
    st.stop()
if "client_created" in st.session_state and st.session_state["client_created"]:
    st.session_state["client_created"] = False
    st.success("Client created successfully.")


# Clients table
st.header("Clients")
url = f"{BACKEND_URL}/clients/get_all/"
res = httpx.get(url, timeout=None)
clients = res.json()


cols = st.columns(spec=[1,4,3,2,2])
cols[1].markdown("**Name**") 
cols[2].markdown("**Email**") 
cols[3].markdown("**Phone**") 
cols[4].markdown("**City**") 


if st.session_state["secure_mode"]:
    for client in clients: 
        row = st.container() 
        cols = row.columns(spec=[1,4,3,2,2])
        
        cols[0].write(client["client_id"]) 
        cols[1].write(client["name"]) 
        cols[2].write(client["email"]) 
        cols[3].write(client["phone"])
        cols[4].write(client["city"]) 
else:
    # Low security mode
    for client in clients: 
        row = st.container() 
        cols = row.columns(spec=[1,4,3,2,2])
        
        with cols[0]:
            components.html(f'{client["client_id"]}', width=0, height=0) 
            st.write(client["client_id"]) 
        with cols[1]:
            components.html(f'{client["name"]}', width=0, height=0) 
            st.write(client["name"]) 
        with cols[2]:
            components.html(f'{client["email"]}', width=0, height=0) 
            st.write(client["email"]) 
        with cols[3]:
            components.html(f'{client["phone"]}', width=0, height=0)
            st.write(client["phone"])
        with cols[4]:
            components.html(f'{client["city"]}', width=0, height=0) 
            st.write(client["city"]) 

st.divider()


expander = st.expander("Create new client")
form = expander.form(key="create_new_client")
name = form.text_input("Name")
email = form.text_input("Email")
phone = form.text_input("Phone")
city = form.text_input("City")
submit = form.form_submit_button("Create new client")
if submit:
    check_input(st, name, email, phone, city)
    url = f"{BACKEND_URL}/clients/create/"
    data = {"name": name, "email": email, "phone": phone, "city": city, "secure_mode": st.session_state["secure_mode"]}
    res = httpx.post(url, json=data, timeout=None)
    if res.status_code == 200:
        st.session_state['client_created'] = True
        st.experimental_rerun()
    else:
        res = res.json()
        expander.error(res['detail'])