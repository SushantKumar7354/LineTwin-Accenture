import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "output_data"

def infer_data(df):
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    df = df.sort_values(['Part_ID', 'Station_Num']).reset_index(drop=True)
    
   
    df['Upstream_Departure_Time'] = df.groupby('Part_ID')['Timestamp'].shift(1)
    
    df['Inferred_Time'] = df['Cycle_Time']
    missing_mask = df['Inferred_Time'].isna()
    
    inferred_deltas = (df.loc[missing_mask, 'Timestamp'] - df.loc[missing_mask, 'Upstream_Departure_Time']).dt.total_seconds() / 60.0
    df.loc[missing_mask, 'Inferred_Time'] = inferred_deltas.round(2)
            
    df['Rolling_Avg'] = df.groupby('Station_ID')['Inferred_Time'].transform(lambda x: x.rolling(5, min_periods=1).mean())
    
    return df

if __name__ == "__main__":
    try:
        in_path = DATA_DIR / "anomalous.csv"
        df = pd.read_csv(in_path)
        df = infer_data(df)
        out_path = DATA_DIR / "inferred.csv"
        df.to_csv(out_path, index=False)
        print(f"Generated {out_path}")
    except Exception as e:
        print(f"Error in soft_sensor.py: {e}")