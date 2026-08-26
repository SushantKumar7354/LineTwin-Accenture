import pandas as pd
import networkx as nx
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
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
    df = df.sort_values(['Part_ID', 'Station_Num'])
    stations = df['Station_ID'].unique()
    G = build_graph(stations)
    
    # 1. Target Variable (Shift within the same station)
    df['Target_Time'] = df.groupby('Station_ID')['Inferred_Time'].shift(-5)
    
    # 2. Graph-Derived Feature: Inject the upstream station's rolling average
    df['Upstream_State'] = df.groupby('Part_ID')['Rolling_Avg'].shift(1).fillna(df['Rolling_Avg'])
    
    # 3. Chronological Train/Test Split (Avoid Leakage)
    split_index = int(df['Part_ID'].max() * 0.7) # Train on first 70% of shift
    valid_data = df.dropna(subset=['Target_Time'])
    
    train_df = valid_data[valid_data['Part_ID'] <= split_index]
    test_df = valid_data[valid_data['Part_ID'] > split_index]
    
    features = ['Part_ID', 'Inferred_Time', 'Rolling_Avg', 'Upstream_State']
    X_train, y_train = train_df[features], train_df['Target_Time']
    X_test, y_test = test_df[features], test_df['Target_Time']
    
    # 4. Train and Evaluate
    model = GradientBoostingRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    test_predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, test_predictions)
    print(f"Model Validated on Test Set. MAE: {mae:.2f} minutes")
    
    # 5. Predict across the live dataset
    df['Predicted_Time'] = np.round(model.predict(df[features]), 2)
    df['Risk_Score'] = np.where(df['Predicted_Time'] > (df['Rolling_Avg'] * 1.25), 1, 0)
    
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