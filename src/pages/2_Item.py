import streamlit as st

st.set_page_config(
    layout="wide", page_title="ICU Data Viewer", page_icon=":gear:")


st.session_state["current_item"] = 220045
st.session_state["current_schema"] = "mimiciv"

tables = {
    "mimiciv_icu": ["chartevents", "inputevents", "outputevents"],
    "mimiciv_hosp": ["labevents", "procedures"],
    "eicu_crd": ["intakeoutput", "infusiondrug"]
}

st.title("Item Viewer")

### SEARCH FORM ###
if st.checkbox("Show Search Form"):
    with st.form(key="search_form", clear_on_submit=False):
        st.write("##### Search Item")
        st.session_state["current_item"] = st.number_input("Item ID", min_value=0, max_value=99999999, value=34422196)
        st.session_state["current_schema"] = st.selectbox("Schema", ["mimiciv_icu", "mimiciv_hosp", "eicu"])

        table = st.selectbox("Table", tables[st.session_state["current_schema"]])
        submitted = st.form_submit_button("Search")
        if submitted:
            pass
