import argparse
import pandas as pd
from airflow.sensors.external_task import ExternalTaskSensor
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.hooks.base import BaseHook
from airflow.operators.python import PythonOperator


from datetime import datetime, timedelta

from sqlalchemy import create_engine

postgre_con = BaseHook.get_connection('postgre_sql_conn')
postgre_con_host = postgre_con.host
postgre_con_user = postgre_con.login
postgre_con_pass = postgre_con.password
postgre_con_port = postgre_con.port

default_args = {
    'owner': 'airflow',
    'email': ['mrteap@ya.ry'],
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False,
    'depends_on_past': False,
    'email_on_failure': False,
    'priority_weight': 10,
    'execution_timeout': timedelta(hours=10),
    'dag_run_timeout': timedelta(hours=10)
}

with DAG(
        dag_id='dag_pg_read',
        schedule_interval='0 18 * * *',
        start_date=datetime(2022, 1, 1),
        catchup=False,
        description=f"""Описание DAG, которое будет видно в airflow""",
        tags=['dag_pg_read'],
        default_args=default_args
) as dag:
    wait_for_pg_insert_dag = ExternalTaskSensor(
        task_id='wait_for_pg_insert_dag',
        external_dag_id='dag_pg_insert',
        external_task_id='firs_task',
        timeout=36000,
        mode='reschedule'
    )

    def read_data_and_save_to_excel():
        sql = """
            select 
                *
            from titanic.titanic_table
        """

        # Создание объекта engine с использованием SQLAlchemy
        engine = create_engine(f'postgresql+psycopg2://{postgre_con_user}:{postgre_con_pass}@{postgre_con_host}:{postgre_con_port}/postgres')

        df = pd.read_sql(sql, engine)
        print('dsadsadas')
        df.to_excel('1.xlsx')


    save_to_excel_task = PythonOperator(
        task_id='save_to_excel_task',
        python_callable=read_data_and_save_to_excel,
        dag=dag

    )

    wait_for_pg_insert_dag >> save_to_excel_task
