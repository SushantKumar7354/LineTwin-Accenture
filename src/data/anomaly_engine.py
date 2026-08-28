import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "output_data"

def inject_anomalies(df):
    anomalous_df = df.copy()
    anomalous_df["Timestamp"] = pd.to_datetime(anomalous_df["Timestamp"])
    anomalous_df = anomalous_df.sort_values(["Part_ID", "Station_Num"]).reset_index(drop=True)

    part_condition = (anomalous_df["Part_ID"] >= 100) & (anomalous_df["Part_ID"] <= 120)

    primary_delay = 4.0
    decay_factors = {"ST-8": 1.0, "ST-9": 0.6, "ST-10": 0.4, "ST-11": 0.25}

    anomalous_df["Rework_Risk"] = 0
    primary_mask = (anomalous_df["Station_ID"] == "ST-8") & part_condition
    anomalous_df.loc[primary_mask, "Rework_Risk"] = 1

    anomalous_df["own_bump"] = 0.0
    for station, factor in decay_factors.items():
        mask = (anomalous_df["Station_ID"] == station) & part_condition
        anomalous_df.loc[mask, "own_bump"] = primary_delay * factor

    anomalous_df["Cycle_Time"] += anomalous_df["own_bump"]

    cumulative_delay = anomalous_df.groupby("Part_ID")["own_bump"].cumsum()
    anomalous_df["Timestamp"] += pd.to_timedelta(cumulative_delay, unit="m")

    return anomalous_df.drop(columns=["own_bump"])

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