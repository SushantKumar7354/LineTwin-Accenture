import math
import streamlit as st

from src.app.utils import station_sort_key

def render_conveyor(snapshot_df):
    """Render the line as a horizontal strip of station nodes.

    Each node encodes two independent facts: whether the station is
    Instrumented (solid corner dot) or Dark / soft-sensor-inferred
    (grey corner dot, dashed border), and whether it currently carries
    a bottleneck risk (red ring + pulse).
    """
    rows = snapshot_df.copy()
    rows["_order"] = rows["Station_ID"].map(station_sort_key)
    rows = rows.sort_values("_order")
    records = rows.to_dict("records")

    html = ['<div class="lt-conveyor-wrap"><div class="lt-conveyor">']
    for i, row in enumerate(records):
        risk = " risk" if row.get("Risk_Score", 0) == 1 else ""
        dark = " dark" if row.get("Coverage") == "Dark" else ""
        num = str(row["Station_ID"]).split("-")[-1]
        inferred_time = row.get("Inferred_Time")
        has_time = inferred_time is not None and not (
            isinstance(inferred_time, float) and math.isnan(inferred_time)
        )
        time_txt = f"{inferred_time:.2f}m" if has_time else "–"
        tooltip = f"{row['Station_ID']} · {row.get('Coverage', '–')} · {time_txt} cycle"
        html.append(
            f'<div class="lt-station{risk}{dark}" title="{tooltip}">{num}'
            f'<span class="lt-dot"></span></div>'
        )
        if i < len(records) - 1:
            html.append('<span class="lt-arrow">&rarr;</span>')
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def render_legend():
    st.markdown(
        """
        <div class="lt-legend">
            <div class="lt-legend-item">
                <span class="lt-legend-swatch" style="background:var(--lt-accent);border-radius:50%;"></span>
                Instrumented (live sensor)
            </div>
            <div class="lt-legend-item">
                <span class="lt-legend-swatch" style="background:var(--lt-white);border:1px solid var(--lt-accent);"></span>
                Dark data (soft-sensor inferred)
            </div>
            <div class="lt-legend-item">
                <span class="lt-legend-swatch" style="background:var(--lt-accent);border-radius:50%;"></span>
                Bottleneck risk detected
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value, tone: str = "", description: str = ""):
    tone_class = f" {tone}" if tone else ""
    label_color = "rgba(255,255,255,0.82)" if tone == "risk" else "#4A4650"
    description_color = "rgba(255,255,255,0.78)" if tone == "risk" else "#6B6670"
    description_html = (
        f'<div class="lt-kpi-description" style="color:{description_color};">{description}</div>'
        if description else ""
    )
    st.markdown(
        f'<div class="lt-kpi"><div class="lt-kpi-label" style="color:{label_color};">{label}</div>'
        f'<div class="lt-kpi-value{tone_class}">{value}</div>{description_html}</div>',
        unsafe_allow_html=True,
    )