import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
import numpy as np
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "output_data"

def run_pred(df):
    df = df.sort_values(['Part_ID', 'Station_Num'])
    
    # 1. Target Variable (Next 5 units)
    df['Target_Time'] = df.groupby('Station_ID')['Inferred_Time'].shift(-5)
    
    # 2. Topology-Aware Features (Using pandas shift instead of a GNN)
    df['Upstream_Cycle_Time'] = df.groupby('Part_ID')['Inferred_Time'].shift(1).fillna(df['Inferred_Time'])
    df['Upstream_Rolling_Avg'] = df.groupby('Part_ID')['Rolling_Avg'].shift(1).fillna(df['Rolling_Avg'])
    df['Upstream_Drift'] = df['Upstream_Cycle_Time'] - df['Upstream_Rolling_Avg']
    
    # 3. Chronological Train/Test Split
    split_index = int(df['Part_ID'].max() * 0.7) 
    valid_data = df.dropna(subset=['Target_Time'])
    
    train_df = valid_data[valid_data['Part_ID'] <= split_index]
    test_df = valid_data[valid_data['Part_ID'] > split_index]
    
    features = ['Part_ID', 'Inferred_Time', 'Rolling_Avg', 'Upstream_Cycle_Time', 'Upstream_Drift']
    
    X_train, y_train = train_df[features], train_df['Target_Time']
    X_test, y_test = test_df[features], test_df['Target_Time']
    
    # 4. Train and Evaluate
    model = GradientBoostingRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    test_predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, test_predictions)
    print(f"Model Validated on Test Set. MAE: {mae:.2f} minutes")
    
    # 5. Predict across live dataset
    df['Predicted_Time'] = np.round(model.predict(df[features]), 2)
    df['Risk_Score'] = np.where(df['Predicted_Time'] > (df['Rolling_Avg'] * 1.25), 1, 0)
    
    return df

if __name__ == "__main__":
    try:
        in_path = DATA_DIR / "inferred.csv"
        df = pd.read_csv(in_path)
        df = run_pred(df)
        out_path = DATA_DIR / "predictions.csv"
        df.to_csv(out_path, index=False)
        print(f"Generated {out_path}")
    except Exception as e:
        print(f"Error in predictor.py: {e}")