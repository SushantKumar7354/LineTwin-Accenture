import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500;600;700&display=swap');

:root {
    --lt-accent: #A100FF;
    --lt-accent-08: rgba(161,0,255,0.10);
    --lt-accent-15: rgba(161,0,255,0.18);
    --lt-accent-30: rgba(161,0,255,0.42);
    --lt-bg: #111117;
    --lt-panel: #1B1B24;
    --lt-white: #FFFFFF;
    --lt-text: #F3F0F7;
    --lt-muted: rgba(243,240,247,0.66);
}

.stApp { background: var(--lt-bg); color: var(--lt-text); font-family: 'Courier New', Courier, monospace !important; }
.stApp button, .stApp label, .stApp [data-testid="stWidgetLabel"] p {
    font-family: 'Courier New', Courier, monospace !important;
}
section[data-testid="stSidebar"] { background: var(--lt-panel); border-right: 1px solid var(--lt-accent-30); }
section[data-testid="stSidebar"] * { color: var(--lt-text) !important; font-family: 'Courier New', Courier, monospace; }
button[data-testid="stSidebarCollapseButton"],
button[data-testid="stSidebarExpandButton"] { display: none !important; }

section[data-testid="stSidebar"] button {
    background: var(--lt-accent) !important;
    border: 1px solid var(--lt-accent) !important;
    color: var(--lt-white) !important;
}
section[data-testid="stSidebar"] button:hover { background: #B52BFF !important; }

h1, h2, h3, h4,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stHeading"] h1,
[data-testid="stHeading"] h2,
[data-testid="stHeading"] h3,
[data-testid="stHeading"] h4,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4 {
    font-family: 'EB Garamond', serif !important;
    font-weight: 700 !important;
    letter-spacing: 0 !important;
    color: var(--lt-accent) !important;
}
p, li, span, label, div, caption { font-family: 'Courier New', Courier, monospace; }

hr, div[data-testid="stDivider"] { border-color: var(--lt-accent-30) !important; }

/* ---- alert / status banners ---- */
.lt-alert {
    background: var(--lt-accent);
    border: 1px solid var(--lt-accent);
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.lt-alert-title {
    color: var(--lt-white);
    font-weight: 700;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-family: 'Courier New', Courier, monospace;
}
.lt-presc {
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.86rem;
    color: var(--lt-white);
    margin-top: 6px;
    padding-left: 10px;
    border-left: 2px solid var(--lt-white);
}
.lt-ok {
    background: var(--lt-white);
    border: 1px solid var(--lt-accent);
    border-left: 4px solid var(--lt-accent);
    border-radius: 6px;
    padding: 14px 18px;
    color: var(--lt-accent);
    font-weight: 700;
    font-size: 0.92rem;
    font-family: 'Courier New', Courier, monospace;
}

/* ---- conveyor / digital twin line ---- */
.lt-conveyor-wrap {
    overflow-x: auto;
    padding: 22px 6px 30px 6px;
    border-top: 1px dashed var(--lt-accent-30);
    border-bottom: 1px dashed var(--lt-accent-30);
    margin: 12px 0 18px 0;
    background: var(--lt-bg);
}
.lt-conveyor { display: flex; align-items: center; min-width: max-content; }
.lt-station {
    width: 44px; height: 44px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--lt-accent);
    background: var(--lt-panel);
    border: 2px solid var(--lt-accent);
    position: relative;
    flex-shrink: 0;
    cursor: default;
    transition: transform 0.15s ease;
}
.lt-station:hover { transform: translateY(-2px); }
/* dark data = soft-sensor inferred: dashed outline, same purple/white palette */
.lt-station.dark { border-style: dashed; border-color: var(--lt-accent); background: var(--lt-panel); }
/* risk = solid purple fill, white text, pulsing ring */
.lt-station.risk {
    background: var(--lt-accent);
    color: var(--lt-white);
    border-color: var(--lt-accent);
    box-shadow: 0 0 0 3px var(--lt-accent-15);
    animation: lt-pulse 1.7s infinite;
}
.lt-station.dark.risk { border-style: solid; }
.lt-dot {
    position: absolute; top: -5px; right: -5px;
    width: 9px; height: 9px; border-radius: 50%;
    background: var(--lt-accent);
    border: 1.5px solid var(--lt-white);
}
.lt-station.dark .lt-dot { background: var(--lt-white); border: 1.5px solid var(--lt-accent); }
.lt-arrow { color: var(--lt-accent-30); font-size: 1.05rem; margin: 0 2px; flex-shrink: 0; }

/* ---- legend ---- */
.lt-legend { display: flex; gap: 22px; flex-wrap: wrap; font-size: 0.78rem; color: var(--lt-muted); margin-top: 2px; }
.lt-legend-item { display: flex; align-items: center; gap: 7px; }
.lt-legend-swatch { width: 12px; height: 12px; border-radius: 3px; display: inline-block; }

/* ---- badges ---- */
.lt-badge {
    display: inline-block; padding: 2px 9px; border-radius: 10px;
    font-size: 0.66rem; font-weight: 700; font-family: 'Courier New', Courier, monospace;
    text-transform: uppercase; letter-spacing: 0.03em;
    border: 1px solid var(--lt-accent);
}
.lt-badge-live { background: var(--lt-accent); color: var(--lt-white); }
.lt-badge-inferred { background: var(--lt-panel); color: var(--lt-accent); }

/* ---- kpi cards ---- */
.lt-kpi {
    background: var(--lt-white);
    border: 1px solid var(--lt-accent);
    border-radius: 10px;
    padding: 16px 18px;
    height: 100%;
}
.lt-kpi-label { color: #242129 !important; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; font-family: 'Courier New', Courier, monospace; font-weight: 700; opacity: 1 !important; }
.lt-kpi-value { font-family: 'Courier New', Courier, monospace; font-size: 1.85rem; font-weight: 700; margin-top: 4px; color: var(--lt-accent); }
.lt-kpi-description { color: #514B59 !important; font-size: 0.68rem; line-height: 1.35; margin-top: 8px; opacity: 1 !important; }
/* risk tone: inverted (filled) card to draw the eye */
.lt-kpi:has(.lt-kpi-value.risk) { background: var(--lt-accent); }
.lt-kpi-value.risk { color: var(--lt-white); }
.lt-kpi:has(.lt-kpi-value.risk) .lt-kpi-label,
.lt-kpi:has(.lt-kpi-value.risk) .lt-kpi-description { color: #FFFFFF !important; }
.lt-kpi-value.warn { color: var(--lt-accent); }
.lt-kpi-value.ok { color: var(--lt-accent); }

.lt-chart {
    background: var(--lt-panel);
    border: 1px solid var(--lt-accent-30);
    border-radius: 8px;
    padding: 14px;
}
.lt-chart table { width: 100%; border-collapse: collapse; color: var(--lt-text); }
.lt-chart th, .lt-chart td { padding: 7px 8px; border-bottom: 1px solid var(--lt-accent-15); text-align: left; }
.lt-chart th { color: var(--lt-accent); font-size: 0.72rem; text-transform: uppercase; }
.lt-detail-table { width: 100%; border-collapse: collapse; background: var(--lt-panel); }
.lt-detail-table th, .lt-detail-table td { padding: 8px 10px; border-bottom: 1px solid var(--lt-accent-15); text-align: left; }
.lt-detail-table th { color: var(--lt-accent); font-size: 0.72rem; text-transform: uppercase; }
.lt-chart svg { display: block; width: 100%; height: auto; }
.lt-svg-grid line { stroke: var(--lt-accent-15); stroke-width: 1; }
.lt-svg-line { fill: none; stroke: var(--lt-accent); stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
.lt-svg-point { fill: var(--lt-accent); }
.lt-chart svg text { fill: var(--lt-muted); font: 11px 'Courier New', Courier, monospace; }
.lt-svg-track { fill: var(--lt-accent-15); stroke: var(--lt-accent-15); }
.lt-svg-track, .lt-svg-fill, .lt-svg-dark { stroke-linecap: round; }
.lt-svg-axis { stroke: var(--lt-accent-30); stroke-width: 1; }
.lt-svg-axis-title { fill: var(--lt-muted); font: 10px 'Courier New', Courier, monospace; text-transform: uppercase; letter-spacing: 0.04em; }
.lt-svg-peak { fill: var(--lt-accent); }
.lt-svg-peak-label { fill: var(--lt-text); font: 11px 'Courier New', Courier, monospace; font-weight: 700; }
.lt-svg-fill { fill: var(--lt-accent); stroke: var(--lt-accent); }
.lt-svg-dark { fill: var(--lt-panel); stroke: var(--lt-white); }
.lt-svg-center { fill: var(--lt-accent) !important; font-size: 24px !important; font-weight: 700; }

@keyframes lt-pulse {
    0%   { box-shadow: 0 0 0 0 var(--lt-accent-30); }
    70%  { box-shadow: 0 0 0 8px rgba(161,0,255,0); }
    100% { box-shadow: 0 0 0 0 rgba(161,0,255,0); }
}
</style>
"""

LIGHT_OVERRIDES = """
<style>
:root {
    --lt-bg: #FFFFFF;
    --lt-panel: #FFFFFF;
    --lt-text: #1A1A1A;
    --lt-muted: rgba(26,26,26,0.6);
}
.stApp { background: var(--lt-bg); color: var(--lt-text); }
section[data-testid="stSidebar"] { background: var(--lt-panel); }
.lt-conveyor-wrap { background: var(--lt-bg); }
.lt-station, .lt-station.dark { background: var(--lt-panel); }
.lt-station.risk { background: var(--lt-accent); }
.lt-badge-inferred { background: var(--lt-panel); }
.lt-svg-dark { fill: #FFFFFF; stroke: #1A1A1A; }
</style>
"""


def inject(dark_mode: bool = True):
    st.markdown(CSS, unsafe_allow_html=True)
    if not dark_mode:
        st.markdown(LIGHT_OVERRIDES, unsafe_allow_html=True)
