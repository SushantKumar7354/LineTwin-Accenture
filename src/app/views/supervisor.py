import math
import streamlit as st

from src.app.utils import latest_snapshot
from src.app import components

def _is_valid_number(value):
    return value is not None and not (isinstance(value, float) and math.isnan(value))

def show(df):
    st.markdown("### Floor Supervisor — Real-Time Operations")
    st.caption("Current line state and recommended actions for active risks.")

    snap = latest_snapshot(df)
    risks = snap[snap["Risk_Score"] == 1]

    if not risks.empty:
        for _, row in risks.iterrows():
            predicted = row.get("Predicted_Time")
            # Risk_Score is computed against Baseline_Time (predictor.py), not
            # Rolling_Avg — Rolling_Avg drifts upward during a sustained
            # anomaly and can end up *higher* than Predicted_Time, which would
            # make an "exceeds the rolling average" message read backwards.
            # Baseline_Time is the stable pre-anomaly reference and is what
            # actually triggered this alert, so that's what we show.
            baseline = row.get("Baseline_Time")
            has_valid_numbers = (
                _is_valid_number(predicted) and _is_valid_number(baseline) and baseline != 0
            )
            predicted_txt = f"{predicted:.2f}m" if has_valid_numbers else "–"
            baseline_txt = f"{baseline:.2f}m" if has_valid_numbers else "–"
            if has_valid_numbers:
                drift_severity = ((predicted - baseline) / baseline) * 100
                recommended_throttle = min(15, max(2, int(drift_severity * 0.5)))
            else:
                recommended_throttle = 5

            st.markdown(
                f"""
                <div class="lt-alert">
                    <div class="lt-alert-title">Action required &mdash; {row['Station_ID']}</div>
                    <div class="lt-presc">
                        Throttle {row['Station_ID']} speed by {recommended_throttle}%. Predicted cycle time
                        {predicted_txt} exceeds its normal baseline of {baseline_txt}.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="lt-ok">&check; Line running optimally &mdash; no interventions '
            "needed right now.</div>",
            unsafe_allow_html=True,
        )

    st.write("")
    components.render_conveyor(snap)
    components.render_legend()

    st.write("")
    st.markdown("#### Station Detail")

    detail = snap[
        ["Station_ID", "Coverage", "Inferred_Time", "Predicted_Time", "Risk_Score"]
    ].reset_index(drop=True)
    detail["Source"] = detail["Coverage"].map(
        {
            "Instrumented": '<span class="lt-badge lt-badge-live">LIVE</span>',
            "Dark": '<span class="lt-badge lt-badge-inferred">INFERRED</span>',
        }
    )
    detail["Status"] = detail["Risk_Score"].map({1: "At risk", 0: "Normal"})
    detail = detail.rename(
        columns={
            "Station_ID": "Station",
            "Inferred_Time": "Cycle time (min)",
            "Predicted_Time": "Predicted next (min)",
        }
    ).drop(columns=["Coverage", "Risk_Score"])

    st.markdown(
        '<div class="lt-detail-table">'
        + detail.to_html(index=False, border=0, classes="lt-detail-table", float_format="{:.2f}".format, escape=False)
        + '</div>',
        unsafe_allow_html=True,
    )