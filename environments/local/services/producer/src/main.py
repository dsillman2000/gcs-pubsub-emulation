import dataclasses
import datetime
import json
import time

from common.config import Settings
from kafka import KafkaProducer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

settings = Settings()


class CreatedFileListener(FileSystemEventHandler):
    def __init__(self, producer: KafkaProducer, topic: str):
        self.producer = producer
        self.topic = topic

    def on_created(self, event: FileSystemEvent):
        self.producer.send(self.topic, dataclasses.asdict(event))


def main():
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_BROKER_URL, value_serializer=lambda x: json.dumps(x).encode("utf-8")
    )
    created_file_listener = CreatedFileListener(producer, settings.KAFKA_TOPIC)
    observer = Observer()
    observer.schedule(created_file_listener, path=settings.WATCHED_DIRECTORY, recursive=True)
    observer.start()
    try:
        while True:
            print("Pinging (time = {})".format(datetime.datetime.now().isoformat()), flush=True)
            observer.join(1)
            if not observer.is_alive():
                break
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
