# Food broker on Cloud Run. Built in the cloud by `gcloud run deploy --source` (see deploy.sh).
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --only-binary=:all: -r requirements.txt

COPY food_broker ./food_broker

# ADK serves every agent folder under /app; ours is /app/food_broker. Cloud Run sets PORT.
# A4I_UI_FLAG=--with_ui serves ADK's chat page at / as well as the API.
CMD ["sh", "-c", "exec adk api_server ${A4I_UI_FLAG:-} ${A4I_ALLOW_ORIGINS:+--allow_origins=$A4I_ALLOW_ORIGINS} --host 0.0.0.0 --port ${PORT:-8080} /app"]
