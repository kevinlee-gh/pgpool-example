from sqlalchemy import create_engine, inspect, update
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import Session

from database.schema import LS_SCHEMA
from components.logger import logger

class PostgresClient:
    def __init__(self, 
            host: str,
            port: int,
            user: str,
            password: str,
            database: str
        ):
        self.engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
        self.db_session = Session(self.engine)

    def setup_database(self):
        for schema in LS_SCHEMA:
            with self.engine.connect() as connection:
                if not inspect(connection).has_schema(schema.__table_args__['schema']):
                    connection.execute(CreateSchema(schema.__table_args__['schema']))
                    connection.commit()
                    logger.info(f"Schema '{schema.__table_args__['schema']}' created.")
                else:
                    logger.info(f"Schema '{schema.__table_args__['schema']}' already exists.")

            schema.metadata.create_all(self.engine)
        return 