from pydantic_settings import BaseSettings
import logging

class Settings(BaseSettings):
    rabbitmq_url: str = "amqp://guest:guest@rabbitmq:5672/"

settings = Settings()
logging.basicConfig(level=logging.INFO)
