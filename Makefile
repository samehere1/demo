# Simple Makefile for local dev and Docker

APP_NAME=sound-realty-api
TAG=gbm-v1

.PHONY: init format lint test run docker-build docker-run clean

init:
	python -m pip install -r requirements.txt

format:
	black .

lint:
	flake8 .

test:
	pytest -q

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8080

docker-build:
	docker build -t $(APP_NAME):$(TAG) .

docker-run:
	docker run --rm -p 8080:8080 -e MODEL_VERSION=$(TAG) $(APP_NAME):$(TAG)

clean:
	rm -rf model mlruns __pycache__ .pytest_cache .mypy_cache
