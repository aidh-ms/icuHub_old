import openai
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from db import mimic
from llm import llm_openai
from pandasai import SmartDataframe

st.set_page_config(
    layout="wide", page_title="ICU Data Viewer", page_icon="📈")

DEFAULT_PATIENT = 30057454

st.session_state["current_patient"] = DEFAULT_PATIENT


@st.cache_data
def load_vitals_data(stay_id: int = DEFAULT_PATIENT):
    """Load data from db"""
    data: pd.DataFrame = mimic.get_vitalsign(stay_id=stay_id)
    data = data.drop(columns=["subject_id", "stay_id"])
    data["charttime"] = pd.to_datetime(data["charttime"])
    data = data.set_index("charttime")
    data.sort_index(inplace=True)
    return data


@st.cache_data
def load_ventilation_data(stay_id: int = DEFAULT_PATIENT):
    """Load data on ventilation from db"""
    data: pd.DataFrame = mimic.get_ventilator_setting(stay_id=stay_id)
    data = data.drop(columns=["subject_id", "stay_id"])
    data["charttime"] = pd.to_datetime(data["charttime"])
    data = data.set_index("charttime")
    data.sort_index(inplace=True)
    return data


@st.cache_data
def load_stay_data(stay_id: int = DEFAULT_PATIENT):
    """Load data on stay from db"""
    data: pd.DataFrame = mimic.get_stay(stay_id=stay_id)
    return data


@st.cache_data
def load_kidney_data(stay_id: int = DEFAULT_PATIENT):
    """Load kidney data from db"""
    urine_data, creatinine_data = mimic.get_kidney(stay_id=stay_id)
    creatinine_data.rename(columns={"valuenum": "creatinine"}, inplace=True)
    creatinine_data.set_index("charttime", inplace=True)
    creatinine_data.sort_index(inplace=True)
    urine_data.set_index("charttime", inplace=True)
    urine_data.sort_index(inplace=True)
    return urine_data, creatinine_data


st.title("Patient Dashboard")

stay_data: pd.DataFrame = load_stay_data(st.session_state["current_patient"])
vitals_data: pd.DataFrame = load_vitals_data(st.session_state["current_patient"])
ventilation_data: pd.DataFrame = load_ventilation_data(st.session_state["current_patient"])

vitals_data_smart = SmartDataframe(vitals_data, config={"llm": llm_openai})

### SEARCH FORM ###
with st.form(key="search_form", clear_on_submit=False):
    st.write("##### Search Patient")
    st.session_state["current_patient"] = st.number_input("Stay ID", min_value=0, max_value=99999999, value=DEFAULT_PATIENT)
    submitted = st.form_submit_button("Search")
    if submitted:
        stay_data: pd.DataFrame = load_stay_data(stay_id=st.session_state["current_patient"])
        vitals_data: pd.DataFrame = load_vitals_data(stay_id=st.session_state["current_patient"])
        ventilation_data: pd.DataFrame = load_ventilation_data(stay_id=st.session_state["current_patient"])

st.write("## Patient Information")
st.write(stay_data)


### VITAL PARAMETERS ###
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

# Ventilation
st.write("## Ventilation Parameters")
if st.checkbox("Show raw ventilation data"):
    st.write(ventilation_data)

vent_tab1, vent_tab2, vent_tab3 = st.tabs(["Respiration", "Pressure", "Volume"])

with vent_tab1:
    fig_resp = go.Figure()

    fig_resp.add_trace(go.Scatter(x=vitals_data.index, y=vitals_data["resp_rate"], mode="markers+lines", name="Respiratory Rate", line={"color": "green"}))
    fig_resp.add_trace(go.Scatter(x=vitals_data.index, y=vitals_data["spo2"], mode="markers+lines", name="SpO2", line={"color": "blue"}))
    fig_resp.add_trace(go.Scatter(x=ventilation_data.index, y=ventilation_data["fio2"], mode="markers+lines", name="FiO2", line={"color": "lightblue"}))
    st.plotly_chart(fig_resp, use_container_width=True)

with vent_tab2:
    fig_vent1 = go.Figure()

    fig_vent1.add_trace(go.Scatter(x=ventilation_data.index, y=ventilation_data["peep"], mode="markers+lines", name="PEEP", line={"color": "green"}))
    fig_vent1.add_trace(go.Scatter(x=ventilation_data.index, y=ventilation_data["plateau_pressure"], mode="markers+lines", name="PIP", line={"color": "blue"}))
    fig_vent1.add_trace(go.Scatter(x=ventilation_data.index, y=ventilation_data["minute_volume"], mode="markers+lines", name="Minute Volume", line={"color": "red"}))

    st.plotly_chart(fig_vent1, use_container_width=True)

with vent_tab3:
    fig_vent2 = go.Figure()

    fig_vent2.add_trace(go.Scatter(x=ventilation_data.index, y=ventilation_data["tidal_volume_observed"], mode="markers+lines", name="Tidal Volume Observed", line={"color": "green"}))
    fig_vent2.add_trace(go.Scatter(x=ventilation_data.index, y=ventilation_data["tidal_volume_spontaneous"], mode="markers+lines", name="Tidal Volume Spontaneous", line={"color": "lightgreen"}))
    st.plotly_chart(fig_vent2, use_container_width=True)

### KIDNEY FUNCTION ###
st.write("## Kidney Function")

urine_data, creatinine_data = load_kidney_data(st.session_state["current_patient"])

if st.checkbox("Show raw kidney function data"):
    st.write(urine_data, creatinine_data)

kidney_tab1, kidney_tab2 = st.tabs(["Urine Output", "Creatinine"])

with kidney_tab1:
    fig_urine = go.Figure()

    fig_urine.add_trace(go.Scatter(x=urine_data.index, y=urine_data["urineoutput"], mode="markers+lines", name="Urine Output", line={"color": "green"}))
    st.plotly_chart(fig_urine, use_container_width=True)
with kidney_tab2:
    fig_creatinine = go.Figure()

    fig_creatinine.add_trace(go.Scatter(x=creatinine_data.index, y=creatinine_data["creatinine"], mode="markers+lines", name="Creatinine", line={"color": "green"}))
    st.plotly_chart(fig_creatinine, use_container_width=True)

### Chat Area ###

st.write("## Chat Area")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hi, I'm your personal assistant. How can I help you today?",
    }]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
prompt = st.chat_input("Type a message...")
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = vitals_data_smart.chat(st.session_state.messages[-1]["content"])
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
