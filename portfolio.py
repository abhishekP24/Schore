import streamlit as st
from auth import create_event

def show_portfolio():
    st.subheader("My Portfolio")

    # Input fields for creating events
    event_title = st.text_input("Event Title")
    description = st.text_area("Description")
    event_date = st.date_input("Event Date")

    # Button to add a new event
    if st.button("Add Event"):
        if event_title and description and event_date:
            try:
                create_event(st.session_state.user_id, event_title, event_date, description)
                st.success("Event created successfully!")
            except ValueError as ve:
                st.error(str(ve))  # Show the error message for invalid dates
            except Exception as e:
                st.error("An error occurred while creating the event.")
        else:
            st.error("Please fill in all fields.")