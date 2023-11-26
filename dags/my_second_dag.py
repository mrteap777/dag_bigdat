from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

# DAG представляет собой рабочий процесс, набор задач
with DAG(dag_id="demo2", start_date=datetime(2022, 1, 1), schedule_interval="0 0 * * *") as dag:

    # Задачи представлены в виде операторов
    hello = BashOperator(task_id="hello", bash_command="echo hello")

    @task()
    def airflow_task():
        print("airflow")

    # Еще одна задача BashOperator
    bash_task = BashOperator(task_id="bash_task", bash_command="python3 '/opt/airflow/dags/test.py'")
    bash_task2 = BashOperator(task_id="bash_task2", bash_command="python3 '/opt/airflow/dags/test.py'")
    bash_task3 = BashOperator(task_id="bash_task3", bash_command="python3 '/opt/airflow/dags/test.py'")
    # Задаем зависимости между задачами для последовательного выполнения
    hello >> airflow_task() >> bash_task >> bash_task2 >> bash_task3