"""Floor Supervisor — real-time operations view.

Leads with prescriptive alerts, then the same conveyor strip filtered
to the current moment, then a station-by-station detail table that
distinguishes live readings from soft-sensor inferred ones.
"""
import streamlit as st

from src.app.utils import latest_snapshot
from src.app import components


def show(df):
    st.markdown("### Floor Supervisor — Real-Time Operations")
    st.caption("Current line state and recommended actions for active risks.")

    snap = latest_snapshot(df)
    risks = snap[snap["Risk_Score"] == 1]

    if not risks.empty:
        for _, row in risks.iterrows():
            predicted = row.get("Predicted_Time")
            rolling = row.get("Rolling_Avg")
            predicted_txt = f"{predicted:.2f}m" if predicted is not None else "–"
            rolling_txt = f"{rolling:.2f}m" if rolling is not None else "–"
            st.markdown(
                f"""
                <div class="lt-alert">
                    <div class="lt-alert-title">Action required &mdash; {row['Station_ID']}</div>
                    <div class="lt-presc">
                        Throttle {row['Station_ID']} speed by 5%. Predicted cycle time
                        {predicted_txt} exceeds its rolling average of {rolling_txt}.
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
        {"Instrumented": "Live", "Dark": "Inferred"}
    )
    detail["Status"] = detail["Risk_Score"].map({1: "At risk", 0: "Normal"})
    detail = detail.rename(
        columns={
            "Station_ID": "Station",
            "Inferred_Time": "Cycle time (min)",
            "Predicted_Time": "Predicted next (min)",
        }
    ).drop(columns=["Coverage", "Risk_Score"])

    st.dataframe(
        detail,
        width='stretch',
        hide_index=True,
        column_config={
            "Cycle time (min)": st.column_config.NumberColumn(format="%.2f"),
            "Predicted next (min)": st.column_config.NumberColumn(format="%.2f"),
        },
    )
