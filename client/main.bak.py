import os, sys
import time
import logging
import random

from sqlalchemy import create_engine, inspect, update
from sqlalchemy.orm import Session
import psycopg
from locust import User, TaskSet, task, between, events

from database.schema.stress_test.counter import Counter
from components.locust_task import custom_locust_task

logging.basicConfig(
    level = logging.INFO,
    format="%(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

N_INSTANCES= 20




# This class will be executed when you run locust
class PostgresLocust(User):
    min_wait = 0
    max_wait = 1
    wait_time = between(min_wait, max_wait)

    def __init__(self, *args):
        super().__init__(*args)

        engine = create_engine(
            f"postgresql+psycopg2://postgres:postgres123@localhost:6433/benchmark_db",
            pool_size=1,
            pool_timeout=60
        )
        self.db_session = Session(engine)
        logger.info("PostgresLocust initialized.")

    @task
    @custom_locust_task(name="SELECT ALL")
    def select_all(self):
        return self.db_session.query(Counter).all()

    @task
    @custom_locust_task(name="SELECT BY ID")
    def select_by_id(self):
        idx = random.randint(0, N_INSTANCES - 1)
        return self.db_session.query(Counter).filter(Counter.id == idx).first()
    
    @task
    @custom_locust_task(name="ADD 1")
    def add_one(self):
        idx = random.randint(0, N_INSTANCES - 1)
        stmt = (
            update(Counter)
            .where(Counter.id == idx)
            .values(value=Counter.value + 1)
        )
        self.db_session.execute(stmt)
        self.db_session.commit()

        return 'OK'