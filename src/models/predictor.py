import pandas as pd
import networkx as nx
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "output_data"

def build_graph(stations):
    G = nx.DiGraph()
    for i in range(len(stations)-1):
        G.add_edge(stations[i], stations[i+1])
    return G

def run_pred(df):
    stations = df['Station_ID'].unique()
    G = build_graph(stations)
    
    df['Target_Time'] = df.groupby('Station_ID')['Inferred_Time'].shift(-5)
    
    train_df = df.dropna(subset=['Target_Time'])
    
    features = ['Part_ID', 'Inferred_Time', 'Rolling_Avg']
    X_train = train_df[features]
    y_train = train_df['Target_Time']
    
    model = GradientBoostingRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    df['Predicted_Time'] = np.round(model.predict(df[features]), 2)
    df['Risk_Score'] = np.where(df['Predicted_Time'] > (df['Rolling_Avg'] * 1.3), 1, 0)
    
    return df, G

if __name__ == "__main__":
    try:
        in_path = DATA_DIR / "inferred.csv"
        df = pd.read_csv(in_path)
        df, G = run_pred(df)
        out_path = DATA_DIR / "predictions.csv"
        df.to_csv(out_path, index=False)
        print(f"Generated {out_path}")
    except Exception as e:
        print(f"Error in predictor.py: {e}")