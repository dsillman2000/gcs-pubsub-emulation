import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    KAFKA_BROKER_URL: str = "kafka:9092"
    KAFKA_TOPIC: str = "test-topic"
    WATCHED_DIRECTORY: str = "./storage"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        os.makedirs(self.WATCHED_DIRECTORY, exist_ok=True)
