import pandas as pd

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
        df = pd.read_csv("anomalous.csv")
        df = infer_data(df)
        df.to_csv("inferred.csv", index=False)
    except Exception as e:
        pass
