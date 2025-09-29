# scripts/train_gbm.py
"""
Train a Gradient Boosting Regressor, log to MLflow (metrics + artifacts),
and export serving artifacts used by the FastAPI service.

Artifacts produced:
- model/model.pkl
- model/model_features.json
- model/feature_importances.png
MLflow artifacts:
- model/          (MLflow's serialized sklearn model)
- artifacts/*     (model.pkl, model_features.json, feature_importances.png)
"""

from pathlib import Path
import json
import pickle
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor

import mlflow
import mlflow.sklearn


# ---- Paths & constants -------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "model"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

SALES_PATH = DATA_DIR / "kc_house_data.csv"
DEMOS_PATH = DATA_DIR / "zipcode_demographics.csv"
TARGET = "price"


def main():
    t0 = time.time()

    # ---- Load & join data ----------------------------------------------------
    sales = pd.read_csv(SALES_PATH)
    demos = pd.read_csv(DEMOS_PATH)

    # Join demographics by zipcode (server uses same logic at inference)
    df = sales.merge(demos, on="zipcode", how="left")

    # ---- Feature selection ---------------------------------------------------
    # numeric-only baseline; drop target and non-predictive 'id' if present
    num_cols = df.select_dtypes(include="number").columns.tolist()
    for drop_col in ["price", "id"]:
        if drop_col in num_cols:
            num_cols.remove(drop_col)

    X = df[num_cols]
    y = df[TARGET]

    # ---- Split ----------------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ---- Pipeline -------------------------------------------------------------
    pre = ColumnTransformer(
        transformers=[("num", StandardScaler(with_mean=False), num_cols)],
        remainder="drop",
    )

    gbm = GradientBoostingRegressor(random_state=42)
    pipe = Pipeline([("pre", pre), ("gbm", gbm)])

    # Small, fast grid (good for demo; expand later if desired)
    param_grid = {
        "gbm__n_estimators": [200, 400],
        "gbm__max_depth": [3, 4],
        "gbm__learning_rate": [0.05, 0.1],
        "gbm__subsample": [0.8, 1.0],
    }

    # ---- MLflow setup (Windows-safe) -----------------------------------------
    mlflow.set_tracking_uri((ROOT / "mlruns").as_uri())  # file:///C:/...
    mlflow.set_experiment("sound-realty-gbm")

    with mlflow.start_run(run_name="gbm-grid") as run:
        # Grid search
        gscv = GridSearchCV(
            pipe,
            param_grid=param_grid,
            cv=3,
            n_jobs=-1,
            verbose=0,
            scoring="neg_root_mean_squared_error",
        )
        gscv.fit(X_train, y_train)
        best = gscv.best_estimator_

        # Evaluate
        y_pred = best.predict(X_test)
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mae = float(mean_absolute_error(y_test, y_pred))
        r2 = float(r2_score(y_test, y_pred))

        # Log params & metrics
        mlflow.log_params(gscv.best_params_)
        mlflow.log_metrics({"rmse": rmse, "mae": mae, "r2": r2})

        # ---- Export serving artifacts (for API) ------------------------------
        with open(MODEL_DIR / "model.pkl", "wb") as f:
            pickle.dump(best, f)

        with open(MODEL_DIR / "model_features.json", "w") as f:
            json.dump(num_cols, f)

        # Feature importance (from GBM inside the pipeline)
        importances = best.named_steps["gbm"].feature_importances_
        top = sorted(zip(num_cols, importances), key=lambda x: x[1], reverse=True)[:20]
        labels, vals = zip(*top) if top else ([], [])

        plt.figure(figsize=(8, 6))
        plt.barh(range(len(vals)), vals)
        plt.yticks(range(len(labels)), labels)
        plt.gca().invert_yaxis()
        plt.title("Top Feature Importances (GBM)")
        plt.tight_layout()
        fig_path = MODEL_DIR / "feature_importances.png"
        plt.savefig(fig_path)
        plt.close()

        # ---- Log artifacts to MLflow ----------------------------------------
        # 1) Full sklearn model in MLflow format (separate from serving files)
        mlflow.sklearn.log_model(best, artifact_path="model")

        # 2) Also log the serving artifacts folder in one shot
        mlflow.log_artifacts(str(MODEL_DIR), artifact_path="artifacts")

        # after your other mlflow.log_artifacts(...)
        mlflow.log_text("hello from this run", artifact_file="hello.txt")


        # Debug prints (handy to verify UI points to same store)
        print("MLflow tracking URI:", mlflow.get_tracking_uri())
        print("Run ID:", run.info.run_id)
        print({"rmse": rmse, "mae": mae, "r2": r2})
        print(f"Artifacts exported to {MODEL_DIR} and logged to MLflow.")

    print(f"Training + logging took {int(time.time() - t0)}s.")


if __name__ == "__main__":
    main()
