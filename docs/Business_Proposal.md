<div align="center">
  <h1>LineTwin: Spatiotemporal Digital Twin for Assembly Lines</h1>
  <p><strong>Accenture Innovation Challenge 2026 - Round 2</strong></p>
  <p>
    <em>Team: NinjaCoder (Meet Kumar Gupta, Sushant Kumar)</em>
  </p>
</div>

<hr>

<h2>1. Problem Framing</h2>
<p>
  Modern assembly lines are a patchwork of legacy and modern equipment.
  A micro-delay at a single station cascades downstream, culminating in
  significant rework costs before end-of-line testing catches it.
  Supervisors lack visibility into these "dark data" blind spots and
  react to bottlenecks rather than preventing them.
</p>

<h2>2. Solution Design</h2>
<p>
  LineTwin is a spatiotemporal digital twin that predicts cycle-time drift
  before it impacts output.
</p>
<ul>
  <li>
    <strong>Soft-Sensor Inference:</strong>
    Estimates station processing/flow time from upstream-to-station temporal deltas, 
    filling blind spots without expensive hardware retrofits.
  </li>
  <li>
    <strong>Graph-Informed Spatiotemporal Prediction:</strong>
    Uses station topology and upstream-state features (like upstream cycle drift) 
    to forecast downstream defect risks for the next 5 incoming units.
  </li>
  <li>
    <strong>Prescriptive Alerts:</strong>
    Outputs actionable, rule-based recommendations such as
    <em>"Throttle Station X speed by 5%"</em> instead of passive alarms.
  </li>
</ul>

<h2>3. Target Users</h2>
<ul>
  <li>
    <strong>Floor Supervisor:</strong>
    Requires real-time, in-the-moment signals and prescriptive actions
    to maintain line balance and clear imminent bottlenecks.
  </li>
  <li>
    <strong>Plant Manager:</strong>
    Requires weekly planning trends, Average Cycle Time metrics, and historical 
    bottleneck analysis.
  </li>
  <li>
    <strong>Leadership:</strong>
    Requires a scalable business case proving ROI through avoided rework
    and increased throughput.
  </li>
</ul>

<h2>4. Real-World Complexities Addressed</h2>
<ul>
  <li>
    <strong>Uneven Sensor Coverage:</strong>
    Solved via soft-sensor state estimation (zero-retrofit).
  </li>
  <li>
    <strong>Multi-Causal Bottlenecks:</strong>
    Addressed by the Graph/ML engine, which tracks upstream material-flow
    variations alongside local station times.
  </li>
  <li>
    <strong>Operational Risk:</strong>
    No PLC logic modification required; LineTwin acts as an external
    advisory overlay.
  </li>
</ul>

<h2>5. Business Case &amp; ROI</h2>
<ul>
  <li>
    <strong>Capital Efficient:</strong>
    Avoids multi-million-dollar sensor retrofits.
  </li>
  <li>
    <strong>Cost Savings:</strong>
    Mitigating just 10 entrenched defects per shift
    (at $1,500 per unit in rework cost) saves $15,000 daily per line.
  </li>
  <li>
    <strong>Scalability:</strong>
    The graph-based architecture easily adapts to varying line layouts
    and sensor maturities across different plants.
  </li>
</ul>

<h2>6. Phased Roadmap</h2>
<ul>
  <li>
    <strong>Phase 1 (Months 1–2):</strong>
    Deploy soft sensors and map the baseline spatiotemporal graph on a
    single high-risk line.
  </li>
  <li>
    <strong>Phase 2 (Months 3–4):</strong>
    Train the predictive model and launch the Floor Supervisor dashboard
    in shadow mode.
  </li>
  <li>
    <strong>Phase 3 (Months 5–6):</strong>
    Activate prescriptive alerts and begin scaling to adjacent lines.
  </li>
</ul>

<h2>7. Key Risks &amp; Mitigations</h2>
<ul>
  <li>
    <strong>Risk:</strong>
    False alarms eroding floor-level trust.
  </li>
  <li>
    <strong>Mitigation:</strong>
    Run the model in "shadow mode" for 30 days to validate predictions
    against actual end-of-line defects before exposing alerts to operators.
  </li>
</ul>