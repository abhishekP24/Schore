import streamlit as st
from auth import create_user, validate_user
from dashboard import show_dashboard
from portfolio import show_portfolio
from calendar1 import show_calendar
import re  # Regular expressions for email validation

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

# Initialize session state for login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Variable to hold the current user ID after successful login
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# Variable to hold the current user role
if "role" not in st.session_state:
    st.session_state.role = ""

# Toggle between Login and Signup
if "signup" not in st.session_state:
    st.session_state.signup = False

st.markdown("""<style>
    .login-container {
        max-width: 400px;
        margin: 5% auto;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        background-color: #f9f9f9;
    }
    .login-header {
        text-align: center;
        margin: 0;
        padding: 0;
        font-size: 1.5em;
    }
    .login-container input {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    .login-container button {
        width: 100%;
        padding: 10px;
        background-color: #28a745;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .login-container button:hover {
        background-color: #218838;
    }
</style>""", unsafe_allow_html=True)

# Show login or signup form if not logged in
if not st.session_state.logged_in:
    if st.session_state.signup:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="login-header">Create a Student Account</h2>', unsafe_allow_html=True)
        
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type='password')
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        school = st.text_input("School")
        grade = st.selectbox("Grade", ["5th Grade", "6th Grade", "7th Grade", "8th Grade", "9th Grade", "10th Grade", "11th Grade", "12th Grade"])
        curriculum = st.text_input("Curriculum")

        if st.button("Sign Up"):
            if not user_id or not password or not first_name or not last_name or not email or not school or not curriculum:
                st.error("Please fill in all fields.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address.")
            else:
                create_user(user_id, password, first_name, last_name, email, school, grade, curriculum, role="student")
                st.success("Account created successfully! You can now log in.")

        if st.button("Back to Login"):
            st.session_state.signup = False

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="login-header">Login to Your Account</h2>', unsafe_allow_html=True)
        
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type='password', key='password_input')

        if st.button("Login"):
            user_data = validate_user(user_id, password)
            if user_data:
                st.session_state.logged_in = True
                st.session_state.user_id = user_data['user_id']  # Save user ID to session
                st.session_state.role = user_data['role']  # Save user role to session
                st.success("Logged in successfully!")
                st.rerun()  # Refresh the app to show dashboard
            else:
                st.error("Invalid user ID or password")

        if st.button("Sign Up"):  
            st.session_state.signup = True

        st.markdown('</div>', unsafe_allow_html=True)
else:
    # User is logged in; show the main content
    st.sidebar.title("Navigation")
    menu_options = ["Dashboard", "Calendar", "Portfolio"]
    choice = st.sidebar.radio("Select a page", menu_options)

    if choice == "Dashboard":
        show_dashboard()  # Show Dashboard

    elif choice == "Calendar":
        show_calendar()  # Show Calendar

    elif choice == "Portfolio":
        show_portfolio()  # Show Portfolio

    # Logout functionality
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = ""
        st.session_state.role = ""
        st.rerun()  # Refresh the app after logout.