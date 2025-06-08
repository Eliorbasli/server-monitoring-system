FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (optional for debugging or networking tools)
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Copy requirement file and install Python packages
COPY ../requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY ./app ./app
COPY ./producer_service ./producer_service
COPY ../.env .env

# Set environment variable for Pydantic to locate .env
ENV PYTHONPATH=/app

# Run the service
CMD ["python", "producer_service/main.py"]
