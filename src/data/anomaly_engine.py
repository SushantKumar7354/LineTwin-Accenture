import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "output_data"

def inject_anomalies(df):
    anomalous_df = df.copy()
    
    target_station = anomalous_df["Station_ID"] == "ST-8"
    delay_condition = target_station & (anomalous_df["Part_ID"] >= 100) & (anomalous_df["Part_ID"] <= 120)
    
    anomalous_df.loc[delay_condition, "Cycle_Time"] += 4.0
    
    anomalous_df["Rework_Risk"] = 0 
    anomalous_df.loc[delay_condition, "Rework_Risk"] = 1
    
    return anomalous_df

if __name__ == "__main__":
    try:
        in_path = DATA_DIR / "baseline.csv"
        df_base = pd.read_csv(in_path)
        df_anomalous = inject_anomalies(df_base)
        out_path = DATA_DIR / "anomalous.csv"
        df_anomalous.to_csv(out_path, index=False)
        print(f"Generated {out_path}")
    except Exception as e:
        print(f"Error in anomaly_engine.py: {e}")