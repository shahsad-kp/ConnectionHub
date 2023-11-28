FROM python:3.11.6-alpine
LABEL authors="shahsad"

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    apt-get install -y build-essential \
RUN pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt
COPY . .