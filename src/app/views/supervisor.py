import streamlit as st
import pandas as pd
import altair as alt

def show():
    st.header("Real-Time Operations")
    
    try:
        df = pd.read_csv("predictions.csv")
        
        latest_part = df['Part_ID'].max()
        curr_state = df[df['Part_ID'] == latest_part]
        
        risks = curr_state[curr_state['Risk_Score'] == 1]
        
        if not risks.empty:
            st.error("ACTION REQUIRED: Downstream Ripple Detected")
            for _, row in risks.iterrows():
                st.warning(f"Prescription: Throttle {row['Station_ID']} speed by 5%. Predicted cycle {row['Predicted_Time']}m exceeds normal {round(row['Rolling_Avg'], 2)}m.")
        else:
            st.success("Line running optimally.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            chart = alt.Chart(curr_state).mark_rect().encode(
                x='Station_ID:O',
                color=alt.condition(
                    alt.datum.Risk_Score == 1,
                    alt.value('red'),
                    alt.value('green')
                ),
                tooltip=['Station_ID', 'Inferred_Time', 'Predicted_Time']
            ).properties(height=200)
            st.altair_chart(chart, use_container_width=True)
        
        with col2:
            st.dataframe(curr_state[['Station_ID', 'Inferred_Time', 'Risk_Score']].reset_index(drop=True))
            
    except:
        st.write("run data pipeline first")
        