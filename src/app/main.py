"""LineTwin — Spatiotemporal Digital Twin.

Entry point: run with `streamlit run src/app/main.py` from the repo
root. Three views, selected from the sidebar: Digital Twin Overview,
Floor Supervisor, and Plant Manager. A sidebar toggle switches between
light (Accenture purple + white) and dark theme.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st

from src.app import theme
from src.app.utils import load_predictions
from src.app.views import overview, supervisor, manager

st.set_page_config(page_title="LineTwin", layout="wide", page_icon="🏭")

with st.sidebar:
    st.markdown("## 🏭 LineTwin")
    st.caption("Spatiotemporal Digital Twin")
    st.write("")
    dark_mode = st.toggle("🌙 Dark mode", value=False, key="lt_dark_mode")
    st.write("")
    view = st.radio(
        "View",
        ["Digital Twin Overview", "Floor Supervisor", "Plant Manager"],
        label_visibility="collapsed",
    )
    st.write("")
    st.divider()
    if st.button("↻ Re-run simulation", width='stretch'):
        st.cache_data.clear()
        st.rerun()
    st.write("")
    st.caption("Accenture Innovation Challenge 2026 · Team NinjaCoder")

theme.inject("dark" if dark_mode else "light")

df = load_predictions()

if view == "Digital Twin Overview":
    overview.show(df)
elif view == "Floor Supervisor":
    supervisor.show(df)
else:
    manager.show(df)
