import json
from kafka import KafkaProducer
from datetime import datetime, timezone

KAFKA_BROKER = "localhost:9092"
TOPIC = "raw_headlines"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_headlines(headlines: list[dict]):
    published = 0
    for item in headlines:
        producer.send(TOPIC, value=item)
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