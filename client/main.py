import os
import time
import logging

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
import psycopg
from locust import User, TaskSet, task, between, events

from database.schema.stress_test.counter import Counter

logging.basicConfig(
    level = logging.INFO,
    format="%(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

class PostgresClient:
    def __init__(self):
        engine = create_engine(
            f"postgresql+psycopg2://postgres:postgres123@localhost:5432/postgres",
            pool_timeout=60
        )
        self.db_session = Session(engine)

# This class will be executed when you run locust
class PostgresLocust(User):
    min_wait = 0
    max_wait = 1
    wait_time = between(min_wait, max_wait)

    def __init__(self, *args):
        super().__init__(*args)
        self.client = PostgresClient()

    @task
    def run_query(self):
        res = self.client.db_session.query(Counter).all()
        logger.info(f"Query executed successfully - {len(res)}")
