import streamlit as st
from src.app import components

ACCENT = "#A100FF"

def _trend_svg(df):
    trend = df.groupby("Part_ID")["Inferred_Time"].mean()
    values = trend.tolist()
    parts = trend.index.tolist()
    if not values:
        return '<svg viewBox="0 0 610 225" role="img"></svg>'

    minimum = min(values)
    maximum = max(values)
    spread = maximum - minimum or 1
    pad = spread * 0.18
    y_min = minimum - pad
    y_max = maximum + pad
    y_spread = y_max - y_min or 1

    plot_left, plot_right = 46, 572
    plot_top, plot_bottom = 20, 176
    n = len(values)

    def x_at(i):
        return plot_left + i * ((plot_right - plot_left) / max(n - 1, 1))

    def y_at(v):
        return plot_bottom - ((v - y_min) / y_spread) * (plot_bottom - plot_top)

    points = [f"{x_at(i):.1f},{y_at(v):.1f}" for i, v in enumerate(values)]

    grid_lines, y_labels = [], []
    y_ticks = 4
    for t in range(y_ticks + 1):
        frac = t / y_ticks
        val = y_min + frac * y_spread
        y = plot_bottom - frac * (plot_bottom - plot_top)
        grid_lines.append(f'<line x1="{plot_left}" y1="{y:.1f}" x2="{plot_right}" y2="{y:.1f}" />')
        y_labels.append(f'<text x="{plot_left - 8}" y="{y + 4:.1f}" text-anchor="end">{val:.1f}</text>')

    x_labels = []
    x_ticks = 4
    for t in range(x_ticks + 1):
        frac = t / x_ticks
        idx = round(frac * (n - 1))
        x = x_at(idx)
        x_labels.append(f'<text x="{x:.1f}" y="{plot_bottom + 20}" text-anchor="middle">{parts[idx]}</text>')

    peak_idx = values.index(maximum)
    peak_x, peak_y = x_at(peak_idx), y_at(maximum)

    return (
        '<svg viewBox="0 0 610 225" role="img" aria-label="Historical average cycle time trend">'
        f'<g class="lt-svg-grid">{"".join(grid_lines)}</g>'
        f'<line x1="{plot_left}" y1="{plot_top}" x2="{plot_left}" y2="{plot_bottom}" class="lt-svg-axis" />'
        f'<line x1="{plot_left}" y1="{plot_bottom}" x2="{plot_right}" y2="{plot_bottom}" class="lt-svg-axis" />'
        f'<polyline class="lt-svg-line" points="{" ".join(points)}" />'
        + "".join(f'<circle class="lt-svg-point" cx="{point.split(",")[0]}" cy="{point.split(",")[1]}" r="2.5" />' for point in points)
        + f'<circle class="lt-svg-peak" cx="{peak_x:.1f}" cy="{peak_y:.1f}" r="4" />'
        + f'<text class="lt-svg-peak-label" x="{peak_x:.1f}" y="{max(peak_y - 10, 12):.1f}" text-anchor="middle">{maximum:.2f}m</text>'
        + "".join(y_labels)
        + "".join(x_labels)
        + '<text x="8" y="14" class="lt-svg-axis-title">min</text>'
        + f'<text x="{(plot_left + plot_right) / 2:.1f}" y="218" text-anchor="middle" class="lt-svg-axis-title">Part ID</text>'
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
        f'<text x="95" y="194">Instrumented &mdash; {live}</text>'
        '<circle class="lt-svg-dark" cx="220" cy="190" r="5" />'
        f'<text x="233" y="194">Dark &mdash; {dark}</text>'
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
