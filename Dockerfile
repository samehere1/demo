FROM python:3.10-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
COPY scripts/ scripts/
COPY model/ model/
COPY data/ data/
ENV MODEL_VERSION=gbm-v1 PYTHONUNBUFFERED=1
CMD ["gunicorn","-k","uvicorn.workers.UvicornWorker","--bind","0.0.0.0:8080","--workers","2","app.main:app"]
