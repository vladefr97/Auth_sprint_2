import logging
import os
import sys
from time import sleep

import psycopg2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
dsl = {
    "dbname": os.getenv("POSTGRES_DB", "postgres"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
    "host": os.getenv("POSTGRES_HOST", "postgres"),
}


def check_postgres_availability() -> None:
    while True:
        try:
            db_connection = psycopg2.connect(**dsl)
            logger.info("Postgres Running")
            sys.exit(0)
        except psycopg2.Error:
            logger.error("Postgres is not available. Sleep for 10 sec")
            sleep(10)

        else:
            db_connection.close()  # type: ignore
            sys.exit(1)


if __name__ == "__main__":
    check_postgres_availability()
