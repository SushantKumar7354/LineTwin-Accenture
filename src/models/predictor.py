import pandas as pd
import networkx as nx
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def build_graph(stations):
    G = nx.DiGraph()
    for i in range(len(stations)-1):
        G.add_edge(stations[i], stations[i+1])
    return G

def run_pred(df):
    stations = df['Station_ID'].unique()
    G = build_graph(stations)
    
    df['Target_Time'] = df.groupby('Station_ID')['Inferred_Time'].shift(-5)
    df = df.bfill().ffill()
    
    features = ['Part_ID', 'Inferred_Time', 'Rolling_Avg']
    X = df[features]
    y = df['Target_Time']
    
    model = GradientBoostingRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    df['Predicted_Time'] = np.round(model.predict(X), 2)
    df['Risk_Score'] = np.where(df['Predicted_Time'] > (df['Rolling_Avg'] * 1.3), 1, 0)
    
    return df, G

if __name__ == "__main__":
    try:
        df = pd.read_csv("inferred.csv")
        df, G = run_pred(df)
        df.to_csv("predictions.csv", index=False)
    except Exception as e:
        pass