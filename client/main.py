import os
import time

import psycopg
from locust import User, TaskSet, task, between, events


class PostgresClient:
    def __init__(self, conn_string):
        self.db_conn = psycopg.connect(conn_string)

    def execute_query(self, query):
        with self.db_conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    

# This class will be executed when you run locust
class PostgresLocust(User):
    min_wait = 0
    max_wait = 1
    wait_time = between(min_wait, max_wait)
    conn_string = "postgresql://postgres:postgres123@localhost:5432/postgres"

    def __init__(self, *args):
        super().__init__(*args)
        self.client = PostgresClient(self.conn_string)

    @task
    def run_query(self):
        self.client.execute_query(
            f"SELECT * FROM loadtesting.user",
        )
