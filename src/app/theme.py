"""LineTwin visual theme: light + dark, both Accenture-branded.

Streamlit reruns the whole script on every interaction, so switching
theme is just a Python decision (see `inject(mode)`) rather than any
client-side JS — main.py reads a sidebar toggle and calls
`theme.inject("dark")` or `theme.inject("light")` accordingly.

Light mode: palette restricted to Accenture purple (#A100FF) and white,
per brand guidelines. Every state that used to rely on a separate hue
(risk, "live", etc.) is now conveyed by fill vs. outline, solid vs.
dashed borders, and weight instead of extra colors.

Dark mode: same structure, but with a lighter purple (#C77DFF) standing
in for "live / healthy" (previously teal) and red kept for genuine
bottleneck risk, so alerts still read as urgent against a dark page.

Fonts: EB Garamond for headings/titles, Courier New for body/UI text,
in both modes. Streamlit's native dataframe/table widget is
intentionally left alone (its font isn't overridden here).

The sidebar is fixed-width and cannot be resized or collapsed, in both
modes.
"""
import streamlit as st

_LIGHT = {
    "bg": "#FFFFFF",
    "panel": "#FFFFFF",
    "text": "#1A1A1A",
    "muted": "rgba(26,26,26,0.6)",
    "accent": "#A100FF",
    "accent-08": "rgba(161,0,255,0.06)",
    "accent-15": "rgba(161,0,255,0.14)",
    "accent-30": "rgba(161,0,255,0.30)",
    "risk-bg": "#A100FF",
    "risk-text": "#FFFFFF",
    "station-bg": "#FFFFFF",
    "station-border": "#A100FF",
    "station-text": "#A100FF",
    "dot-live": "#A100FF",
    "dot-dark": "#FFFFFF",
    "dot-dark-border": "#A100FF",
    "dot-ring": "#FFFFFF",
    "border": "rgba(161,0,255,0.30)",
    "border-soft": "rgba(161,0,255,0.08)",
}

_DARK = {
    "bg": "#14181C",
    "panel": "#1B2126",
    "text": "#E8ECEF",
    "muted": "#8B98A5",
    "accent": "#C77DFF",
    "accent-08": "rgba(199,125,255,0.08)",
    "accent-15": "rgba(199,125,255,0.16)",
    "accent-30": "rgba(199,125,255,0.35)",
    "risk-bg": "#EF4444",
    "risk-text": "#FFFFFF",
    "station-bg": "#1B2126",
    "station-border": "#2A333A",
    "station-text": "#E8ECEF",
    "dot-live": "#C77DFF",
    "dot-dark": "#6B7280",
    "dot-dark-border": "#14181C",
    "dot-ring": "#14181C",
    "border": "#2A333A",
    "border-soft": "#232B31",
}

CSS_TEMPLATE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500;600;700&display=swap');

:root {{
    --lt-bg: {bg};
    --lt-panel: {panel};
    --lt-text: {text};
    --lt-muted: {muted};
    --lt-accent: {accent};
    --lt-accent-08: {accent-08};
    --lt-accent-15: {accent-15};
    --lt-accent-30: {accent-30};
    --lt-risk-bg: {risk-bg};
    --lt-risk-text: {risk-text};
    --lt-station-bg: {station-bg};
    --lt-station-border: {station-border};
    --lt-station-text: {station-text};
    --lt-dot-live: {dot-live};
    --lt-dot-dark: {dot-dark};
    --lt-dot-dark-border: {dot-dark-border};
    --lt-dot-ring: {dot-ring};
    --lt-border: {border};
    --lt-border-soft: {border-soft};
}}

.stApp {{ background: var(--lt-bg); color: var(--lt-text); font-family: 'Courier New', Courier, monospace; }}

/* ---- rigid sidebar: fixed width, no drag-resize, no collapse ---- */
section[data-testid="stSidebar"] {{
    background: var(--lt-panel);
    border-right: 1px solid var(--lt-border);
    width: 240px !important;
    min-width: 240px !important;
    max-width: 240px !important;
}}
section[data-testid="stSidebar"] * {{ color: var(--lt-text) !important; font-family: 'Courier New', Courier, monospace; }}
[data-testid="stSidebarResizeHandle"] {{ display: none !important; pointer-events: none !important; }}
[data-testid="collapsedControl"] {{ display: none !important; }}

h1, h2, h3, h4 {{
    font-family: 'EB Garamond', serif;
    font-weight: 700;
    letter-spacing: 0;
    color: var(--lt-accent);
}}
p, li, span, label, div, caption {{ font-family: 'Courier New', Courier, monospace; }}

hr, div[data-testid="stDivider"] {{ border-color: var(--lt-border) !important; }}

/* ---- alert / status banners ---- */
.lt-alert {{
    background: var(--lt-risk-bg);
    border: 1px solid var(--lt-risk-bg);
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 10px;
}}
.lt-alert-title {{
    color: var(--lt-risk-text);
    font-weight: 700;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-family: 'Courier New', Courier, monospace;
}}
.lt-presc {{
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.86rem;
    color: var(--lt-risk-text);
    margin-top: 6px;
    padding-left: 10px;
    border-left: 2px solid var(--lt-risk-text);
}}
.lt-ok {{
    background: var(--lt-panel);
    border: 1px solid var(--lt-accent);
    border-left: 4px solid var(--lt-accent);
    border-radius: 6px;
    padding: 14px 18px;
    color: var(--lt-accent);
    font-weight: 700;
    font-size: 0.92rem;
    font-family: 'Courier New', Courier, monospace;
}}

/* ---- conveyor / digital twin line ---- */
.lt-conveyor-wrap {{
    overflow-x: auto;
    padding: 22px 6px 30px 6px;
    border-top: 1px dashed var(--lt-border);
    border-bottom: 1px dashed var(--lt-border);
    margin: 12px 0 18px 0;
    background: var(--lt-bg);
}}
.lt-conveyor {{ display: flex; align-items: center; min-width: max-content; }}
.lt-station {{
    width: 44px; height: 44px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--lt-station-text);
    background: var(--lt-station-bg);
    border: 2px solid var(--lt-station-border);
    position: relative;
    flex-shrink: 0;
    cursor: default;
    transition: transform 0.15s ease;
}}
.lt-station:hover {{ transform: translateY(-2px); }}
/* dark data = soft-sensor inferred: dashed outline */
.lt-station.dark {{ border-style: dashed; }}
/* risk = filled with the risk color, pulsing ring */
.lt-station.risk {{
    background: var(--lt-risk-bg);
    color: var(--lt-risk-text);
    border-color: var(--lt-risk-bg);
    box-shadow: 0 0 0 3px var(--lt-accent-15);
    animation: lt-pulse 1.7s infinite;
}}
.lt-station.dark.risk {{ border-style: solid; }}
.lt-dot {{
    position: absolute; top: -5px; right: -5px;
    width: 9px; height: 9px; border-radius: 50%;
    background: var(--lt-dot-live);
    border: 1.5px solid var(--lt-dot-ring);
}}
.lt-station.dark .lt-dot {{ background: var(--lt-dot-dark); border: 1.5px solid var(--lt-dot-dark-border); }}
.lt-arrow {{ color: var(--lt-border); font-size: 1.05rem; margin: 0 2px; flex-shrink: 0; }}

/* ---- legend ---- */
.lt-legend {{ display: flex; gap: 22px; flex-wrap: wrap; font-size: 0.78rem; color: var(--lt-muted); margin-top: 2px; }}
.lt-legend-item {{ display: flex; align-items: center; gap: 7px; }}
.lt-legend-swatch {{ width: 12px; height: 12px; border-radius: 3px; display: inline-block; }}
.lt-legend-live {{ background: var(--lt-dot-live); }}
.lt-legend-dark {{ background: var(--lt-dot-dark); border: 1px solid var(--lt-station-border); }}
.lt-legend-risk {{ background: var(--lt-risk-bg); border-radius: 50%; }}

/* ---- badges ---- */
.lt-badge {{
    display: inline-block; padding: 2px 9px; border-radius: 10px;
    font-size: 0.66rem; font-weight: 700; font-family: 'Courier New', Courier, monospace;
    text-transform: uppercase; letter-spacing: 0.03em;
    border: 1px solid var(--lt-accent);
}}
.lt-badge-live {{ background: var(--lt-accent); color: var(--lt-bg); }}
.lt-badge-inferred {{ background: transparent; color: var(--lt-accent); }}

/* ---- kpi cards ---- */
.lt-kpi {{
    background: var(--lt-panel);
    border: 1px solid var(--lt-accent);
    border-radius: 10px;
    padding: 16px 18px;
    height: 100%;
}}
.lt-kpi-label {{ color: var(--lt-muted); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; font-family: 'Courier New', Courier, monospace; }}
.lt-kpi-value {{ font-family: 'Courier New', Courier, monospace; font-size: 1.85rem; font-weight: 700; margin-top: 4px; color: var(--lt-accent); }}
/* risk tone: inverted (filled) card to draw the eye */
.lt-kpi:has(.lt-kpi-value.risk) {{ background: var(--lt-risk-bg); border-color: var(--lt-risk-bg); }}
.lt-kpi-value.risk {{ color: var(--lt-risk-text); }}
.lt-kpi:has(.lt-kpi-value.risk) .lt-kpi-label {{ color: rgba(255,255,255,0.75); }}
.lt-kpi-value.warn {{ color: var(--lt-accent); }}
.lt-kpi-value.ok {{ color: var(--lt-accent); }}

@keyframes lt-pulse {{
    0%   {{ box-shadow: 0 0 0 0 var(--lt-accent-30); }}
    70%  {{ box-shadow: 0 0 0 8px rgba(0,0,0,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(0,0,0,0); }}
}}
</style>
"""


def inject(mode: str = "light"):
    """Inject the theme CSS for the given mode ('light' or 'dark')."""
    values = _DARK if mode == "dark" else _LIGHT
    st.markdown(CSS_TEMPLATE.format(**values), unsafe_allow_html=True)
