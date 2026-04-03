# Real-Time AI Stock Research Agent

An autonomous, production-grade pipeline that monitors financial markets in real time,
runs NLP inference on live news, and serves insights through a WebSocket-powered dashboard.

## Architecture
(diagram coming soon)

## Stack
- **Scraping:** Playwright, Scrapy
- **Streaming:** Apache Kafka (Confluent free tier)
- **ML Tracking:** MLflow
- **Orchestration:** Prefect
- **Storage:** TimescaleDB (time-series) + ChromaDB (vectors)
- **Backend:** FastAPI + WebSockets
- **Frontend:** React + Recharts
- **Monitoring:** Prometheus + Grafana
- **Deployment:** Docker Compose + Render

## Roadmap
- [ ] Week 1 — Data ingestion pipeline (Scraper → Kafka → TimescaleDB)
- [ ] Week 2 — NLP inference + RAG layer
- [ ] Week 3 — ML model + automated retraining
- [ ] Week 4 — FastAPI + React live dashboard
- [ ] Week 5 — Monitoring + full deployment

## Setup
(instructions coming soon)