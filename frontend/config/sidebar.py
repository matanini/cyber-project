def init_page(st):
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
    st.session_state["secure_mode"] = col_sidebar.selectbox("Select security level", ["Low", "High"]) == 'High'

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