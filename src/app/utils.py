import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st

from src.data.simulator import generate_baseline
from src.data.anomaly_engine import inject_anomalies
from src.models.soft_sensor import infer_data
from src.models.predictor import run_pred


@st.cache_data(show_spinner="Running LineTwin pipeline (simulate -> infer -> predict)...")
def load_predictions():
   
    base = generate_baseline()
    anomalous = inject_anomalies(base)
    inferred = infer_data(anomalous)
    predictions = run_pred(inferred)
    return predictions


def station_sort_key(station_id: str) -> int:
   
    try:
        return int(str(station_id).split("-")[1])
    except (IndexError, ValueError):
        return 0


def ordered_stations(df):
    stations = df["Station_ID"].unique().tolist()
    return sorted(stations, key=station_sort_key)


def latest_snapshot(df):
   
    latest_part = df["Part_ID"].max()
    snap = df[df["Part_ID"] == latest_part].copy()
    snap["_order"] = snap["Station_ID"].map(station_sort_key)
    snap = snap.sort_values("_order").drop(columns="_order").reset_index(drop=True)
    return snap
