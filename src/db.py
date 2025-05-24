import os
import psycopg2


def get_db_connection():
    try:
        return psycopg2.connect(
            host=os.environ["DB_HOST"],
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            port=os.environ.get("DB_PORT", 5432),
        )

    except psycopg2.OperationalError as e:
        print("DB connection error:", e)
        raise
