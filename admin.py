import streamlit as st
import streamlit_authenticator as stauth
from shared import connect_to_mongodb
from datetime import datetime
import pandas as pd

def authenticate():
    st.title("Admin Authentication")
    st.write("Please enter your credentials.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if username == "admin" and password == "admin123":
        st.session_state.authenticated = True

    if login_button and not st.session_state.get('authenticated', False):
        st.error("Incorrect username or password.")


def upload_schedule(collection):
    st.title("Upload Exam Schedule")

    exam_name = st.text_input("Exam Name")
    exam_date = st.date_input("Select Date of Exam", min_value=datetime.today())
    
    # Convert date to datetime
    exam_date = datetime.combine(exam_date, datetime.min.time())

    # Format the date to display day first, then month and year
    formatted_exam_date = exam_date.strftime('%d-%m-%Y')

    # Dropdown menu for department selection
    departments = ["IT", "CS", "BCA", "BBA", "BMS"]
    department = st.selectbox("Department", departments)

    # Dropdown menu for semester selection
    semesters = ["Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5"]
    semester = st.selectbox("Semester", semesters)

    if st.button("Upload"):
        schedule_data = {
            "exam_name": exam_name,
            "exam_date": formatted_exam_date,
            "department": department,
            "semester": semester
        }
        collection.insert_one(schedule_data)
        st.success("Schedule uploaded successfully!")

def view_recent_schedule(collection):
    st.title("View Exam Schedule")
    schedule_data = collection.find({}, {"_id": 0}).sort("_id", -1)  # Sort by _id in descending order
    df = pd.DataFrame(list(schedule_data))
    
    # Convert exam_date to datetime format
    df['exam_date'] = pd.to_datetime(df['exam_date'])
    
    # Format the date column to remove time
    df['exam_date'] = df['exam_date'].dt.strftime('%Y-%m-%d')
    
    st.table(df)


def main():
    st.set_page_config(layout="wide")  # Move this line to the beginning
    collection = connect_to_mongodb()  # Get MongoDB collection

    if st.session_state.get('authenticated', False):
        st.sidebar.title("Admin Menu")
        page = st.sidebar.radio("Navigation", ["Upload Schedule", "View Schedule"])

        if page == "Upload Schedule":
            upload_schedule(collection)
        elif page == "View Schedule":
            view_recent_schedule(collection)
    else:
        authenticate()

if __name__ == "__main__":
    main()
