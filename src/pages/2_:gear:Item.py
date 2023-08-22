import logging
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from db import mimic
from logger import CustomLogger


st.set_page_config(
    layout="wide", page_title="ICU Data Viewer", page_icon=":gear:")

st.session_state["current_item"] = 220045
st.session_state["current_schema"] = "mimiciv_icu"


@st.cache_data
def load_item_data(item_id: int = 220045, schema: str = "mimiciv_icu"):
    """Load data from db"""
    data: pd.DataFrame = mimic.get_item(item_id=item_id, schema=schema)
    data["charttime"] = pd.to_datetime(data["charttime"])
    data = data.set_index("charttime")
    data.sort_index(inplace=True)
    return data


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
        st.session_state["current_item"] = st.number_input("Item ID", min_value=0, max_value=99999999, value=220045)
        st.session_state["current_schema"] = st.selectbox("Schema", ["mimiciv_icu", "mimiciv_hosp", "eicu"])

        table = st.selectbox("Table", tables[st.session_state["current_schema"]])
        submitted = st.form_submit_button("Search")
        if submitted:
            pass

item_data: pd.DataFrame = load_item_data(st.session_state["current_item"], st.session_state["current_schema"])

st.markdown("## Overview")

# histogram of values
fig_hist = go.Figure()

fig_hist.add_trace(go.Histogram(
    x=item_data["value"],
    name="Value",
    marker_color="#EB89B5",
    opacity=0.75,
    xbins=dict(
        start=0,
        end=300,
        size=10
    )
))
st.plotly_chart(fig_hist, use_container_width=True)

all_stay_ids = st.session_state["patient_stays"]["stay_id"].unique()
item_stay_ids = item_data["stay_id"].unique()
fraction_of_stays_with_item = len(item_stay_ids) / len(all_stay_ids)
st.write(f"Fraction of stays with item: {fraction_of_stays_with_item:.2%}")
