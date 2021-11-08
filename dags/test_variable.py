from airflow.models import Variable
from datetime import timedelta, datetime
import pendulum
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

my_var = Variable.get("AIRFLOW_VAR_FOO")
local_tz = pendulum.timezone("Asia/Seoul")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 10, 24, tzinfo=local_tz),
    'retries': 0,
}
dag = DAG(
    dag_id='test_variable',
    default_args=default_args,
    schedule_interval='@once',
)    

t1 = BashOperator(
    task_id='print_variable',
    bash_command='echo $my_var',
    dag=dag,
)