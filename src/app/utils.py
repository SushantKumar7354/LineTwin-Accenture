import streamlit as st
from src.data.simulator import generate_baseline
from src.data.anomaly_engine import inject_anomalies
from src.models.soft_sensor import infer_data
from src.models.predictor import run_pred

@st.cache_data(show_spinner="Running LineTwin pipeline...")
def load_predictions():
    """Run the full pipeline once per session and cache it."""
    base = generate_baseline()
    anomalous = inject_anomalies(base)
    inferred = infer_data(anomalous)
    predictions = run_pred(inferred)
    return predictions