from locust import User, between, task

from components.client import PostgresClient
from components.locust_task import custom_locust_task
from components.logger import logger

class PostgresLocust(User):
    min_wait = 0
    max_wait = 1
    wait_time = between(min_wait, max_wait)

    def __init__(self, *args):
        super().__init__(*args)

        self.master = PostgresClient(
            host="postgres-proxy",
            port=5433,
            user="postgres",
            password="postgres123",
            database="benchmark_db"
        )
        self.slave = PostgresClient(
            host="postgres-proxy",
            port=5434,
            user="postgres",
            password="postgres123",
            database="benchmark_db"
        )

        self.master.setup_database()
    
    @task
    @custom_locust_task(name="[MASTER] SELECT ALL")
    def master_select_all(self):
        self.master.select_all()
    
    @task
    @custom_locust_task(name="[SLAVE] SELECT ALL")
    def slave_select_all(self):
        self.slave.select_all()