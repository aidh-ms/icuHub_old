
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from db import mimic


st.set_page_config(
    layout="wide", page_title="ICU Data Viewer", page_icon="📈")


@st.cache_data
def load_vitals_data(stay_id: int = 34422196):
    """Load data from db"""
    data: pd.DataFrame = mimic.get_vitalsign(stay_id=stay_id)
    data = data.drop(columns=["subject_id", "stay_id"])
    data["charttime"] = pd.to_datetime(data["charttime"])
    data = data.set_index("charttime")
    data.sort_index(inplace=True)
    return data


@st.cache_data
def load_ventilation_data(stay_id: int = 34422196):
    """Load data on ventilation from db"""
    data: pd.DataFrame = mimic.get_ventilator_setting(stay_id=stay_id)
    data = data.drop(columns=["subject_id", "stay_id"])
    data["charttime"] = pd.to_datetime(data["charttime"])
    data = data.set_index("charttime")
    data.sort_index(inplace=True)
    return data


@st.cache_data
def load_stay_data(stay_id: int = 34422196):
    """Load data on stay from db"""
    data: pd.DataFrame = mimic.get_stay(stay_id=stay_id)
    return data


st.title("Patient Dashboard")


stay_data: pd.DataFrame = load_stay_data()
vitals_data: pd.DataFrame = load_vitals_data()
ventilation_data: pd.DataFrame = load_ventilation_data()


st.write("## Patient Information")
st.write(stay_data)


# vital parameters
fig_vitals = go.Figure()

fig_vitals.add_trace(go.Scatter(x=vitals_data.index, y=vitals_data["heart_rate"], mode="markers+lines", name="Heart Rate", line={"color": "green"}))
fig_vitals.add_trace(go.Scatter(x=vitals_data.index, y=vitals_data["spo2"], mode="markers+lines", name="SpO2", line={"color": "blue"}))
fig_vitals.add_trace(go.Scatter(x=vitals_data.index, y=vitals_data["sbp"], mode="markers+lines", name="Systolic BP", line={"color": "red"}))
fig_vitals.add_trace(go.Scatter(x=vitals_data.index, y=vitals_data["dbp"], mode="markers+lines", name="Diastolic BP", line={"color": "red"}))
fig_vitals.add_trace(go.Scatter(x=vitals_data.index, y=vitals_data["mbp"], mode="markers+lines", name="Mean BP", line={"color": "red"}))

st.write("## Vital Parameters")
if st.checkbox("Show raw vitals data"):
    st.write(vitals_data)
st.plotly_chart(fig_vitals, use_container_width=True)


### RESPIRATORY AND VENTILATION PARAMETERS ###
fig_resp = go.Figure()

fig_resp.add_trace(go.Scatter(x=vitals_data.index, y=vitals_data["resp_rate"], mode="markers+lines", name="Respiratory Rate", line={"color": "green"}))
fig_resp.add_trace(go.Scatter(x=vitals_data.index, y=vitals_data["spo2"], mode="markers+lines", name="SpO2", line={"color": "blue"}))
fig_resp.add_trace(go.Scatter(x=ventilation_data.index, y=ventilation_data["fio2"], mode="markers+lines", name="FiO2", line={"color": "lightblue"}))
st.write("## Respiratory Parameters")
st.plotly_chart(fig_resp, use_container_width=True)

# Ventilation
st.write("#### Ventilation Parameters")
if st.checkbox("Show raw ventilation data"):
    st.write(ventilation_data)

vent_tab1, vent_tab2 = st.tabs(["Pressure", "Volume"])

with vent_tab1:
    fig_vent1 = go.Figure()

    fig_vent1.add_trace(go.Scatter(x=ventilation_data.index, y=ventilation_data["peep"], mode="markers+lines", name="PEEP", line={"color": "green"}))
    fig_vent1.add_trace(go.Scatter(x=ventilation_data.index, y=ventilation_data["plateau_pressure"], mode="markers+lines", name="PIP", line={"color": "blue"}))
    fig_vent1.add_trace(go.Scatter(x=ventilation_data.index, y=ventilation_data["minute_volume"], mode="markers+lines", name="Minute Volume", line={"color": "red"}))

    st.plotly_chart(fig_vent1, use_container_width=True)

with vent_tab2:
    fig_vent2 = go.Figure()

    fig_vent2.add_trace(go.Scatter(x=ventilation_data.index, y=ventilation_data["tidal_volume_observed"], mode="markers+lines", name="Tidal Volume Observed", line={"color": "green"}))
    fig_vent2.add_trace(go.Scatter(x=ventilation_data.index, y=ventilation_data["tidal_volume_spontaneous"], mode="markers+lines", name="Tidal Volume Spontaneous", line={"color": "lightgreen"}))
    st.plotly_chart(fig_vent2, use_container_width=True)

### KIDNEY FUNCTION ###