import streamlit as st

from src.app.utils import latest_snapshot, ordered_stations
from src.app import components


def show(df):
    st.markdown("### Digital Twin — Live Line State")
    st.caption(
        "Assembly line ST-1 through ST-35, mirrored in real time from live sensors "
        "and soft-sensor-inferred readings for legacy stations."
    )

    snap = latest_snapshot(df)
    total_stations = len(ordered_stations(df))
    dark_count = int((snap["Coverage"] == "Dark").sum())
    live_count = total_stations - dark_count
    risk_count = int((snap["Risk_Score"] == 1).sum())

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        components.kpi_card("Stations on line", total_stations, description="Total stations being monitored")
    with c2:
        components.kpi_card("Live sensor coverage", live_count, tone="ok", description="Stations with direct sensor readings")
    with c3:
        components.kpi_card("Dark data (inferred)", dark_count, tone="warn", description="Stations estimated by the soft sensor")
    with c4:
        components.kpi_card(
            "Active risk alerts", risk_count, tone="risk" if risk_count else "ok",
            description="Stations currently predicted to bottleneck",
        )

    st.write("")
    components.render_conveyor(snap)
    components.render_legend()

    st.write("")
    if risk_count > 0:
        st.markdown(
            '<div class="lt-alert"><div class="lt-alert-title">Live risk detected</div>'
            "Open the <b>Floor Supervisor</b> view for the prescriptive action.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="lt-ok">&check; All stations operating within normal '
            "cycle-time bounds.</div>",
            unsafe_allow_html=True,
        )

    st.write("")
    with st.expander("How LineTwin builds this view"):
        st.markdown(
            "1. **Simulate** — synthetic cycle-time data streams from all 35 stations.\n"
            "2. **Detect dark data** — legacy stations (ST-10–15, ST-25–30) report no "
            "live sensor data.\n"
            "3. **Infer** — a soft-sensor model reconstructs missing cycle times from "
            "timestamp deltas and rolling averages.\n"
            "4. **Predict** — a graph-based model forecasts each station's next cycle "
            "time and flags bottleneck risk before it happens.\n"
            "5. **Prescribe** — the Floor Supervisor view turns each risk into a "
            "concrete corrective action."
        )
