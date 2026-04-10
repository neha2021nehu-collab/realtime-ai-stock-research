import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from confluent_kafka import Consumer
from data_processor.nlp_processor import process_headline
from data_processor.db import insert_headlines  # add this

KAFKA_BROKER = "localhost:9092"
TOPIC = "raw_headlines"


def start_consumer():
    print("[consumer] Starting — listening to topic 'raw_headlines'...")

    consumer = Consumer({
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": "nlp-processor-group-v4",
        "auto.offset.reset": "earliest"
    })

    consumer.subscribe([TOPIC])
    batch = []

    try:
        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                # flush batch every time poll times out
                if batch:
                    insert_headlines(batch)
                    batch = []
                continue

            if msg.error():
                print(f"[consumer] Error: {msg.error()}")
                continue

            headline_data = json.loads(msg.value().decode("utf-8"))
            print(f"\n[consumer] Received: {headline_data['headline'][:60]}...")

            enriched = process_headline(headline_data)
            print(f"[consumer] Sentiment: {enriched['sentiment']} (score: {enriched['sentiment_score']})")

            batch.append(enriched)

            # insert in batches of 50
            if len(batch) >= 50:
                insert_headlines(batch)
                batch = []

    except KeyboardInterrupt:
        if batch:
            insert_headlines(batch)
        print("\n[consumer] Stopped.")
    finally:
        consumer.close()


if __name__ == "__main__":
    start_consumer()