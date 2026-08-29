import pandas as pd

def add_anom(df):
    new_df = df.copy()
    
    mask = new_df["Station_ID"] == "ST-8"
    cond = mask & (new_df["Part_ID"] >= 100) & (new_df["Part_ID"] <= 120)
    
    new_df.loc[cond, "Cycle_Time"] += 4.0
    new_df["Rework_Risk"] = 0 
    
    return new_df

if __name__ == "__main__":
    try:
        base = pd.read_csv("baseline.csv")
        anom = add_anom(base)
        anom.to_csv("anomalous.csv", index=False)
    except Exception as e:
        pass
