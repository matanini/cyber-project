import streamlit as st

# Create an empty container
st.set_page_config(layout="wide")
st.title("Welcome to Comunication_LTD")
placeholder = st.empty()

actual_email = "email"
actual_password = "password"
# Insert a form in the container
# st.markdown(
#     """
#     <style>
#         div[data-testid="column"]
#         {
#             border: 1px red;
#             align-text: center;
#             width: 50%;
#         }


#     </style>
#     """,unsafe_allow_html=True
# )
st.markdown(
        """
    <style>
        div[data-testid="column"]
        {
            border: 1px solid red;
            border-radius: 20px;
            
            text-align: center;
            width: 50px;
            
        } 
        div[data-testid="stForm"]{
            width: 500px;
        }
        button[data-testid="stFormSubmitButton"]{
        width: 250px;
        }

        
    </style>
    """,
        unsafe_allow_html=True,
    )
with placeholder.form("Login"):
    st.markdown("Please log in or create a new account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("Login")
    with col2:
        register = st.form_submit_button("Register")

if submit and email == actual_email and password == actual_password:
    # If the form is submitted and the email and password are correct,
    # clear the form/container and display a success message
    placeholder.empty()
    st.success("Login successful")
elif submit and email != actual_email and password != actual_password:
    st.error("Login failed")
else:
    pass


# st.markdown(
#     """
#     <style>
#         div[data-testid="column"]:nth-of-type(1)
#         {
#             border:1px solid red;
#         }

#         div[data-testid="column"]:nth-of-type(2)
#         {
#             border:1px solid blue;
#             text-align: end;
#         }
#     </style>
#     """,unsafe_allow_html=True
# )

# col1, col2, col3 = st.columns(3)

# with col1:
#     """
#     ## Column 1
#     Lorem ipsum dolor sit amet, consectetur adipiscing elit,
#     sed do eiusmod tempor incididunt ut labore et dolore
#     magna aliqua. Volutpat sed cras ornare arcu dui vivamus.
#     """
# with col2:
#     """
#     ## Column 2
#     Stuff aligned to the right
#     """
#     st.button("➡️")
# with col3:
#     """
#     ## Column 3
#     This column was untouched by our CSS
#     """
#     st.button("🐈")
