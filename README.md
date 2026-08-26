# LineTwin - Accenture Innovation Challenge 2026

**Team NinjaCoder:** Meet Kumar Gupta & Sushant Kumar  
**Track:** AI Reinvention Made Real

## Overview
LineTwin is a spatiotemporal digital twin designed to predict and prevent assembly line bottlenecks in mixed modern/legacy manufacturing environments. It uses soft-sensor inference to fill "dark data" gaps and a graph-based ML engine to issue prescriptive alerts.

🎬 **[Watch our 3-Minute Demo Video Here] ()**

## Architecture
1. **Simulation Engine (`src/data/`)**: Generates realistic 35-station telemetry and injects multi-causal bottlenecks.
2. **Predictive Engine (`src/models/`)**: Infers missing legacy data and predicts downstream ripples using Gradient Boosting on a directed graph.
3. **Multi-Persona UI (`src/app/`)**: Streamlit dashboards tailored for Floor Supervisors and Plant Managers.

## Local Setup

### 1. Install Dependencies
```bash
git clone [https://github.com/YourUsername/LineTwin-Accenture.git](https://github.com/YourUsername/LineTwin-Accenture.git)
cd LineTwin-Accenture
pip install -r requirements.txt
