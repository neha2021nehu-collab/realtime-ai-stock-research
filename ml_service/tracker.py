import mlflow
import mlflow.sklearn
from datetime import datetime, timezone

EXPERIMENT_NAME = "stock-sentiment-analysis"

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment(EXPERIMENT_NAME)

def log_sentiment_batch(headlines: list[dict]):
    if not headlines:
        return
    positive = sum(1 for h in headlines if h["sentiment"] == "positive")
    negative = sum(1 for h in headlines if h["sentiment"] == "negative")
    neutral = sum(1 for h in headlines if h["sentiment"] == "neutral")
    avg_score = sum(h["sentiment_score"] for h in headlines) / len(headlines)

    with mlflow.start_run(run_name=f"batch_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"):
        #log metrics
        mlflow.log_metric("total_headlines" , len(headlines))
        mlflow.log_metric("positive_count" , positive)
        mlflow.log_metric("negative_count" , negative)
        mlflow.log_metric("neutral_count" , neutral)
        mlflow.log_metric("avg_sentiment_score" , round(avg_score, 4))
        mlflow.log_metric("positive_score" , round(positive / len(headlines), 4))
        mlflow.log_metric("negative_score" , round(negative / len(headlines), 4))

        #log parameters
        mlflow.log_param("model", "VADER")
        mlflow.log_param("source", "Finviz")
        mlflow.log_param("batch_size", len(headlines))
        mlflow.log_param("processed_at", datetime.now(timezone.utc).isoformat())
    print(f"[mlflow] Logged batch - {len(headlines)} headlines, avg score : {round(avg_score, 4)}")

if __name__ == "__main__":
    #test with dummy data
    test_data = [{"sentiment": "positive", "sentiment_score": 0.8},
        {"sentiment": "negative", "sentiment_score": -0.5},
        {"sentiment": "neutral",  "sentiment_score": 0.0},
        ] 
    log_sentiment_batch(test_data)       