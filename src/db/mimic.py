"""MIMIC-IV database connector module. Used to execute queries against
    the MIMIC-IV database."""

import logging
import pandas as pd
from typing import LiteralString
from pyICU.connection.Connector import MimicConnector
from pyICU.connection.key import mimic_demo_engine
from logger import CustomLogger


logger: logging.Logger = CustomLogger().get_logger()
connector = MimicConnector(mimic_demo_engine)


def get_patient_stays():
    """Get all stays of patient"""
    query: str = """
    SELECT *
    FROM mimiciv_derived.icustay_detail
    """
    return connector.execute_query(query)


def get_item_of_patient(item_ids: tuple, stay_id: int, schema: str = "mimiciv_icu", table: str = "chartevents") -> pd.DataFrame:
    """Get item of patient"""
    query: str = f"""
    SELECT stay_id, charttime, value
    FROM {schema}.{table}
    WHERE itemid IN {item_ids}
    AND stay_id = {stay_id}
    """

    return connector.execute_query(query)


def get_item(item_id: int, schema: str = "mimiciv_icu", table: str = "chartevents") -> pd.DataFrame:
    """Get all instances of an item"""
    query: str = f"""
    SELECT stay_id, charttime, value
    FROM {schema}.{table}
    WHERE itemid = {item_id}
    """

    return connector.execute_query(query)


def get_vitalsign(stay_id: int) -> pd.DataFrame:
    """Get vitalsigns of patient"""
    query: str = f"""
    SELECT *
    FROM mimiciv_derived.vitalsign
    WHERE stay_id = {stay_id}
    """

    return connector.execute_query(query)


def get_ventilator_setting(stay_id: int) -> pd.DataFrame:
    """Get ventilation data of patient"""
    query: str = f"""
    SELECT *
    FROM mimiciv_derived.ventilator_setting
    WHERE stay_id = {stay_id}
    """

    return connector.execute_query(query)


def get_stay(stay_id: int) -> pd.DataFrame:
    """Get stay data of patient"""
    query: str = f"""
    SELECT *
    FROM mimiciv_derived.icustay_detail
    WHERE stay_id = {stay_id}
    """

    return connector.execute_query(query)


def get_kidney(stay_id: int) -> pd.DataFrame:
    """Get kidney data of patient"""
    query_urine: str = f"""
    SELECT charttime, urineoutput
    FROM mimiciv_derived.urine_output
    WHERE stay_id = {stay_id}
    """
    query_creatinine: str = f"""
    SELECT l.charttime, l.valuenum
    FROM mimiciv_hosp.labevents AS l
    INNER JOIN mimiciv_icu.icustays AS s USING(subject_id)
    WHERE l.itemid IN (50912, 52546)
    AND s.stay_id = {stay_id}
    AND l.charttime > s.intime
    AND l.charttime < s.outtime
    """

    return connector.execute_query(query_urine), connector.execute_query(query_creatinine)
