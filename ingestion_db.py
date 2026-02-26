import pandas as pd
import os 
from sqlalchemy import create_engine
import logging
import time

engine = create_engine('sqlite:///inventory.db')

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode = "a"
)

def load_raw_data():
    '''This function will load the csv into dataframe and ingest into DB '''
    start = time.time()
    for file in os.listdir('data'):
        if '.csv' in file:
            df = pd.read_csv('data/'+file)
            logging.info(f'Ingesting {file} in db')
            ingest_db(df, file[:-4], engine)
    end =time.time()
    total_time = (end - start)/60
    logging.info('--------------- Ingestion completed --------------')
    logging.info(f'Total time taken: {total_time} minutes')

def ingest_db(df, table_name, engine):
    ''' this function will ingest the dataframe into db table '''
    df.to_sql(table_name, con = engine, if_exists = 'replace', index = False)

if __name__ == '__main__':
    load_raw_data()
