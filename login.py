import streamlit as st

# Define correct login credentials (you can enhance this later for more security)
USER_CREDENTIALS = {"username": "admin", "password": "password123"}

# Function for checking login credentials
def check_login(username, password):
    if username == USER_CREDENTIALS["username"] and password == USER_CREDENTIALS["password"]:
        return True
    return False

def login_form():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.rerun()  # This will refresh the page to show the rest of the app after login
        else:
            st.error("Incorrect username or password.")
