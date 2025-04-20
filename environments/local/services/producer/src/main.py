import json
import time

from common.config import Settings
from kafka import KafkaProducer


def main():
    settings = Settings()

    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_BROKER_URL, value_serializer=lambda x: json.dumps(x).encode("utf-8")
    )
    for i in range(10):
        data = {"counter": i}
        producer.send(settings.KAFKA_TOPIC, value=data)
        time.sleep(1)
    producer.close()
