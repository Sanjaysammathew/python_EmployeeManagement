import psycopg
from psycopg.rows import dict_row
from config.settings import settings as config
from psycopg import AsyncConnection


def get_connection():
    return psycopg.AsyncConnection.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        row_factory=dict_row,
    )
