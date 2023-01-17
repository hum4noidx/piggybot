import os
from typing import Optional

from pydantic import BaseSettings, PostgresDsn, RedisDsn, validator


class Config(BaseSettings):
    bot_token: str = os.getenv("BOT_TOKEN", '')
    postgres_dsn: PostgresDsn = os.getenv("POSTGRES_DSN", '')
    redis_dsn: Optional[str]
    app_host: Optional[str] = os.getenv("APP_HOST", '')
    app_port: Optional[int] = os.getenv("APP_PORT", '')
    webhook_domain: Optional[str] = os.getenv("WEBHOOK_DOMAIN", '')
    webhook_path: Optional[str] = os.getenv("WEBHOOK_PATH", '')
    environment: Optional[str] = os.getenv("ENVIRONMENT", '')
    service_name: Optional[str] = os.getenv("SERVICE_NAME", '')

    @validator("webhook_path")
    def validate_webhook_path(cls, v, values):
        if values["webhook_domain"] and not v:
            raise ValueError("Webhook path is missing!")
        return v

    class Config:
        env_file = '../bot.ini'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


config = Config()
