"""Plant Manager — ROI dashboard.

Executive-facing: throughput, OEE-proxy cycle time, bottlenecks
predicted, sensor coverage, and the financial-impact case.
"""
import streamlit as st

from src.app import components

ACCENT = "#A100FF"


def _trend_svg(df):
    trend = df.groupby("Part_ID")["Inferred_Time"].mean().tail(30)
    values = trend.tolist()
    minimum = min(values)
    maximum = max(values)
    spread = maximum - minimum or 1
    points = []
    for index, value in enumerate(values):
        x = 42 + index * (530 / max(len(values) - 1, 1))
        y = 176 - ((value - minimum) / spread) * 132
        points.append(f"{x:.1f},{y:.1f}")
    labels = []
    for index in (0, len(values) // 2, len(values) - 1):
        if values:
            x = 42 + index * (530 / max(len(values) - 1, 1))
            labels.append(
                f'<text x="{x:.1f}" y="205" text-anchor="middle">{trend.index[index]}</text>'
            )
    return (
        '<svg viewBox="0 0 610 225" role="img" aria-label="Historical average cycle time trend">'
        '<g class="lt-svg-grid"><line x1="42" y1="44" x2="572" y2="44" />'
        '<line x1="42" y1="110" x2="572" y2="110" /><line x1="42" y1="176" x2="572" y2="176" /></g>'
        f'<polyline class="lt-svg-line" points="{" ".join(points)}" />'
        + "".join(f'<circle class="lt-svg-point" cx="{point.split(",")[0]}" cy="{point.split(",")[1]}" r="3" />' for point in points)
        + '<text x="8" y="48">high</text><text x="8" y="180">low</text>'
        + "".join(labels)
        + '</svg>'
    )


def _coverage_svg(stations):
    counts = stations["Coverage"].value_counts()
    live = int(counts.get("Instrumented", 0))
    dark = int(counts.get("Dark", 0))
    total = max(live + dark, 1)
    live_ratio = live / total
    circumference = 2 * 3.14159265359 * 54
    live_arc = circumference * live_ratio
    dark_arc = circumference - live_arc
    return (
        '<svg viewBox="0 0 360 250" role="img" aria-label="Sensor coverage donut chart">'
        '<g transform="rotate(-90 180 105)">'
        '<circle class="lt-svg-track" cx="180" cy="105" r="54" fill="none" stroke-width="22" />'
        f'<circle class="lt-svg-fill" cx="180" cy="105" r="54" fill="none" stroke-width="22" stroke-dasharray="{live_arc:.1f} {circumference:.1f}" />'
        f'<circle class="lt-svg-dark" cx="180" cy="105" r="54" fill="none" stroke-width="22" stroke-dasharray="{dark_arc:.1f} {circumference:.1f}" stroke-dashoffset="{-live_arc:.1f}" />'
        '</g>'
        f'<text class="lt-svg-center" x="180" y="101" text-anchor="middle">{round(live_ratio * 100)}%</text>'
        '<text x="180" y="120" text-anchor="middle">LIVE COVERAGE</text>'
        '<circle class="lt-svg-fill" cx="82" cy="190" r="5" />'
        f'<text x="95" y="194">Instrumented {live}</text>'
        '<circle class="lt-svg-dark" cx="220" cy="190" r="5" />'
        f'<text x="233" y="194">Dark {dark}</text>'
        '</svg>'
    )


def show(df):
    st.markdown("### Plant Manager — ROI Dashboard")
    st.caption("Line-wide throughput, predicted bottlenecks, and estimated savings.")

    total_parts = int(df["Part_ID"].nunique())
    avg_cycle = df["Inferred_Time"].mean()
    predicted_bottlenecks = int(df["Risk_Score"].sum())
    savings = predicted_bottlenecks * 1500

    stations = df.drop_duplicates("Station_ID")
    dark_count = int((stations["Coverage"] == "Dark").sum())
    coverage_pct = round(100 * (1 - dark_count / len(stations)))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        components.kpi_card("Total throughput", f"{total_parts} parts", description="Unique parts processed across the line")
    with c2:
        components.kpi_card("Avg cycle time", f"{avg_cycle:.2f} min", description="Mean time to complete one station cycle")
    with c3:
        components.kpi_card("Predicted bottlenecks", predicted_bottlenecks, tone="ok", description="Predicted slowdowns flagged before escalation")
    with c4:
        components.kpi_card("Est. savings", f"${savings:,}", tone="ok", description="Avoided rework cost from predicted bottlenecks")

    st.write("")
    left, right = st.columns([2, 1])

    with left:
        st.markdown("#### Historical Cycle-Time Trend")
        st.markdown(f'<div class="lt-chart">{_trend_svg(df)}</div>', unsafe_allow_html=True)

    with right:
        st.markdown("#### Sensor Coverage")
        components.kpi_card("Live coverage", f"{coverage_pct}%", tone="warn" if coverage_pct < 100 else "ok", description="Stations reporting directly from live sensors")
        st.write("")
        st.markdown(f'<div class="lt-chart">{_coverage_svg(stations)}</div>', unsafe_allow_html=True)

    st.write("")
    st.info(
        f"💰 **Financial impact** — flagging {predicted_bottlenecks} predicted "
        f"bottleneck{'s' if predicted_bottlenecks != 1 else ''} early "
        f"mitigates an estimated **${savings:,}** in downstream rework costs, based on "
        f"the {dark_count} legacy stations LineTwin recovers visibility on."
    )