import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "output_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def get_base(n=35, parts=200):
    random.seed(42)
    res = []
    st = datetime(2026, 9, 1, 8, 0, 0)
    
    for i in range(1, parts + 1):
        cur = st + timedelta(minutes=i * 2)
        for j in range(1, n + 1):
            cyc = 2.0 + random.gauss(0, 0.1)
            cur += timedelta(minutes=cyc)
            
            legacy = (10 <= j <= 15) or (25 <= j <= 30)
            c_time = None if legacy else round(cyc, 2)
            cov = "Dark" if legacy else "Instrumented"
            
            res.append({
                "Part_ID": i,
                "Station_ID": f"ST-{j}",
                "Timestamp": cur,
                "Cycle_Time": c_time,
                "Coverage": cov
            })
            
    return pd.DataFrame(res)

if __name__ == "__main__":
    try:
        df = get_base()
        out_path = DATA_DIR / "baseline.csv"
        df.to_csv(out_path, index=False)
        print(f"Generated {out_path}")
    except Exception as e:
        print(f"Error in simulator.py: {e}")