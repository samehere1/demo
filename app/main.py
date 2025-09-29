# app/main.py
import json, os, pickle, time, io
from pathlib import Path
from typing import Dict, Any

import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

APP_VERSION = "v1"
ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "model"
DATA_DIR = ROOT / "data"
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "model.pkl"
FEATURES_PATH = MODEL_DIR / "model_features.json"
DEMOS_PATH = DATA_DIR / "zipcode_demographics.csv"

app = FastAPI(title="Sound Realty Pricing API", version=APP_VERSION)

# Lazy-loaded globals
MODEL = None
FEATURES = None
DEMOS = None

def _try_load_artifacts():
    global MODEL, FEATURES, DEMOS
    if FEATURES is None and FEATURES_PATH.exists():
        FEATURES = json.load(open(FEATURES_PATH))
    if DEMOS is None and DEMOS_PATH.exists():
        DEMOS = pd.read_csv(DEMOS_PATH).set_index("zipcode")
    if MODEL is None and MODEL_PATH.exists():
        with open(MODEL_PATH, "rb") as f:
            MODEL = pickle.load(f)

class HouseRecord(BaseModel):
    bedrooms: float
    bathrooms: float
    sqft_living: float
    sqft_lot: float
    floors: float
    waterfront: int
    view: int
    condition: int
    grade: int
    sqft_above: float
    sqft_basement: float
    yr_built: int
    yr_renovated: int
    zipcode: int = Field(..., ge=1)
    lat: float
    long: float
    sqft_living15: float
    sqft_lot15: float

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/v1/metadata")
def metadata():
    _try_load_artifacts()
    info = {
        "model_version": os.getenv("MODEL_VERSION", "unset"),
        "demographics_join_key": "zipcode",
        "artifacts_present": {
            "model.pkl": MODEL_PATH.exists(),
            "model_features.json": FEATURES_PATH.exists(),
            "zipcode_demographics.csv": DEMOS_PATH.exists()
        }
    }
    if FEATURES_PATH.exists():
        info["features"] = json.load(open(FEATURES_PATH))
    return info

def _merge_and_vectorize(d: Dict[str, Any]) -> pd.DataFrame:
    if DEMOS is None or FEATURES is None or MODEL is None:
        raise HTTPException(status_code=503, detail="Model artifacts not loaded. Train/copy artifacts into /model.")
    row = pd.DataFrame([d])
    zc = int(row.at[0, "zipcode"])
    if zc not in DEMOS.index:
        raise HTTPException(status_code=400, detail=f"Unknown zipcode: {zc}")
    demo = DEMOS.loc[[zc]].reset_index(drop=False)
    merged = row.merge(demo, on="zipcode", how="left")
    missing = [c for c in FEATURES if c not in merged.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required features: {missing}")
    return merged[FEATURES]

@app.post("/v1/predict")
def predict(h: HouseRecord):
    _try_load_artifacts()
    start = time.time()
    X = _merge_and_vectorize(h.model_dump())
    y = float(MODEL.predict(X)[0])
    return {
        "prediction": y,
        "model_version": os.getenv("MODEL_VERSION", "unset"),
        "features_used": FEATURES,
        "timing_ms": int((time.time()-start)*1000)
    }

@app.post("/v1/predict_min")
def predict_min(d: Dict[str, Any]):
    _try_load_artifacts()
    if "zipcode" not in d:
        raise HTTPException(status_code=400, detail="zipcode is required")
    start = time.time()
    X = _merge_and_vectorize(d)
    y = float(MODEL.predict(X)[0])
    return {
        "prediction": y,
        "model_version": os.getenv("MODEL_VERSION", "unset"),
        "features_used": FEATURES,
        "timing_ms": int((time.time()-start)*1000)
    }

# -------- NEW: batch CSV endpoint --------
@app.post("/v1/predict_batch")
def predict_batch(
    file: UploadFile = File(..., description="CSV with one row per house (no demographics)"),
    output: str = Query("json", pattern="^(json|csv)$")
):
    _try_load_artifacts()

    if file.content_type not in ("text/csv", "application/vnd.ms-excel", "application/octet-stream"):
        raise HTTPException(status_code=400, detail=f"Unsupported content type: {file.content_type}")

    content = file.file.read()
    df = pd.read_csv(io.BytesIO(content))

    if "zipcode" not in df.columns:
        raise HTTPException(status_code=400, detail="zipcode column is required in the CSV")

    merged = df.merge(DEMOS.reset_index(), on="zipcode", how="left")
    missing = [c for c in FEATURES if c not in merged.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required features: {missing}")

    X = merged[FEATURES]
    preds = MODEL.predict(X)
    out_df = df.copy()
    out_df["prediction"] = preds

    # simple request log (optional)
    ts = int(time.time())
    try:
        out_df.assign(_ts=ts).to_csv(LOG_DIR / f"batch_{ts}.csv", index=False)
    except Exception:
        pass

    if output == "json":
        return {"count": len(out_df), "predictions": out_df.to_dict(orient="records")}
    else:
        buf = io.StringIO()
        out_df.to_csv(buf, index=False); buf.seek(0)
        return StreamingResponse(iter([buf.getvalue()]),
                                 media_type="text/csv",
                                 headers={"Content-Disposition": "attachment; filename=predictions.csv"})
