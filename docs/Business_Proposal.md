# LineTwin: Business Proposal

**A Spatiotemporal Digital Twin for Assembly Lines**
Accenture Innovation Challenge 2026 — Round 2 | Track: AI Reinvention Made Real
Team NinjaCoder — Meet Kumar Gupta & Sushant Kumar, IIT Patna

---

## Executive Summary

LineTwin is a software-only digital twin that predicts assembly-line bottlenecks before they cause rework — including at "dark" legacy stations with no direct sensors. Rather than requiring a multi-million-dollar IoT retrofit, it infers missing station data from timestamp deltas and models how a delay at one station propagates to the next. In our validated prototype, a controlled delay injected at one station is correctly detected cascading through two additional unsensored downstream stations, with the model's risk predictions confirmed on a chronologically held-out test set (MAE ≈ 0.13 minutes). We're proposing a phased, single-line pilot to validate this against real production data.

## 1. Problem Framing

Modern assembly lines are a patchwork of legacy and modern equipment. A micro-delay or early defect at a single station cascades downstream, compounding into significant rework cost long before end-of-line inspection catches it. Two structural issues make this hard to fix today:

- **The Dark Data Problem.** Legacy manual stations have no real-time sensors. Supervisors can't act on what they can't see, so blind spots persist even on lines with heavy investment in modern equipment elsewhere.
- **The Capability Gap.** Existing dashboards show isolated, per-station status — not the relational dependencies between stations. Operators end up reacting to a bottleneck after it's already caused downstream damage, instead of preventing it.

## 2. Solution Design

LineTwin is a spatiotemporal digital twin that predicts cycle-time drift before it impacts output, built in three layers:

- **Soft-Sensor Inference** — Estimates a station's processing time from the time delta between it and its upstream neighbor, filling dark-station blind spots without any hardware retrofit.
- **Upstream-Aware Predictive Model** — A gradient-boosted model trained on each station's own cycle-time history *and* its immediate upstream neighbor's drift, so a slowdown at one station is reflected in the risk score of the next — not just flagged in isolation.
- **Prescriptive Alerts** — Outputs plain-language, actionable recommendations (e.g., throttle a specific station's speed by a data-driven percentage) instead of a passive alarm the operator still has to interpret.

### Validated in the Current Prototype

We tested this end-to-end by injecting a controlled anomaly at one station and tracking what the system actually predicts downstream — not a projection, a measured result from the current build:

| Station | Sensor Coverage | Baseline Cycle Time | During Injected Anomaly | Risk Flagged |
|---|---|---|---|---|
| Origin station | Instrumented | 1.99 min | 5.99 min | Yes |
| +1 downstream | Instrumented | 2.00 min | 4.42 min | Yes |
| +2 downstream | **Dark (soft-sensed)** | 2.01 min | 3.55 min | Yes |
| +3 downstream | **Dark (soft-sensed)** | 1.99 min | 2.96 min | Yes |
| +4 downstream | Instrumented | 2.00 min | 2.05 min | No — correctly dissipates |

The two "Dark" rows are the core technical claim: LineTwin catches the ripple at stations that have **no direct sensor reading at all**, purely through soft-sensor inference. The effect also correctly decays to nothing four stations downstream, matching physical intuition rather than over-flagging indefinitely.

## 3. Multi-Stakeholder Value

| Stakeholder | Need | What LineTwin Delivers |
|---|---|---|
| **Floor Supervisor** | Real-time, in-the-moment signal to act on | Live risk alerts with a specific, prescriptive action per station |
| **Plant Manager** | Trend visibility for shift and weekly planning | Average cycle time, sensor coverage confidence, and flagged-bottleneck history |
| **Leadership** | A scalable business case with clear ROI | Capital-light deployment model with a quantified savings estimate (below) |

## 4. Real-World Complexities Addressed

- **Uneven Sensor Coverage** — Solved via soft-sensor state estimation; no retrofit required on legacy stations.
- **Multi-Causal Bottlenecks** — The upstream-aware model tracks material-flow drift from the preceding station alongside each station's own local history, rather than scoring stations in isolation.
- **Operational Risk** — LineTwin is a read-only advisory overlay. It does not modify PLC logic or line-control systems, which keeps integration risk and validation overhead low.

## 5. Competitive Differentiation

| | Status Quo Dashboards | Full IoT Retrofit | LineTwin |
|---|---|---|---|
| Sees relational dependencies between stations | No | Depends on analytics layer | Yes |
| Covers legacy/unsensored stations | No | Only after retrofit | Yes, via soft sensors |
| Capital required | Low, but low value | High (new sensors + wiring per station) | Low — software only |
| Output | Passive alarms | Raw telemetry | Prescriptive, plain-language actions |

## 6. Business Case & ROI

- **Cost avoidance basis:** mitigating 10 entrenched defects per shift, at an estimated $1,500 in rework cost per unit, avoids **$15,000 per line per day**.
- **Illustrative annualized impact:** at ~250 production days/year, that basis extrapolates to **~$3.75M per line per year** in avoided rework cost — a figure to validate against real defect and rework data during the Phase 1 pilot below, not a guaranteed figure.
- **Capital efficiency:** because dark stations are handled via soft sensors, LineTwin avoids the per-station hardware and wiring cost of a full sensor retrofit, which is typically the largest line item in a traditional Industry 4.0 rollout.
- **Scalability:** the same modeling approach adapts to different line lengths and sensor maturities across plants without re-architecting the system per site.

## 7. Phased Rollout Roadmap

- **Phase 1 (Months 1–2) — Baseline.** Deploy soft sensors and map the baseline spatiotemporal model on a single high-risk line, using real historical defect data to calibrate against the current prototype's synthetic-data assumptions.
- **Phase 2 (Months 3–4) — Shadow Mode.** Train the predictive model on live data and run the Floor Supervisor dashboard in shadow mode — visible to supervisors, but not yet the system of record — to build trust and measure false-alarm rate before go-live.
- **Phase 3 (Months 5–6) — Activate & Scale.** Turn on prescriptive alerts for the pilot line, then begin extending to adjacent lines using the lessons and calibration from Phase 1–2.

## 8. Key Risks & Mitigations

| Risk | Mitigation |
|---|---|
| False alarms erode floor-level trust in the system | Run in shadow mode for 30 days, validating predictions against actual end-of-line defects before exposing alerts to operators |
| Real plant data behaves differently than the synthetic prototype data | Phase 1 is explicitly a calibration phase against real historical defect records before any prescriptive action goes live |
| Soft-sensor inference is less precise than a direct sensor reading | Combine with the existing 5-reading rolling average per station to smooth noise, and prioritize instrumenting the highest-value dark stations over time |
| Supervisor workflow disruption during rollout | Advisory-only overlay in Phase 1–2 — no changes to existing controls or required workflow until Phase 3 |

## 9. Success Metrics

- Reduction in end-of-line defects traced back to a station-level delay LineTwin flagged in advance
- False-positive rate of prescriptive alerts during shadow mode
- Time-to-detection: minutes between an upstream delay occurring and a downstream risk flag being raised
- Supervisor adoption rate of prescriptive recommendations once alerts go live

## 10. The Ask

We're seeking Round 2 evaluation and progression to the final stage, with a path to a Phase 1 pilot on a single production line to validate the ROI model above against real plant data.

---
*Team NinjaCoder — Meet Kumar Gupta (Systems & AI Architecture) & Sushant Kumar (Data & Model Engineering), IIT Patna*
