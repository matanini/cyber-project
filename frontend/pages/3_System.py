import streamlit as st

st.set_page_config(page_title="System", page_icon=":smiley:")
if 'test' not in st.session_state:
    st.session_state['test'] = None

new = st.text_input("Enter new value")
if st.button("Update"):
    st.session_state['test'] = new
    st.experimental_rerun()

st.json(st.session_state)