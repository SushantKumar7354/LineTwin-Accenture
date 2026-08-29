"""Plant Manager — ROI dashboard.

Executive-facing: throughput, OEE-proxy cycle time, bottlenecks
prevented, sensor coverage, and the financial-impact case.
"""
import altair as alt
import streamlit as st

from src.app import components

ACCENT = "#A100FF"

ALT_THEME = {
    "config": {
        "background": "transparent",
        "axis": {
            "labelColor": ACCENT,
            "titleColor": ACCENT,
            "gridColor": "rgba(161,0,255,0.15)",
            "domainColor": ACCENT,
            "labelFont": "Courier New",
            "titleFont": "Courier New",
        },
        "legend": {"labelColor": ACCENT, "titleColor": ACCENT, "labelFont": "Courier New"},
        "view": {"stroke": "transparent"},
    }
}


def show(df):
    st.markdown("### Plant Manager — ROI Dashboard")
    st.caption("Line-wide throughput, prevented bottlenecks, and estimated savings.")

    total_parts = int(df["Part_ID"].nunique())
    avg_cycle = df["Inferred_Time"].mean()
    bottlenecks_prevented = int(df["Risk_Score"].sum())
    savings = bottlenecks_prevented * 1500

    stations = df.drop_duplicates("Station_ID")
    dark_count = int((stations["Coverage"] == "Dark").sum())
    coverage_pct = round(100 * (1 - dark_count / len(stations)))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        components.kpi_card("Total throughput", f"{total_parts} parts")
    with c2:
        components.kpi_card("Avg cycle time", f"{avg_cycle:.2f} min")
    with c3:
        components.kpi_card("Bottlenecks prevented", bottlenecks_prevented, tone="ok")
    with c4:
        components.kpi_card("Est. savings", f"${savings:,}", tone="ok")

    st.write("")
    left, right = st.columns([2, 1])

    with left:
        st.markdown("#### Historical Cycle-Time Trend")
        trend = (
            alt.Chart(df)
            .mark_line(opacity=0.55, strokeWidth=1.2, color=ACCENT)
            .encode(
                x=alt.X("Part_ID:Q", title="Part"),
                y=alt.Y("Inferred_Time:Q", title="Cycle time (min)"),
                detail="Station_ID:N",
                tooltip=["Station_ID", "Part_ID", "Inferred_Time"],
            )
            .properties(height=290)
        )
        st.altair_chart(trend.properties(**ALT_THEME), width='stretch')

    with right:
        st.markdown("#### Sensor Coverage")
        components.kpi_card("Live coverage", f"{coverage_pct}%", tone="warn" if coverage_pct < 100 else "ok")
        st.write("")
        cov = stations["Coverage"].value_counts().reset_index()
        cov.columns = ["Coverage", "Stations"]
        donut = (
            alt.Chart(cov)
            .mark_arc(innerRadius=55, cornerRadius=3, padAngle=0.02, stroke=ACCENT, strokeWidth=1.5)
            .encode(
                theta="Stations:Q",
                color=alt.Color(
                    "Coverage:N",
                    scale=alt.Scale(
                        domain=["Instrumented", "Dark"], range=[ACCENT, "#FFFFFF"]
                    ),
                    legend=alt.Legend(orient="bottom", title=None),
                ),
                tooltip=["Coverage", "Stations"],
            )
            .properties(height=220)
        )
        st.altair_chart(donut.properties(**ALT_THEME), width='stretch')

    st.write("")
    st.info(
        f"💰 **Financial impact** — preventing {bottlenecks_prevented} predicted "
        f"bottleneck{'s' if bottlenecks_prevented != 1 else ''} before they cascade "
        f"avoids an estimated **${savings:,}** in downstream rework costs, based on "
        f"the {dark_count} legacy stations LineTwin recovers visibility on."
    )
