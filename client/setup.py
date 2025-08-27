import logging 

from sqlalchemy import create_engine, inspect
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import Session

from database.schema import LS_SCHEMA
from database.schema.stress_test.counter import Counter

logging.basicConfig(
    level = logging.INFO,
    format="%(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

engine = create_engine(
    f"postgresql+psycopg2://postgres:postgres123@localhost:6433/benchmark_db",
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

db_session = Session(engine)
for i in range(20):
    if db_session.query(Counter).filter(Counter.id == i).all():
        continue
    counter = Counter(
        id = i,
        value= 0, count=0
    )
    db_session.add(counter)
db_session.commit()