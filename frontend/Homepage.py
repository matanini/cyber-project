import streamlit as st
import httpx
import os

BACKEND_URL = os.getenv('BACKEND_URL')

st.set_page_config(page_title="Homepage", page_icon=":smiley:")
def init_page():
    if 'user' not in st.session_state :
        st.session_state['user'] = None
    
    _, col_sidebar ,_=st.sidebar.columns([1,3,1]) 
    _, col_sidebar_user_type ,_=st.sidebar.columns([1,2,1]) 
    if st.session_state['user']:
        col_sidebar.write("User connected: ")
        col_sidebar.write(st.session_state['user'])
    else:
        col_sidebar.write("No user is logged in")
        
    # Security level

    # Logo + ©️

init_page()

st.image("https://i.ibb.co/tKm1VRH/comunication-ltd.png")

st.title("Welcome to Communication LTD")

st.markdown("""
    Dear Roi Zimon,  
    You are welcome to our system.  
    We are excited to see you here!   
    
    Please be kind and grade us with 100 😎.

""")