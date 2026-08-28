<div align="center">
  <h1>🏭 LineTwin</h1>
  <p><b>Accenture Innovation Challenge 2026</b></p>
  <p><i>Team NinjaCoder: Meet Kumar Gupta & Sushant Kumar</i></p>
  <p>Track: AI Reinvention Made Real</p>
  <br>
  <a href="[https://youtube.com/your-unlisted-link-here](https://youtube.com/your-unlisted-link-here)"><b>🎬 Watch our 3-Minute Demo Video Here</b></a>
</div>

<hr>

## Overview
LineTwin is a spatiotemporal digital twin designed to predict and prevent assembly line bottlenecks in mixed modern/legacy manufacturing environments. It uses soft-sensor inference to fill "dark data" gaps and a graph-based ML engine to issue prescriptive alerts.

## Local Setup

### 1. Install Dependencies
```bash
git clone https://github.com/SushantKumar7354/LineTwin-Accenture.git
cd LineTwin-Accenture
pip install -r requirements.txt
```

### 2. Run the Data & ML Pipeline
Execute the pipeline sequentially to generate the simulated plant data, inject anomalies, run the soft-sensor inference, and calculate predictive risks:
```bash
python src/data/simulator.py
python src/data/anomaly_engine.py
python src/models/soft_sensor.py
python src/models/predictor.py
```

### 3. Launch the Dashboard
```bash
streamlit run src/app/main.py
```
