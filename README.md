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