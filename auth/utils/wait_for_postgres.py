import logging
import sys
from time import sleep

import psycopg2
from core.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_postgres_availability() -> None:
    while True:
        try:
            db_connection = psycopg2.connect(config.POSTGRES_DSN)
            logger.info("Postgres Running")
            sys.exit(0)
        except psycopg2.Error:
            logger.error("Postgres is not available. Sleep for 10 sec")
            sleep(10)

        finally:
            db_connection.close()
            sys.exit(1)


if __name__ == "__main__":
    check_postgres_availability()
