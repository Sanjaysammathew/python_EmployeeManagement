import psycopg2

from config import config

def get_connection() :
    return psycopg2.connect(

        host=config.DB_HOST,
        PORT=config.DB_PORT,
        db_name=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )
