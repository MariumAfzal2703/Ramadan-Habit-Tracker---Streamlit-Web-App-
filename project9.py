import streamlit as st
import pandas as pd
import datetime
from PIL import Image

# Initialize session state for habit tracking
if 'habits' not in st.session_state:
    st.session_state.habits = pd.DataFrame(columns=["Date", "Fasted", "Prayed 5 Times", "Prayed Traweeh", "Read Quran", "Did Charity", "Notes"])

# Title
st.header("Project 9: build a simple web app to track your Ramadan habits")
st.title("Consistency & Growth: Your Ramadan Habit Tracker")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, width=200)

# Date selection
st.header("Select Date for Entry")
selected_date = st.date_input("Choose a date", datetime.date.today())

# Habit selection
st.header("Welcome! Let's Track Your Daily Habits")
fasted = st.checkbox("Fasted Today?")
prayed_5_times = st.checkbox("Prayed 5 Times Today?")
prayed_traweeh = st.checkbox("Prayed Traweeh?")
read_quran = st.checkbox("Read Quran Today?")
did_charity = st.checkbox("Did Charity Today?")
notes = st.text_area("Notes", "")

# Submit button
if st.button("Save Entry"):
    if selected_date in st.session_state.habits["Date"].values:
        st.warning("An entry for today already exists! Please edit or delete the existing entry.")
    else:
        new_entry = pd.DataFrame({
            "Date": [selected_date],
            "Fasted": [fasted],
            "Prayed 5 Times": [prayed_5_times],
            "Prayed Traweeh": [prayed_traweeh],
            "Read Quran": [read_quran],
            "Did Charity": [did_charity],
            "Notes": [notes]
        })
        
        st.session_state.habits = pd.concat([st.session_state.habits, new_entry], ignore_index=True)
        st.success("Entry Saved!")

# Display previous entries
st.header("Habit History")
st.dataframe(st.session_state.habits)

# Edit Entry
st.header("Edit Entry")
if not st.session_state.habits.empty:
    edit_index = st.number_input("Enter row index to edit:", min_value=0, max_value=len(st.session_state.habits)-1, step=1)
    
    if st.button("Load Entry for Editing"):
        entry = st.session_state.habits.loc[edit_index]

        fasted_edit = st.checkbox("Fasted?", entry["Fasted"])
        prayed_5_times_edit = st.checkbox("Prayed 5 Times?", entry["Prayed 5 Times"])
        prayed_traweeh_edit = st.checkbox("Prayed Traweeh?", entry["Prayed Traweeh"])
        read_quran_edit = st.checkbox("Read Quran?", entry["Read Quran"])
        did_charity_edit = st.checkbox("Did Charity?", entry["Did Charity"])
        notes_edit = st.text_area("Edit Notes", entry["Notes"])

        if st.button("Save Changes"):
            st.session_state.habits.loc[edit_index, "Fasted"] = fasted_edit
            st.session_state.habits.loc[edit_index, "Prayed 5 Times"] = prayed_5_times_edit
            st.session_state.habits.loc[edit_index, "Prayed Traweeh"] = prayed_traweeh_edit
            st.session_state.habits.loc[edit_index, "Read Quran"] = read_quran_edit
            st.session_state.habits.loc[edit_index, "Did Charity"] = did_charity_edit
            st.session_state.habits.loc[edit_index, "Notes"] = notes_edit
            st.success("Entry Updated!")

# Delete Entry
st.header("Delete Entry")
if not st.session_state.habits.empty:
    delete_index = st.number_input("Enter row index to delete:", min_value=0, max_value=len(st.session_state.habits)-1, step=1)
    if st.button("Delete Selected Entry"):
        st.session_state.habits = st.session_state.habits.drop(index=delete_index).reset_index(drop=True)
        st.success("Entry Deleted!")

# Export Data
st.header("Export Data")
csv = st.session_state.habits.to_csv(index=False).encode('utf-8')
st.download_button(label="Download CSV", data=csv, file_name="ramadan_habits.csv", mime="text/csv")
