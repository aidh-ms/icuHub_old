"""MIMIC-IV database connector module. Used to execute queries against
    the MIMIC-IV database."""

import logging
from db.Connector import SQLDBConnector
from db.key import engine
from logger import CustomLogger


logger: logging.Logger = CustomLogger().get_logger()

connector: SQLDBConnector = SQLDBConnector(engine)


def get_item_of_patient(item_id: int, stay_id: int, schema: str = "mimiciv_icu", table: str = "chartevents"):
    """Get item of patient"""
    query: str = f"""
    SELECT stay_id, charttime, value
    FROM {schema}.{table}
    WHERE itemid = {item_id}
    AND stay_id = {stay_id}
    """

    return connector.execute_query(query)


def get_vitalsign(stay_id: int):
    """Get vitalsigns of patient"""
    query: str = f"""
    SELECT *
    FROM mimiciv_derived.vitalsign
    WHERE stay_id = {stay_id}
    """

    return connector.execute_query(query)


def get_ventilator_setting(stay_id: int):
    """Get ventilation data of patient"""
    query: str = f"""
    SELECT *
    FROM mimiciv_derived.ventilator_setting
    WHERE stay_id = {stay_id}
    """

    return connector.execute_query(query)


def get_stay(stay_id: int):
    """Get stay data of patient"""
    query: str = f"""
    SELECT *
    FROM mimiciv_derived.icustay_detail
    WHERE stay_id = {stay_id}
    """

    return connector.execute_query(query)
