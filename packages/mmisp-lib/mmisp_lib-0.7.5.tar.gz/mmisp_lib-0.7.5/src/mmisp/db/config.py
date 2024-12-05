"""This module handels the parameters to connect to the database.

The following environment variables are supported:

- DATABASE_URL
- DEBUG
- DB_RETRY: Time to wait before trying new connection attempt. (Default 5)
- DB_MAX_RETRIES: Limit for retry attempts. (Default 100)

"""

import logging
from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    DATABASE_URL: str
    DEBUG: bool
    RETRY_SLEEP: int
    MAX_RETRIES: int


load_dotenv(getenv("ENV_FILE", ".env"))


config: DatabaseConfig = DatabaseConfig(
    DATABASE_URL=getenv("DATABASE_URL", ""),
    DEBUG=bool(getenv("DEBUG", False)),
    RETRY_SLEEP=int(getenv("DB_RETRY", 5)),
    MAX_RETRIES=int(getenv("DB_MAX_RETRIES", 100)),
)
sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.setLevel(logging.INFO)
if config.DEBUG:
    sqlalchemy_logger.setLevel(logging.DEBUG)
