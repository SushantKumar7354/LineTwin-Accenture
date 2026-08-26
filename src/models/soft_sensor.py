import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "output_data"

def infer_data(df):
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values(['Part_ID', 'Timestamp']).reset_index(drop=True)
    df['Inferred_Time'] = df['Cycle_Time']
    
    for i in range(1, len(df)):
        if pd.isna(df.loc[i, 'Cycle_Time']):
            diff = (df.loc[i, 'Timestamp'] - df.loc[i-1, 'Timestamp']).total_seconds() / 60.0
            df.loc[i, 'Inferred_Time'] = round(diff, 2)
            
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