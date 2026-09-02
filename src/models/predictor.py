import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "output_data"

FORECAST_HORIZON_UNITS = 5 
TRAIN_SPLIT_RATIO = 0.7 
N_ESTIMATORS = 50
RANDOM_STATE = 42
RISK_THRESHOLD_RATIO = 1.25 
BASELINE_SETTLE_PARTS = 60   

REQUIRED_COLUMNS = {"Part_ID", "Station_ID", "Station_Num", "Inferred_Time", "Rolling_Avg"}


def run_pred(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"predictor.run_pred: missing required columns: {sorted(missing)}")
    if df.empty:
        raise ValueError("predictor.run_pred: received an empty DataFrame")

    df = df.sort_values(["Part_ID", "Station_Num"]).reset_index(drop=True)

    df["Target_Time"] = df.groupby("Station_ID")["Inferred_Time"].shift(-FORECAST_HORIZON_UNITS)

    df["Upstream_Cycle_Time"] = (
        df.groupby("Part_ID")["Inferred_Time"].shift(1).fillna(df["Inferred_Time"])
    )
    df["Upstream_Rolling_Avg"] = (
        df.groupby("Part_ID")["Rolling_Avg"].shift(1).fillna(df["Rolling_Avg"])
    )
    df["Upstream_Drift"] = df["Upstream_Cycle_Time"] - df["Upstream_Rolling_Avg"]

    split_index = int(df["Part_ID"].max() * TRAIN_SPLIT_RATIO)
    valid_data = df.dropna(subset=["Target_Time"])
    if valid_data.empty:
        raise ValueError(
            "predictor.run_pred: no rows survived the target shift — "
            "is there enough data per station?"
        )

    train_df = valid_data[valid_data["Part_ID"] <= split_index]
    test_df = valid_data[valid_data["Part_ID"] > split_index]
    if train_df.empty or test_df.empty:
        raise ValueError(
            "predictor.run_pred: chronological split produced an empty train "
            f"or test set (split_index={split_index}). Check TRAIN_SPLIT_RATIO "
            "and the number of simulated parts."
        )

    features = ["Part_ID", "Inferred_Time", "Rolling_Avg", "Upstream_Cycle_Time", "Upstream_Drift"]
    X_train, y_train = train_df[features], train_df["Target_Time"]
    X_test, y_test = test_df[features], test_df["Target_Time"]

    model = GradientBoostingRegressor(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    test_predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, test_predictions)
    logger.info("Model validated on held-out test set. MAE: %.2f minutes", mae)

    df["Predicted_Time"] = np.round(model.predict(df[features]), 2)

    # 6. Risk scoring against a STABLE per-station baseline (see module
    #    docstring). Fall back to Rolling_Avg for any station with no data
    #    in the settle window, so risk scoring never silently goes to zero.
    settled = df[df["Part_ID"] <= BASELINE_SETTLE_PARTS]
    baseline_by_station = settled.groupby("Station_ID")["Inferred_Time"].mean()
    df["Baseline_Time"] = df["Station_ID"].map(baseline_by_station)
    df["Baseline_Time"] = df["Baseline_Time"].fillna(df["Rolling_Avg"])

    df["Risk_Score"] = np.where(
        df["Predicted_Time"] > (df["Baseline_Time"] * RISK_THRESHOLD_RATIO), 1, 0
    )

    return df


if __name__ == "__main__":
    in_path = DATA_DIR / "inferred.csv"
    out_path = DATA_DIR / "predictions.csv"
    try:
        raw = pd.read_csv(in_path)
        result = run_pred(raw)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(out_path, index=False)
        logger.info("Wrote predictions to %s", out_path)
    except FileNotFoundError:
        logger.error("Could not find %s — run soft_sensor.py first.", in_path)
        raise
    except Exception:
        logger.exception("predictor.py failed")
        raise
