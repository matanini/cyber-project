import streamlit as st
import os
from config.sidebar import init_page

BACKEND_URL = os.getenv('BACKEND_URL')

st.set_page_config(page_title="Homepage", page_icon=":smiley:")

init_page(st)

st.image("https://i.ibb.co/tKm1VRH/comunication-ltd.png")

st.title("Welcome to Communication LTD")

st.markdown("""
    Dear Roi Zimon,  
    You are welcome to our system.  
    We are excited to see you here!   
    
    Please be kind and grade us with 100 😎.

    ### Vulnerabilities:
    - [x] SQL Injection:
        - [x] [REGISTER : username] 1' OR 'a'='a'; drop table 'tokens' --
        - [x] [LOGIN : username] a' OR '1'='1'; drop table 'users' --
        - [x] [SYSTEM : city] w'); drop table 'clients' --
    - [x] Stored XSS:
        - [x] [SYSTEM : any input] <script>alert("XSS MUAHAHAHAHA 😈")</script>

""")