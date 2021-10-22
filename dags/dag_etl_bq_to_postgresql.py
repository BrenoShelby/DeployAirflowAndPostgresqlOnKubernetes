# -*- coding: utf-8 -*-
"""
Created on 19/10/2021 13:50,
@author: Breno Gomes
"""

from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from google.cloud import bigquery
from datetime import datetime, timedelta
from airflow import DAG
from pandas import DataFrame
from pandas.io.json import json_normalize
from sqlalchemy import create_engine
from json import loads


POSTGRESQL_CREDENTIALS = Variable.get('postgresql_credentials', deserialize_json=True)


def _extract_data_from_bq():

    # bqclient = bigquery.Client()

    query_string = \
    """
        SELECT
            *
        FROM `bigquery-public-data.crypto_ethereum_classic.tokens`
    """

    return BigQueryHook(bigquery_conn_id='my_gcp_connection', use_legacy_sql=True).get_pandas_df(query_string).to_json()
    # return bqclient.query(query_string).result().to_dataframe().to_json()

def _process_data(ti) -> DataFrame:
    dataframe = ti.xcom_pull(task_ids='extract_data_from_bq')

    print(f'TIPO ----> {type(dataframe)}')

    return dataframe

def _upload_data_on_postgresql(ti) -> None:
    data_str = ti.xcom_pull(task_ids='process_data')

    # CONVERTER DE STRING PARA JSON
    json_dataframe = loads(data_str)

    # CONVERTER JSON PARA DATAFRAME
    dataframe = json_normalize(json_dataframe)

    print(dataframe.head())

    # dialect+driver://username:password@host:port/database
    engine = create_engine(
        f"postgresql+psycopg2://{POSTGRESQL_CREDENTIALS['username']}:{POSTGRESQL_CREDENTIALS['passwd']}@localhost:5432/postgres"
    )

    dataframe.to_sql('class', engine, if_exists='replace', index=False)


docs = """
ETL - Criptomoedas
"""


default_args = {
    'owner': 'Breno Gomes',
    'depends_on_past': False,
    'start_date': datetime(2021, 10, 19),
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id="dag_etl_bq_to_postgresql",
    default_args=default_args,
    description='ETL simples',
    schedule_interval='30 12 * * *',
    dagrun_timeout=timedelta(minutes=15),
    catchup=False,
    tags=['dev'],
) as dag:

    dag.docs = docs

    extract = PythonOperator(
        task_id='extract_data_from_bq',
        python_callable=_extract_data_from_bq
    )

    process = PythonOperator(
        task_id='process_data',
        python_callable=_process_data
    )

    upload = PythonOperator(
        task_id='upload_data_on_postgresql',
        python_callable=_upload_data_on_postgresql
    )

    extract >> process >> upload
