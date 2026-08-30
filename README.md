<div align="center">

# #LineTwin#
### A Spatiotemporal Digital Twin for Assembly Lines

**Turning hidden factory blind spots into foresight — before defects happen.**

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-app-FF4B4B.svg)
![scikit--learn](https://img.shields.io/badge/model-GradientBoosting-orange.svg)
![Status](https://img.shields.io/badge/status-Round%202%20Prototype-brightgreen.svg)

**Accenture Innovation Challenge 2026 — Round 2** · Track: *AI Reinvention Made Real*
**Team NinjaCoder** — Meet Kumar Gupta & Sushant Kumar, IIT Patna

[ Watch the 3-Minute Demo Video](https://drive.google.com/file/d/17vJB6JF5hcJOp2adi3lZwweLatvdL-Fz/view?usp=sharing) · [📄 Business Proposal](docs/Business_Proposal.md)

</div>

---

## The Problem

Modern assembly lines have three blind spots that static dashboards can't see:

| Problem | Why it hurts |
|---|---|
| **The Ripple Effect** | A micro-delay or early defect at one station cascades downstream, compounding into costly rework long before end-of-line inspection catches it. |
| **The Dark Data Problem** | Real plants have uneven instrumentation — legacy manual stations have no real-time sensors, creating blind spots that break static dashboards. |
| **The Capability Gap** | Existing systems show isolated station status, not relational dependencies — forcing operators to react to bottlenecks instead of preventing them. |

Built for line supervisors and quality engineers — no data-science degree required.

## Our Solution

LineTwin models the assembly line as a connected, time-aware system instead of a set of isolated station readouts:

<hr>

`[ Plant Simulator ] ➔ [ Anomaly Injector ] ➔ [ Soft-Sensor Inference ] ➔ [ Predictive Model ] ➔ [ Multi-Persona Dashboard ]`

##  Core Architecture
1. **Sense & Infer** — Physical sensor readings are merged with soft-sensor inferred times for legacy "dark" stations using upstream-to-station temporal deltas.
2. **Model the Line** — A gradient-boosted model learns the spatiotemporal topology of the assembly line.
3. **Predict the Ripple** — LineTwin flags exactly when and where an upstream delay will bottleneck downstream stations on the next 5 units.
4. **Prescribe Action** — Supervisors get a plain-language action (e.g., "Throttle speed by 5%") instead of a passive alarm.

##  Validated Results
The prototype simulates a 35-station line and injects a physical delay shockwave at ST-8. The ML pipeline successfully tracks the decaying ripple effect across both instrumented and inferred stations:

| Station | Coverage | Baseline Cycle Time | During Anomaly |
|---|---|---|---|
| ST-8 *(origin)* | Instrumented | 1.99 min | **5.99 min** |
| ST-9 | Instrumented | 2.00 min | **4.42 min** |
| ST-10 | Dark *(soft-sensed)* | 2.01 min | **3.55 min** |
| ST-11 | Dark *(soft-sensed)* | 1.99 min | **2.96 min** |
| ST-12 | Instrumented | 2.00 min | 2.05 min (0 - ripple dies) |

*The delay decays as it travels downstream and is successfully inferred across the dark stations (ST-10, ST-11).*

##  Multi-Persona Dashboard
One dataset, three views, tailored to who's looking at the screen:
* **Digital Twin Overview** — line-wide topology and live sensor coverage stats.
* **Floor Supervisor** — real-time alerts, prescriptive actions, and current line state.
* **Plant Manager** — trend lines, sensor coverage ROI, and financial impact.

##  Tech Stack
`Python` · `Streamlit` · `pandas` · `scikit-learn (Gradient Boosting)` · `networkx`

##  Repository Structure
```text
LineTwin_NinjaCoder/
├── src/
│   ├── data/
│   │   ├── simulator.py       # Synthetic 35-station plant data generator
│   │   └── anomaly_engine.py  # Injects the anomaly + decaying downstream ripple
│   ├── models/
│   │   ├── soft_sensor.py     # Infers missing readings at Dark stations
│   │   └── predictor.py       # Upstream-aware Gradient Boosting + risk scoring
│   └── app/
│       ├── main.py            # Streamlit entry point
│       ├── utils.py           # In-memory pipeline runner (no CSVs required)
│       ├── theme.py           # App styling
│       ├── components.py      # Shared UI components
│       └── views/             # overview.py, supervisor.py, manager.py
├── docs/
│   └── Business_Proposal.md
├── requirements.txt
└── README.md
