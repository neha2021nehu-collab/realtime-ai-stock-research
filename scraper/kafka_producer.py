import json
from confluent_kafka import Producer
from datetime import datetime, timezone

KAFKA_BROKER = "localhost:9092"
TOPIC = "raw_headlines"

producer = Producer(
    {"bootstrap.servers":KAFKA_BROKER}
    
)

def delivery_report(err, msg):
    if err:
        print(f"[kafka] Delivery failed: {err}")

def publish_headlines(headlines: list[dict]):
    published = 0
    for item in headlines:
        producer.produce(
            TOPIC,
            value=json.dumps(item).encode("utf-8"),
            callback=delivery_report
        )
        published += 1
    producer.flush()
    print(f"[kafka] Published {published} headlines to topic '{TOPIC}'")

if __name__=="__main__":
    #quick test - publish one dummy message
    test_msg = {
        "headline": "test headline",
        "url" : "https://test.com",
        "time_raw" : "09:00AM",
        "published_at" : f"{datetime.now(timezone.utc).date().isoformat()} 09:00AM",
        "scraped_at" : datetime.now(timezone.utc).isoformat()
    }
    publish_headlines([test_msg])
    print("[kafka] Test message sent successfully.")