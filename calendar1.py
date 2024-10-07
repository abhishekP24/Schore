import streamlit as st
from auth import get_available_events, enroll_student, get_students_in_event

def show_calendar():
    st.subheader("Activity Calendar")
    st.write("Here are your upcoming activities:")

    available_events = get_available_events()
    
    if available_events:
        for event in available_events:
            # Determine the event type and style
            if event['creator_role'] == "teacher":
                event_style = "color: black; padding: 10px; border: 1px solid #ccc; border-radius: 5px;"
                event_type = "Teacher Created"
            else:
                event_style = "color: slateblue; padding: 10px; border: 1px solid #ccc; border-radius: 5px;"
                event_type = "Student Created"
            
            st.markdown(
                f"<div style='{event_style}'>"
                f"<strong>{event['event_title']}</strong> on {event['event_date']}: {event['description']} ({event_type})"
                "</div>",
                unsafe_allow_html=True
            )

            st.markdown("<div style='margin: 1px 0;'></div>", unsafe_allow_html=True)  # Small space

            # Allow students to enroll in events created by teachers
            if event['creator_role'] == "teacher":
                if st.session_state.role == "student":
                    if st.button(f"Enroll in {event['event_title']}", key=f"enroll_{event['id']}"):
                        if enroll_student(event['id'], st.session_state.user_id):
                            st.success(f"You have successfully enrolled in {event['event_title']}!")
                        else:
                            st.error("You are already enrolled in this event.")
                # Allow teachers to view enrolled students for events they created
                elif st.session_state.role == "teacher":
                    if st.button(f"View Enrolled Students for {event['event_title']}", key=f"view_students_{event['id']}"):
                        enrolled_students = get_students_in_event(event['id'])
                        if enrolled_students:
                            st.write("Enrolled Students:")
                            for student in enrolled_students:
                                st.write(f"- {student['first_name']} {student['last_name']} (Email: {student['email']})")
                        else:
                            st.write("No students enrolled in this event.")
            
            elif event['creator_role'] == "student":
                if st.session_state.role == "student":
                    if st.button(f"Enroll in {event['event_title']}", key=f"enroll_{event['id']}"):
                        if enroll_student(event['id'], st.session_state.user_id):
                            st.success(f"You have successfully enrolled in {event['event_title']}!")
                        else:
                            st.error("You are already enrolled in this event.")
                else:
                    st.write("This is a Student created event.")

            # Add space after the entire event block for separation
            st.markdown("<br><br><br>", unsafe_allow_html=True)  # Adds 3 lines of space after each event

    else:
        st.write("No events available for enrollment.")