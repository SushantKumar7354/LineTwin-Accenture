# LineTwin: Spatiotemporal Digital Twin for Assembly Lines
**Team:** NinjaCoder (Meet Kumar Gupta, Sushant Kumar)
**Accenture Innovation Challenge 2026 - Round 2**

## 1. Problem Framing
Modern assembly lines are a patchwork of legacy and modern equipment. A micro-delay at a single station cascades downstream, culminating in significant rework costs before end-of-line testing catches it. Supervisors lack visibility into these "dark data" blind spots and react to bottlenecks rather than preventing them. 

## 2. Solution Design
LineTwin is a spatiotemporal digital twin that predicts cycle-time drift before it impacts output. 
*   **Soft-Sensor Inference:** Calculates missing telemetry for legacy stations using upstream and downstream buffer delta times, eliminating the need for expensive hardware retrofits.
*   **Spatiotemporal Graph Model:** Maps relational dependencies across the line to forecast downstream defect risks and ripple effects 15-30 minutes in advance.
*   **Prescriptive Alerts:** Outputs actionable instructions (e.g., "Throttle Station X by 5%") instead of passive alarms.

## 3. Target Users
*   **Floor Supervisor:** Requires real-time, in-the-moment signals and prescriptive actions to maintain line balance and clear imminent bottlenecks.
*   **Plant Manager:** Requires weekly planning trends, Overall Equipment Effectiveness (OEE) metrics, and historical bottleneck analysis.
*   **Leadership:** Requires a scalable business case proving ROI through avoided rework and increased throughput.

## 4. Real-World Complexities Addressed
*   **Uneven Sensor Coverage:** Solved via soft-sensor state estimation (zero-retrofit).
*   **Multi-Causal Bottlenecks:** Addressed by the Graph/ML engine which tracks upstream material flow variations alongside local station times.
*   **Operational Risk:** No PLC logic modification required; LineTwin acts as an external advisory overlay.

## 5. Business Case & ROI
*   **Capital Efficient:** Avoids multi-million dollar sensor retrofits.
*   **Cost Savings:** Preventing just 10 entrenched defects per shift (at $1,500/unit rework cost) saves $15,000 daily per line.
*   **Scalability:** The graph-based architecture easily adapts to varying line layouts and sensor maturities across different plants.

## 6. Phased Roadmap
*   **Phase 1 (Months 1-2):** Deploy soft-sensors and map the baseline spatiotemporal graph on a single high-risk line.
*   **Phase 2 (Months 3-4):** Train the predictive model and launch the Floor Supervisor dashboard in shadow mode.
*   **Phase 3 (Months 5-6):** Activate prescriptive alerts and begin scaling to adjacent lines.

## 7. Key Risks & Mitigations
*   **Risk:** False alarms eroding floor-level trust.
*   **Mitigation:** Run the model in "shadow mode" for 30 days to validate predictions against actual end-of-line defects before exposing alerts to operators.
