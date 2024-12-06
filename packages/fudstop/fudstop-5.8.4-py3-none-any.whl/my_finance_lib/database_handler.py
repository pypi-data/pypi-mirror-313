# my_finance_lib/database.py
import pandas as pd
from sqlalchemy import create_engine
import time
from .utils import setup_logging

logger = setup_logging()

class DatabaseHandler:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)

    def batch_insert(self, df, table_name):
        start_time = time.perf_counter()
        try:
            df.to_sql(table_name, con=self.engine, if_exists='append', index=False)
            logger.info(f'Inserted {len(df)} records into {table_name}')
        except Exception as e:
            logger.error(f'Error inserting into {table_name}: {e}')
        finally:
            end_time = time.perf_counter()
            logger.info(f'batch_insert took {end_time - start_time:.4f} seconds')
