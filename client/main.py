import random

from locust import User, between, task
from sqlalchemy import text

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
        self.slave2 = PostgresClient(
            host="postgres-proxy",
            port=5434,
            user="postgres",
            password="postgres123",
            database="benchmark_db"
        )
        self.slave3 = PostgresClient(
            host="postgres-proxy",
            port=5435,
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
    @custom_locust_task(name="[MASTER] SELECT BY ID")
    def master_select_by_id(self):
        count = self.master.count_all()
        try:
            self.master.select_by_id(random.randint(0, count - 1))
        except Exception as e:
            return "skip"

    @task
    @custom_locust_task(name="[MASTER] INSERT")
    def master_insert(self):
        self.master.insert_data(random.randint(1, 100))

    @task
    @custom_locust_task(name="[MASTER] DELETE")
    def master_delete(self):
        self.master.delete_data(random.randint(1, 100))

    @task
    @custom_locust_task(name="[MASTER] UPDATE ADD ONE")
    def master_update_add_one(self):
        count = self.master.count_all()
        self.master.update_add_one(random.randint(0, count - 1))

    
    @task
    @custom_locust_task(name="[SLAVE-2] SELECT ALL")
    def slave_select_all(self):
        self.slave2.select_all()

    @task
    @custom_locust_task(name="[SLAVE-2] RANDOM CHECK SYNC")
    def check_sync(self):
        count = self.master.count_all()

        idx= random.randint(0, count - 1)
        try:
            m = self.master.select_by_id(idx)
            s = self.slave2.select_by_id(idx)
        except Exception as e:
            return "skip"
        assert m.value == s.value, "Data mismatch between master and slave"

    @task
    @custom_locust_task(name="[SLAVE-2] ADD ONE & CHECK SYNC")
    def add_one_and_check_sync(self):
        count = self.master.count_all()

        idx= random.randint(0, count - 1)
        self.master.update_add_one(idx)

        try:
            m = self.master.select_by_id(idx)
            s = self.slave2.select_by_id(idx)
        except Exception as e:
            return "skip"
        assert m.value <= s.value, "Data mismatch between master and slave"

    # @task
    # @custom_locust_task(name="CHECK WAL RECEIVE SYNC")
    # def check_wal_receive_sync(self):
    #     a = int(self.master.db_session.execute(text("SELECT pg_current_wal_lsn() - '0/0';")).first()[0])
    #     b = int(self.slave.db_session.execute(text("SELECT pg_last_wal_receive_lsn() - '0/0';")).first()[0])
    #     assert a <= b, "WAL receive LSN mismatch between master and slave"


    # @task
    # @custom_locust_task(name="CHECK WAL REPLAY SYNC")
    # def check_wal_replay_sync(self):
    #     a = int(self.master.db_session.execute(text("SELECT pg_current_wal_lsn() - '0/0';")).first()[0])
    #     b = int(self.slave.db_session.execute(text("SELECT pg_last_wal_replay_lsn() - '0/0';")).first()[0])
    #     assert a <= b, "WAL replay LSN mismatch between master and slave"
