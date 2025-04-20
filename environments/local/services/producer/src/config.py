from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    KAFKA_BROKER_URL: str = "kafka:9092"
    KAFKA_TOPIC: str = "test-topic"
