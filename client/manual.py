import random

from locust import User, between, task
from sqlalchemy import text

from components.client import PostgresClient
from components.locust_task import custom_locust_task
from components.logger import logger

master = PostgresClient(
            host="postgres-proxy",
            port=5433,
            user="postgres",
            password="postgres123",
            database="benchmark_db"
        )
slave = PostgresClient(
    host="postgres-proxy",
    port=5434,
    user="postgres",
    password="postgres123",
    database="benchmark_db"
)


a= int(master.db_session.execute(text("SELECT pg_current_wal_lsn() - '0/0';")).first()[0])
b= int(slave.db_session.execute(text("SELECT pg_last_wal_receive_lsn() - '0/0';")).first()[0])
print(type(a), a)
print(type(b), b)