import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = ROOT_DIR / "output_data"

def show():
    st.header("Real-Time Operations")
    
    try:
        in_path = DATA_DIR / "predictions.csv"
        df = pd.read_csv(in_path)
        
        latest_part = df['Part_ID'].max()
        curr_state = df[df['Part_ID'] == latest_part]
        risks = curr_state[curr_state['Risk_Score'] == 1]
        
        if not risks.empty:
            st.error("ACTION REQUIRED: Downstream Ripple Detected")
            for _, row in risks.iterrows():
                # Dynamic Prescription Logic
                drift_severity = ((row['Predicted_Time'] - row['Rolling_Avg']) / row['Rolling_Avg']) * 100
                recommended_throttle = min(15, max(2, int(drift_severity * 0.5)))
                
                st.warning(f"Rule-Based Recommendation: Throttle {row['Station_ID']} speed by {recommended_throttle}%. Predicted cycle {row['Predicted_Time']}m exceeds normal {round(row['Rolling_Avg'], 2)}m.")
        else:
            st.success("Line running optimally.")
        
        st.markdown("---")
        st.subheader("Live Assembly Line Topology (Spatiotemporal Graph)")
        
        stations = curr_state['Station_ID'].tolist()
        G = nx.DiGraph()
        for i in range(len(stations)-1):
            G.add_edge(stations[i], stations[i+1])
            
        pos = {}
        for i, station in enumerate(stations):
            row = i // 10
            col = i % 10 if row % 2 == 0 else 9 - (i % 10) 
            pos[station] = (col, -row)
            
        risk_stations = risks['Station_ID'].tolist()
        node_colors = ['#ff4b4b' if node in risk_stations else '#28a745' for node in G.nodes()]
        
        fig, ax = plt.subplots(figsize=(14, 5))
        nx.draw(G, pos, with_labels=True, node_color=node_colors, 
                node_size=800, font_size=8, font_color="white", 
                font_weight="bold", edge_color="gray", ax=ax, arrows=True)
        
        ax.set_title("Red nodes indicate T+15m bottleneck prediction", fontsize=12, color="gray")
        st.pyplot(fig)
        
        st.markdown("---")
        st.subheader("Station Telemetry")
        st.dataframe(curr_state[['Station_ID', 'Coverage', 'Inferred_Time', 'Predicted_Time', 'Risk_Score']].reset_index(drop=True), use_container_width=True)
            
    except Exception as e:
        st.error(f"Error loading UI: {e}")