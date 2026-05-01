from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/opt/airflow')

from ingestion.pipeline import fetch_all_countries
from ingestion.db import save_to_db

default_args = {
    'owner' : 'airflow',
    'retries' : 3,
    'retry_delay' : timedelta(minutes=5),
}

def run_pipeline():
    df = fetch_all_countries()
    save_to_db(df)
    print(f"Zapisano {len(df)} rekordów")

with DAG(
    dag_id='music_pipeline',
    default_args=default_args,
    description='Pobiera Top 50 z Last.fm i Spotify co dzien',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    pipeline_task = PythonOperator(
        task_id='fetch_and_save',
        python_callable=run_pipeline,
    )