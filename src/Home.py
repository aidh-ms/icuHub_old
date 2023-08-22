import streamlit as st
from db.mimic import get_patient_stays

st.set_page_config(
    page_title="Hello",
    page_icon="🧊",
)

st.write("Hello, world!")
st.sidebar.success("Hello, User!")

st.markdown("## This is a header")

st.session_state["current_patient"] = 34422196
st.session_state["current_item"] = 220045
st.session_state["patient_stays"] = get_patient_stays()
