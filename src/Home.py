import streamlit as st


st.set_page_config(
    page_title="Hello",
    page_icon="🧊",
)

st.write("Hello, world!")
st.sidebar.success("Hello, User!")

st.markdown("## This is a header")

st.session_state["current_patient"] = 34422196
st.session_state["current_item"] = 220045
