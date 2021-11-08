from airflow.hooks.base_hook import BaseHook
from airflow.operators.slack_operator import SlackAPIPostOperator

class SlackAlert:
    def __init__(self, channel):
        self.slack_channel = channel
        self.slack_token = BaseHook.get_connection('slack').password

    def slack_fail_alert(self, context):
        alert = SlackAPIPostOperator(
            task_id='slack_failed',
            channel=self.slack_channel,
            token=self.slack_token,
            text="""
                :red_circle: Task Failed.
                *Task*: {task}  
                *Dag*: {dag}
                *Execution Time*: {exec_date}  
                *Log Url*: {log_url}
                """.format(
                    task=context.get('task_instance').task_id,
                    dag=context.get('task_instance').dag_id,
                    exec_date=context.get('execution_date'),
                    log_url=context.get('task_instance').log_url,
                    )
        )
        return alert.execute(context=context)