"""Define pre-made TaskGroups for usage across DAGs."""

from uuid import uuid4

from airflow import AirflowException, DAG
from airflow.models import TaskInstance
from airflow.operators.python import PythonOperator
from airflow.utils.db import provide_session
from airflow.utils.state import State
from airflow.utils.task_group import TaskGroup
from airflow.utils.trigger_rule import TriggerRule

from regscale.airflow.hierarchy import AIRFLOW_CLICK_OPERATORS as OPERATORS
from regscale.airflow.tasks.click import execute_click_command
from regscale.core.app.api import Api
from regscale.core.app.utils.regscale_utils import send_email


def generate_name(name: str, tag: str = None) -> str:
    """Generate a unique name for a TaskGroup

    :param str name: the name of the TaskGroup
    :param str tag: a unique identifier for the TaskGroup
    :return: a unique name for the TaskGroup
    :rtype: str
    """
    if not tag:
        tag = str(uuid4())[:8]  # give the task group a unique name for tracking
    return f"{name}-{tag}"


def setup_task_group(
    dag: DAG,
    setup_tag: str = None,
) -> TaskGroup:
    """Create a TaskGroup for setting up the init.yaml and initialization of the DAG

    :param DAG dag: an Airflow DAG
    :param str setup_tag: a unique identifier for the task
    :return: a setup TaskGroup
    :rtype: TaskGroup
    """
    setup_name = generate_name("setup", setup_tag)
    with TaskGroup(setup_name, dag=dag) as setup:
        login = PythonOperator(
            task_id=f"login-{setup_tag}",
            task_group=setup,
            python_callable=execute_click_command,
            op_kwargs={
                "command": OPERATORS["login"]["command"],
                "token": '{{ dag_run.conf.get("token") }}',
                "domain": '{{ dag_run.conf.get("domain") }}',
            },
        )
        login
        return setup


@provide_session
def _email_on_fail(task, execution_date, dag, session=None, **kwargs):
    """
    Send an email if any of the upstream DAGs failed

    :param DAG dag: The DAG to add the operator to
    :param execution_date: The execution date of the DAG
    :param session: DAG session
    :return: The PythonOperator to send an email if any of the DAG tasks fail
    :rtype: TaskGroup
    """
    upstream_task_instances = (
        session.query(TaskInstance)
        .filter(
            TaskInstance.dag_id == dag.dag_id,
            TaskInstance.execution_date == execution_date,
            TaskInstance.task_id.in_(task.upstream_task_ids),
        )
        .all()
    )
    upstream_states = [ti.state for ti in upstream_task_instances]
    fail_this_task = State.FAILED in upstream_states
    api = Api()
    dag_config = kwargs["dag_run"].conf

    if email := kwargs["dag_run"].conf.get("email"):
        email_payload = {
            "id": 0,
            "from": "Support@RegScale.com",
            "emailSenderId": api.config["userId"],
            "to": email,
            "cc": "",
            "dateSent": "",
            "subject": f"An Automated Job Has Failed: {dag_config['jobName']} ({dag_config['cadence']})",
            "body": f"{dag.dag_id} with ID: {dag_config['dag_run_id']} job has failed. Please check the logs for more information: {dag_config['job_url']}",
        }

        if send_email(api=api, domain=api.config["domain"], payload=email_payload):
            print(f"Email sent to {email} about {dag.dag_id} job failure.")

    if fail_this_task:
        raise AirflowException("Failing task because one or more upstream tasks failed.")


def email_on_fail_operator(dag, email_tag: str = None) -> PythonOperator:
    """
    Create a PythonOperator to send an email if any of the DAGs fail

    :param DAG dag: The DAG to add the operator to
    :param str email_tag: A unique identifier for the task, if not provided one will be generated.
    :return: The PythonOperator to send an email if any of the DAG tasks fail
    :rtype: TaskGroup
    """
    return PythonOperator(
        task_id=generate_name("email", email_tag),
        python_callable=_email_on_fail,
        trigger_rule=TriggerRule.ALL_DONE,
        provide_context=True,
        dag=dag,
    )
