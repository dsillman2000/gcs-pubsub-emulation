import json
from pathlib import Path

from common import calculator
from common.config import Settings
from kafka import KafkaConsumer


def checksum_file(file_path: str) -> str | None:
    """Computes the CRC32 checksum of a file and appends it to the file name, updating the file in place.

    Args:
        file_path (str): The path to the file for which the checksum is to be computed.

    Returns:
        str | None: The new file path with the checksum appended, or None if the file does not exist.
    """
    path = Path(file_path)
    if not path.is_file() or not path.exists():
        return None
    checksum = hex(calculator.checksum(path.read_bytes()))[2:].zfill(8)
    new_file_path = path.with_name(f"{path.name}.crc={checksum}")
    path.rename(new_file_path)
    print(f"Computed checksum for {file_path}: {checksum}", flush=True)
    return str(new_file_path)


def main():
    settings = Settings()

    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BROKER_URL,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    print("Waiting for messages...")
    try:
        while True:
            partitions = consumer.poll(timeout_ms=1000)
            for _, messages in partitions.items():
                for message in messages:
                    print(f"Received message: {message.value}", flush=True)
                    file_path = message.value.get("src_path")
                    if file_path is not None:
                        checksum_file(file_path)
    except KeyboardInterrupt:
        print("Stopping consumer...", flush=True)
        consumer.close()
    finally:
        consumer.close()
