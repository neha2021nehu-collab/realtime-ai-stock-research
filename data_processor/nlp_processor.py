from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import os
from datetime import datetime, timezone

analyzer = SentimentIntensityAnalyzer()

OUTPUT_DIR = os.path.join(os.path.dirname(__file__),"..","data","processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_sentiment(text:str)->tuple[str,float]:
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return label, round(compound,4)

def process_headline(headline_data:dict)->dict:
    headline = headline_data.get("headline","")
    sentiment, score = get_sentiment(headline)

    enriched = {
        **headline_data,
        "sentiment":sentiment,
        "sentiment_score":score,
        "processed_at":datetime.now(timezone.utc).isoformat()
    }

    save_processed(enriched)
    return enriched


def save_processed(data:dict):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    filepath = os.path.join(OUTPUT_DIR, f"processed_{timestamp}.jsonl")

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")
