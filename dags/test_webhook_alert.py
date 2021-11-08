from airflow.hooks.base_hook import BaseHook
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from datetime import timedelta, datetime
import pendulum
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

SLACK_CONN_ID = 'slack_conn'
local_tz = pendulum.timezone("Asia/Seoul")


def task_fail_slack_alert(context):
    slack_webhook_token = BaseHook.get_connection(SLACK_CONN_ID).password
    slack_msg = """
    :red_circle: *[보험DW]* batch_tm_daily.sh 
*Dag*: {dag}
*테스크*: {task}  
*실행 시간*: {exec_date}  
*Log Url*: {log_url} 
""".format(
task=context.get('task_instance').task_id,
dag=context.get('task_instance').dag_id,
ti=context.get('task_instance'),
exec_date=context.get('execution_date').in_timezone('Asia/Seoul').strftime('%Y-%m-%d %H:%M:%S'),
log_url=context.get('task_instance').log_url,
)
    failed_alert = SlackWebhookOperator(
        task_id='slack_test',
        http_conn_id='slack_conn',
        webhook_token=slack_webhook_token,
        message=slack_msg,
        username='airflow')
    return failed_alert.execute(context=context)


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 10, 24, tzinfo=local_tz),
    'retries': 0,
    'on_failure_callback': task_fail_slack_alert
}
dag = DAG(
    dag_id='test_webhook_alert',
    default_args=default_args,
    schedule_interval='@once',
)    

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

t2 = BashOperator(
    task_id='print_date_error',
    bash_command='exit(1)',
    dag=dag,
)

t1 >> t2 