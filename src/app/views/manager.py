import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = ROOT_DIR / "output_data"

def show():
    st.header("Plant Manager & ROI Dashboard")
    
    try:
        in_path = DATA_DIR / "predictions.csv"
        df = pd.read_csv(in_path)
        
        total_parts = df['Part_ID'].nunique()
        avg_cycle = df['Inferred_Time'].mean()
        rework_risks = df['Risk_Score'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Throughput", total_parts)
        col2.metric("Line OEE (Avg Cycle)", f"{round(avg_cycle, 2)} min")
        col3.metric("Bottlenecks Flagged", int(rework_risks))
        
        st.subheader("Historical Bottleneck Analysis")
        trend = alt.Chart(df).mark_line(opacity=0.3).encode(
            x='Part_ID:Q',
            y='Inferred_Time:Q',
            color='Station_ID:N'
        ).properties(height=300)
        st.altair_chart(trend, use_container_width=True)
        
        st.subheader("Sensor Coverage & Confidence")
        coverage = df.groupby('Coverage')['Station_ID'].nunique().reset_index()
        st.dataframe(coverage)
        
        savings = int(rework_risks * 1500)
        st.info(f"Financial Impact: Flagging {int(rework_risks)} bottleneck risks early helps mitigate an estimated ${savings} in downstream rework costs.")
        
    except Exception as e:
        st.error(f"Error loading UI: {e}")