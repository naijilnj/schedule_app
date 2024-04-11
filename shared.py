from pymongo import MongoClient
import streamlit as st

@st.cache_resource
def connect_to_mongodb():
    # Paste your MongoDB connection URI here
    uri = "mongodb+srv://naijilaji:8FS9IVijl1HjtYMZ@scheduleapp.s8rln09.mongodb.net/"
    client = MongoClient(uri)
    db = client["exam_schedule"]
    collection = db["schedule"]
    return collection
