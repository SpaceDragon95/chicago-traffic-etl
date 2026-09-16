
import os
import logging
from pathlib import Path
from sqlalchemy import create_engine, URL
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = int(os.getenv("DB_PORT"))
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

logger = logging.getLogger(__name__)

def create_db_engine():
    db_url = URL.create(
        drivername="postgresql+psycopg",
    )

    db_url = URL.create(
        drivername="postgresql+psycopg",
        username=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name,
    )

    engine = create_engine(db_url)
    return engine

def create_tables(engine):
    sql_path = Path("sql/create_tables.sql")
    sql_script = sql_path.read_text()

    with engine.begin() as connection:
        connection.exec_driver_sql(sql_script)

    logger.info("PostgreSQL tables created successfully")


def load_dataframe(df, table_name, engine):
    df.to_sql(
        name = table_name,
        con = engine,
        schema = "public",
        if_exists = "append",
        index = False,
        chunksize = 1000
    )
    logger.info("Loaded %d rows into %s", len(df), table_name)

