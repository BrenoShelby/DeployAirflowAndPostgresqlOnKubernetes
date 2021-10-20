from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

bqclient = bigquery.Client()

query_string = \
"""
    SELECT
        *
    FROM `bigquery-public-data.crypto_ethereum_classic.tokens`
"""

df = (
    bqclient
    .query(query_string)
    .result()
    .to_dataframe()
    )

from sqlalchemy import create_engine
#dialect+driver://username:password@host:port/database

engine=create_engine("postgresql+psycopg2://postgres:xxxx@localhost:5432/postgres")

import pandas as pd

df = pd.read_csv('class.csv')

try:
    df.to_sql('class', engine, if_exists= 'replace', index= False)

except:
    print("Sorry, some error has occurred!")
finally:
    engine.dispose()

print(dataframe.head())