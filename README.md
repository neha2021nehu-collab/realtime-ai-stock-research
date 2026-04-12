# Real-Time AI Stock Research Agent

An autonomous, production-grade pipeline that monitors financial markets in real time,
runs NLP inference on live news, and serves insights through a React dashboard.

## Architecture

> Finviz → Playwright → Kafka → NLP Consumer → TimescaleDB → FastAPI → React

- **Scraper**: Playwright scrapes Finviz every 30 min via APScheduler with deduplication
- **Streaming**: Apache Kafka (Docker) as message bus — topic `raw_headlines`
- **NLP**: VADER sentiment analysis scores each headline (positive / negative / neutral)
- **Storage**: TimescaleDB hypertable for time-series sentiment queries
- **API**: FastAPI with 4 endpoints — headlines, sentiment summary, trend, search
- **Dashboard**: React + Recharts — live sentiment charts and searchable headlines table
- **MLOps**: MLflow tracks every batch run with metrics and parameters
- **Monitoring**: Prometheus scrapes FastAPI metrics · Grafana visualizes them

## Stack

| Layer | Technology |
|---|---|
| Scraping | Playwright, APScheduler |
| Streaming | Apache Kafka (confluent-kafka) |
| NLP | VADER Sentiment |
| Storage | TimescaleDB (PostgreSQL) |
| Backend | FastAPI, Uvicorn |
| Frontend | React, Recharts |
| MLOps | MLflow |
| Monitoring | Prometheus, Grafana |
| Infra | Docker Compose |

## Running locally

```bash
# Start infrastructure
docker compose up -d

# Start consumer (Terminal 1)
cd data_processor && python consumer.py

# Start API (Terminal 2)
uvicorn api.main:app --reload --port 8000

# Start MLflow (Terminal 3)
mlflow server --host 0.0.0.0 --port 5000

# Start dashboard (Terminal 4)
cd frontend/dashboard && npm start

# Run scraper
cd scraper && python news_scraper.py
```

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /headlines` | Latest headlines with sentiment |
| `GET /sentiment/summary` | Count by sentiment label |
| `GET /sentiment/trend` | Hourly avg sentiment (24h) |
| `GET /headlines/search?q=` | Full-text search |




<img width="1901" height="857" alt="image" src="https://github.com/user-attachments/assets/55106733-3ece-4c72-8ef0-2f725318f39c" />
