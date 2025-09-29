# Sound Realty Pricing API – phData Challenge

This project implements a production-style Machine Learning API for real estate price prediction, built for the phData take-home challenge.

---

## 🚀 Features
- Gradient Boosting Model (GBM) trained on housing + demographics data
- MLflow tracking of experiments and artifacts
- FastAPI app containerized with Docker + Gunicorn
- Batch and JSON (on-demand) prediction endpoints
- Auto-generated API docs via FastAPI (/docs and /redoc)
- CI pipeline with GitHub Actions

---

## 🏗️ Setup

### 1. Clone & enter repo
```bat
git clone https://github.com/samehere1/demo.git
cd demo
```

### 2. Start services
```bat
docker compose up --build
```
This starts:
- API at [http://localhost:8080](http://localhost:8080)
- MLflow UI at [http://localhost:5000](http://localhost:5000)

Check health:
```bat
curl http://localhost:8080/healthz
```

---

## 📖 API Docs

- **Swagger UI** → [http://localhost:8080/docs](http://localhost:8080/docs)  
  Interactive, test endpoints, upload CSVs, copy curl examples.
- **ReDoc UI** → [http://localhost:8080/redoc](http://localhost:8080/redoc)  
  Static, scrollable API reference.
- **OpenAPI spec** → [http://localhost:8080/openapi.json](http://localhost:8080/openapi.json)

> Swagger curl examples are Linux-style. See “Swagger on Windows” below.

---

## 🔮 Training the model

Run locally:
```bat
conda activate phdata
python scripts\train_gbm.py
```

This logs metrics and artifacts to `mlruns/` and saves production artifacts to `model/`.  
Artifacts include `model.pkl`, `model_features.json`, and demographics CSV.  
All logged in MLflow at [http://localhost:5000](http://localhost:5000).

---

## 📦 Batch Scoring

### From CSV
Run batch prediction on unseen examples:

```bat
curl -o data\future_unseen_examples_scores.csv ^
  -F "file=@data\future_unseen_examples.csv" ^
  "http://localhost:8080/v1/predict_batch?output=csv"
```

The output is saved to `data/future_unseen_examples_scores.csv`.

### From JSON (on-demand scoring)

Double-click `scripts/run_json_tiny.bat` or run:
```bat
scripts\run_json_tiny.bat
```
This:
- Creates two JSON payloads
- Calls `/v1/predict`
- Saves results to `data/future_unseen_examples_scores_tiny.json`

---

## ⚡ Swagger on Windows

Swagger (`/docs`) shows curl commands in Linux format. On Windows:

1. Use `^` for line continuation, not `\`
2. Use `"` double quotes, not `'`
3. Ensure file paths are correct

Example (relative path from repo root):

```bat
curl -X POST "http://localhost:8080/v1/predict_batch?output=json" ^
  -H "accept: application/json" ^
  -H "Content-Type: multipart/form-data" ^
  -F "file=@data\future_unseen_examples.csv;type=text/csv"
```

### Save results cleanly
By default, responses dump inline (messy). Use `-o`:

```bat
curl -o data\future_unseen_examples_scores.json ^
  -X POST "http://localhost:8080/v1/predict_batch?output=json" ^
  -H "accept: application/json" ^
  -H "Content-Type: multipart/form-data" ^
  -F "file=@data\future_unseen_examples.csv;type=text/csv"
```

---

## 🖼️ Pretty Printing JSON

The saved JSON is compact (one line). To generate a human-friendly copy:

```bat
:: Convert to pretty JSON
powershell -Command "Get-Content data\future_unseen_examples_scores.json | ConvertFrom-Json | ConvertTo-Json -Depth 5 | Set-Content data\future_unseen_examples_scores_pretty.json"
```

Now you’ll have both:
- `data/future_unseen_examples_scores.json` → raw compact (pipeline-friendly)
- `data/future_unseen_examples_scores_pretty.json` → indented, human-readable

---

## 🎬 One-Click Demo Scripts

For convenience, a few `.bat` scripts are included under `scripts/` so you  can test everything without typing long curl commands.

### 1. Batch scoring (CSV)
```bat
scripts\run_batch_csv.bat
```
- Calls `/v1/predict_batch?output=csv`
- Saves results to: `data/future_unseen_examples_scores.csv`

### 2. Batch scoring (JSON with pretty-print)
```bat
scripts\run_batch_pretty.bat
```
- Calls `/v1/predict_batch?output=json`
- Saves compact JSON → `data/future_unseen_examples_scores.json`
- Saves pretty JSON → `data/future_unseen_examples_scores_pretty.json`

### 3. On-demand (tiny JSON payloads)
```bat
scripts\run_json_tiny.bat
```
- Sends two handcrafted JSON records to `/v1/predict`
- Shows execution time & prediction results
- Saves to: `data/future_unseen_examples_scores_tiny.json`

---

## ✅ Demo checklist

1. Train → `python scripts/train_gbm.py`
2. Start → `docker compose up --build`
3. Health check → `curl http://localhost:8080/healthz`
4. Batch predict → CSV & JSON demos
5. MLflow UI → confirm metrics + artifacts
6. API docs → show `/docs` and `/redoc`

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
├── model/                # Exported artifacts
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🎯 Notes

- Swagger UI → great for reviewers to test interactively
- ReDoc → nice static reference
- MLflow → full experiment history & artifacts
- Curl → cross-platform, but Windows tweaks are documented
- Predictions → available via both CSV batch and JSON on-demand

---
