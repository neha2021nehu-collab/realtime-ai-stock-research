import json 
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from confluent_kafka import Consumer
from data_processor.nlp_processor import process_headline

KAFKA_BROKER = "localhost:9092"
TOPIC = "raw_headlines"

def start_consumer():
    print("[consumer] Starting - listening to topic 'raw_headlines'...")

    consumer = Consumer({
        
        "bootstrap.servers":KAFKA_BROKER,
        "group.id":"nlp-processor-group-v3",
        "auto.offset.reset":"earliest"
        
    })
    consumer.subscribe([TOPIC])
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"[consumer] Error: {msg.error()}")
                continue
    
            headline_data = json.loads(msg.value().decode("utf-8"))
            print(f"\n[consumer] Recieved: {headline_data['headline'][:60]}...")

            enriched = process_headline(headline_data)

            print(f"[consumer] Sentiment: {enriched['sentiment']} (score: {enriched['sentiment_score']})")
            print(f"[consumer] Saved to processed store.")
    except KeyboardInterrupt:
        print("\n[consumer] Stopped.")
    finally:
        consumer.close()


if __name__=="__main__":
    start_consumer()