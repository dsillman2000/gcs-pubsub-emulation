import dataclasses
import json
import time
from pathlib import Path

from common import calculator
from common.config import Settings
from kafka import KafkaProducer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

settings = Settings()


def validate_checksum(file_path: str) -> bool:
    """Given a file path which ends with a crc 32 checksum, determine if the checksum is valid.

    Args:
        file_path (str): The path to the file with a checksum.

    Returns:
        bool: True if the checksum is valid, False otherwise.
    """
    parts = file_path.rsplit(".", 1)
    suffix = parts[-1] if len(parts) > 1 else ""
    suffix = suffix.lower()
    if not suffix.startswith("crc="):
        return False
    checksum = suffix.split("=", 1)[-1]
    if not checksum.isalnum() or len(checksum) != 8:
        return False
    try:
        checksum_int = int(checksum, 16)
    except ValueError:
        return False
    path = Path(file_path)
    if not path.is_file() or not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return calculator.verify(path.read_bytes(), checksum_int)


class CreatedFileListener(FileSystemEventHandler):
    def __init__(self, producer: KafkaProducer):
        self.producer = producer

    def on_any_event(self, event):
        if event.is_directory or event.event_type not in ("created", "modified", "moved"):
            return
        extant_path = src_path if (src_path := Path(event.src_path)).exists() else Path(event.dest_path)
        if not extant_path.exists():
            print("Ignoring modified event for non-existent file: {}".format(extant_path), flush=True)
            return
        print("Observed event: {}".format(dataclasses.asdict(event)), flush=True)
        if validate_checksum(str(extant_path)):
            print("Received event for file with valid checksum: {}".format(extant_path), flush=True)
        else:
            print("Received event for file with INVALID checksum: {}".format(extant_path), flush=True)
            self.producer.send(settings.KAFKA_TOPIC, dataclasses.asdict(event))


def main():
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_BROKER_URL,
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )
    created_file_listener = CreatedFileListener(producer)
    observer = Observer()
    observer.schedule(created_file_listener, path=settings.WATCHED_DIRECTORY, recursive=True)
    observer.start()
    try:
        while True:
            observer.join(1)
            if not observer.is_alive():
                break
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
