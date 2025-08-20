import logging 

from sqlalchemy import create_engine, inspect
from sqlalchemy.schema import CreateSchema

from database.schema import LS_SCHEMA

logging.basicConfig(
    level = logging.INFO,
    format="%(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

engine = create_engine(
    f"postgresql+psycopg2://postgres:postgres123@localhost:5432/postgres",
    pool_timeout=60
)

for schema in LS_SCHEMA:
    with engine.connect() as connection:
        if not inspect(connection).has_schema(schema.__table_args__['schema']):
            connection.execute(CreateSchema(schema.__table_args__['schema']))
            connection.commit()
            logger.info(f"Schema '{schema.__table_args__['schema']}' created.")
        else:
            logger.info(f"Schema '{schema.__table_args__['schema']}' already exists.")

    schema.metadata.create_all(engine)