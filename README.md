# Sound Realty Pricing API – phData Challenge

This project implements a production-style Machine Learning API for real estate price prediction, built for the phData take-home challenge.

---

## 🚀 Features
- Gradient Boosting Model (GBM) trained on housing + demographics data
- MLflow tracking of experiments and artifacts
- FastAPI app containerized with Docker + Gunicorn
- Batch and JSON (on-demand) prediction endpoints
- Auto-generated API docs via FastAPI (`/docs` and `/redoc`)
- CI pipeline with GitHub Actions

---

## 🏗️ Setup

### 1) Clone & enter repo
```bat
git clone https://github.com/samehere1/demo.git
cd demo
```

### 2) Start services
```bat
docker compose up --build
```

This starts:
- API → http://localhost:8080
- MLflow UI → http://127.0.0.1:5001

Check health:
```bat
curl http://localhost:8080/healthz
```

---

## 📖 API Docs

- **Swagger UI** → http://localhost:8080/docs  
  Interactive: test endpoints, upload CSVs, copy curl examples.
- **ReDoc UI** → http://localhost:8080/redoc  
  Static, scrollable API reference.
- **OpenAPI spec** → http://localhost:8080/openapi.json

> Swagger’s curl samples are Linux-style. See **Swagger on Windows** below.

---

## 🔮 Training the model

Run locally (host):
```bat
conda activate phdata
python scripts\\train_gbm.py
```

This logs metrics and artifacts to `mlruns/` and saves production artifacts to `model/`.  
Artifacts include `model.pkl`, `model_features.json`, and (optionally) plots.  
All logged in MLflow at **http://127.0.0.1:5001**.

---

## 📦 Batch Scoring

### A) From CSV
Batch prediction on unseen examples:
```bat
curl -o data\\future_unseen_examples_scores.csv ^
  -F "file=@data\\future_unseen_examples.csv" ^
  "http://localhost:8080/v1/predict_batch?output=csv"
```
Output → `data/future_unseen_examples_scores.csv`.

### B) From JSON (on-demand scoring)
Double-click:
```bat
scripts\\run_json_tiny.bat
```
This:
- creates two JSON payloads,
- calls `/v1/predict`,
- saves results to `data/future_unseen_examples_scores_tiny.json`.

---

## ⚡ Swagger on Windows

Swagger (`/docs`) shows curl in Linux format. On Windows:
1) Use `^` for line continuation (not `\\`)  
2) Use `"` double quotes (not `'`)  
3) Check file paths

Example (relative path):
```bat
curl -X POST "http://localhost:8080/v1/predict_batch?output=json" ^
  -H "accept: application/json" ^
  -H "Content-Type: multipart/form-data" ^
  -F "file=@data\\future_unseen_examples.csv;type=text/csv"
```

### Save results cleanly
By default responses print inline. Save to file:
```bat
curl -o data\\future_unseen_examples_scores.json ^
  -X POST "http://localhost:8080/v1/predict_batch?output=json" ^
  -H "accept: application/json" ^
  -H "Content-Type: multipart/form-data" ^
  -F "file=@data\\future_unseen_examples.csv;type=text/csv"
```

---

## 🖼️ Pretty Printing JSON

The saved JSON is compact (one line). Create a human-friendly version:
```bat
powershell -Command "Get-Content data\\future_unseen_examples_scores.json | ConvertFrom-Json | ConvertTo-Json -Depth 5 | Set-Content data\\future_unseen_examples_scores_pretty.json"
```

You’ll have:
- `data/future_unseen_examples_scores.json` → compact (pipeline-friendly)  
- `data/future_unseen_examples_scores_pretty.json` → indented (human-readable)

---

## 🎬 One-Click Demo Scripts (Windows)

Convenience `.bat` scripts in `scripts/` so you don’t type long curl commands:

1) **Batch scoring (CSV)**
```bat
scripts\\run_batch_csv.bat
```
- Calls `/v1/predict_batch?output=csv`
- Saves → `data/future_unseen_examples_scores.csv`

2) **Batch scoring (JSON + pretty)**
```bat
scripts\\run_batch_pretty.bat
```
- Calls `/v1/predict_batch?output=json`
- Saves compact → `data/future_unseen_examples_scores.json`
- Saves pretty → `data/future_unseen_examples_scores_pretty.json`

3) **On-demand (tiny JSON)**
```bat
scripts\\run_json_tiny.bat
```
- Sends two handcrafted JSON records to `/v1/predict`
- Shows execution time & predictions
- Saves → `data/future_unseen_examples_scores_tiny.json`

---

## ⚙️ Environments: Serving vs Training

**Serving (Docker)**  
- The API container is self-contained.  
- Uses the committed baseline model (`model/model.pkl`) so anyone can run the API immediately.  
- Start services:
```bat
docker compose up --build
```

**Training (Host Conda)**  
- Training happens **outside Docker** using a Conda environment.  
- The spec is provided in `environment.yml`.  
- Create & use the environment:
```bat
conda env create -f environment.yml -n phdata
conda activate phdata
python scripts\\train_gbm.py
```
- This regenerates `model/model.pkl` and logs a new run to MLflow at **http://127.0.0.1:5001**.  
- After retraining, restart API to pick up the new model:
```bat
docker compose restart api
```

---

## ✅ Demo checklist

1) Train → `python scripts/train_gbm.py`  
2) Start → `docker compose up --build`  
3) Health → `curl http://localhost:8080/healthz`  
4) Batch predict → CSV & JSON demos  
5) MLflow UI → confirm metrics & artifacts at **http://127.0.0.1:5001**  
6) API docs → show `/docs` and `/redoc`

---

## 📂 Repo Structure

```
phdata-mle-solution/
│
├── app/                  # FastAPI app
│   └── main.py           # API routes
├── scripts/              # Training + demo scripts
│   ├── train_gbm.py
│   ├── run_batch_demo.bat
│   ├── run_batch_csv.bat
│   ├── run_batch_pretty.bat
│   └── run_json_tiny.bat
├── data/                 # Input + outputs
│   └── future_unseen_examples.csv
├── model/                # Exported artifacts (baseline committed)
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── environment.yml
└── README.md
```

---

## 🎯 Notes

- Swagger UI → great for interactive testing  
- ReDoc → static reference  
- MLflow → experiment history & artifacts  
- curl → cross-platform (Windows notes above)  
- Predictions available via both CSV batch and JSON on-demand
