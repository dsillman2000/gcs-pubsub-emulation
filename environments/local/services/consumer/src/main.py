import json

from common.config import Settings
from kafka import KafkaConsumer


def main():
    settings = Settings()

    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BROKER_URL,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )
    for message in consumer:
        print(message.value)
