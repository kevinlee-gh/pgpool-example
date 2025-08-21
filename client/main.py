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

def custom_locust_task(name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            err = None
            start_time = time.time()
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                err = "error {}".format(e)

            events.request.fire(
                request_type="postgres",
                name=name,
                response_time=int((time.time() - start_time) * 1000),
                response_length=len(res) if res else 0,
                exception=err
            )
        return wrapper
    return decorator


class PostgresClient:
    def __init__(self):
        engine = create_engine(
            f"postgresql+psycopg2://postgres:postgres123@localhost:5432/postgres",
            pool_timeout=60
        )
        self.db_session = Session(engine)
    
    @custom_locust_task(name="SELECT ALL")
    def get_all(self):
        return self.db_session.query(Counter).all()


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
        res = self.client.get_all()
