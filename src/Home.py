import streamlit as st


st.set_page_config(
    page_title="Hello",
    page_icon="🧊",
)

st.write("Hello, world!")
st.sidebar.success("Hello, User!")

st.markdown("## This is a header")
