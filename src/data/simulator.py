import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "output_data"

def generate_baseline(num_stations=35, num_parts=200):
    random.seed(42)
    simulation_results = []
    start_time = datetime(2026, 9, 1, 8, 0, 0)
    
    for part_index in range(1, num_parts + 1):
        current_time = start_time + timedelta(minutes=part_index * 2)
        for station_index in range(1, num_stations + 1):
            
           
            if station_index <= 12:
                base_cycle = 2.0 
            elif station_index <= 24:
                base_cycle = 4.5 
            else:
                base_cycle = 3.0 
                
            cycle_time = base_cycle + random.gauss(0, base_cycle * 0.05)
            current_time += timedelta(minutes=cycle_time)
            
            is_legacy = (10 <= station_index <= 15) or (25 <= station_index <= 30)
            recorded_time = None if is_legacy else round(cycle_time, 2)
            coverage_type = "Dark" if is_legacy else "Instrumented"
            
            simulation_results.append({
                "Part_ID": part_index,
                "Station_Num": station_index,
                "Station_ID": f"ST-{station_index}",
                "Timestamp": current_time,
                "Cycle_Time": recorded_time,
                "Coverage": coverage_type
            })
            
    return pd.DataFrame(simulation_results)

if __name__ == "__main__":
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        df_baseline = generate_baseline()
        out_path = DATA_DIR / "baseline.csv"
        df_baseline.to_csv(out_path, index=False)
        print(f"Generated {out_path}")
    except Exception as e:
        print(f"Error in simulator.py: {e}")