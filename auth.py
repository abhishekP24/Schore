import bcrypt
from db import get_db_connection
from datetime import datetime

def create_user(user_id, password, first_name, last_name, email, school, grade, curriculum, role):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (user_id, password, first_name, last_name, email, school, grade, curriculum, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (user_id, hashed_password.decode('utf-8'), first_name, last_name, email, school, grade, curriculum, role)
        )
        connection.commit()
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        cursor.close()
        connection.close()

def validate_user(user_id, password):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return user
    except Exception as e:
        print(f"Error validating user: {e}")
    finally:
        cursor.close()
        connection.close()
    
    return None

def create_event(user_id, event_title, event_date, description):
    # Check if the event date is in the past
    if event_date < datetime.now().date():
        raise ValueError("Event date cannot be in the past.")
    
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO events (user_id, event_title, event_date, description, created_by, creator_role) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, event_title, event_date, description, user_id, 'teacher' if user_id.startswith('teacher') else 'student')
        )
        connection.commit()
    except Exception as e:
        print(f"Error creating event: {e}")
    finally:
        cursor.close()
        connection.close()

def get_available_events():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM events")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching available events: {e}")
    finally:
        cursor.close()
        connection.close()

def enroll_student(event_id, student_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Check if the student is already enrolled in the event
        cursor.execute("SELECT * FROM enrollments WHERE event_id = %s AND student_id = %s", (event_id, student_id))
        existing_enrollment = cursor.fetchone()
        
        if existing_enrollment:
            return False  # Indicate that the student is already enrolled

        # Proceed with enrollment
        cursor.execute(
            "INSERT INTO enrollments (event_id, student_id) VALUES (%s, %s)",
            (event_id, student_id)
        )
        connection.commit()
    except Exception as e:
        print(f"Error enrolling student: {e}")
    finally:
        cursor.close()
        connection.close()

    return True

def get_students_in_event(event_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT u.first_name, u.last_name, u.email FROM users u JOIN enrollments e ON u.user_id = e.student_id WHERE e.event_id = %s",
            (event_id,)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching students in event: {e}")
    finally:
        cursor.close()
        connection.close()

def create_student_activity(user_id, activity_title, activity_date, description):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO events (user_id, event_title, event_date, description, creator_role, created_by) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, activity_title, activity_date, description, 'student', user_id)
        )
        connection.commit()
    except Exception as e:
        print(f"Error adding student activity: {e}")
    finally:
        cursor.close()
        connection.close()

def get_student_activities(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM events WHERE user_id = %s", (user_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching student activities: {e}")
    finally:
        cursor.close()
        connection.close()