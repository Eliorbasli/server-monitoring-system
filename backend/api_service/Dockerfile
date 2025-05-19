FROM python:3.11-slim

WORKDIR /app

COPY ../app /app/backend/app
COPY api_service /app/backend/api_service
COPY ../requirements.txt /app/requirements.txt
COPY ../.env /app/.env

RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONPATH=/app

CMD ["uvicorn", "backend.api_service.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
