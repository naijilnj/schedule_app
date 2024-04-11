import streamlit as st
from shared import connect_to_mongodb
import pandas as pd

def filter_schedule(collection):
    st.title("Filter Exam Schedule")

    # Dropdown menu for department selection
    departments = ["IT", "CS", "BCA", "BBA", "BMS"]
    department = st.selectbox("Select Department", departments)

    # Dropdown menu for semester selection
    semesters = ["Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5"]
    semester = st.selectbox("Select Semester", semesters)

    # Filter schedule based on department and semester
    filtered_schedule = collection.find({"department": department, "semester": semester}, {"_id": 0})
    df = pd.DataFrame(list(filtered_schedule))

    # Check if 'exam_date' column exists
    if 'exam_date' in df.columns:
        # Convert exam_date to datetime format and remove time component
        df['exam_date'] = pd.to_datetime(df['exam_date']).dt.strftime('%Y-%m-%d')

        # Sort the DataFrame by index in descending order to display the most recent uploads on top
        df = df.sort_index(ascending=False)

        st.table(df)
    else:
        st.write("No exams scheduled for selected department and semester.")

def main():
    st.set_page_config(layout="wide")

    # Hide Streamlit main menu and footer
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    collection = connect_to_mongodb()  # Get MongoDB collection

    filter_schedule(collection)

if __name__ == "__main__":
    main()
