# RescueBroker Coordinator Dispatch Console on Cloud Run
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY index.html recipients_data.js serve.py ./

CMD ["python3", "serve.py"]
