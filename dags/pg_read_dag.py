from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.hooks.base import BaseHook
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from datetime import datetime, timedelta

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

"""
Описание DAG
"""
with DAG(
        dag_id='dag_pg_read',
        schedule_interval='0 18 * * *',
        start_date=datetime(2022, 1, 1),
        catchup=False,
        description=f"""Описание DAG, которое будет видно в airflow""",
        tags=['dag_pg_read'],
        default_args=default_args
) as dag:
    # Сенсор ожидания выполнения DAG pg_insert_dag
    wait_for_pg_insert_dag = ExternalTaskSensor(
        task_id='wait_for_pg_insert_dag',
        external_dag_id='dag_pg_insert',
        external_task_id='firs_task',
        timeout=36000,
        mode='reschedule'
    )

    
    result_firs_task = BashOperator(
        task_id='firs_task', 
        bash_command=f"python3 /opt/airflow/dags/pg_read.py {postgre_con_host} {postgre_con_user} {postgre_con_pass} {postgre_con_port}"
        )

    wait_for_pg_insert_dag >> result_firs_task
