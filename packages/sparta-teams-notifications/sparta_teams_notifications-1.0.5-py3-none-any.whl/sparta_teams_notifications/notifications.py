from airflow.models import Variable
from airflow.utils.state import State
from requests import post

FAIL_MSG = "Task Failed"


def teams_notification(
    ctx,
    channels: list[str],
    webhooks_dict_variable: str = "TEAMS_WEBHOOKS",
    airflow_host_variable: str = "AIRFLOW_HOST",
):
    task_instance = ctx.get("task_instance")
    if task_instance.state != State.FAILED:
        return None

    url = task_instance.log_url.replace(
        "localhost:8080", Variable.get(airflow_host_variable)
    )

    dag_run = ctx.get("dag_run")

    if dag_run.run_type == "manual":
        trigger_info = f"Triggered manually"
    else:
        trigger_info = "Triggered automatically"

    card_content = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {
                "type": "TextBlock",
                "text": FAIL_MSG,
                "color": "attention",
                "weight": "bolder",
                "size": "large",
            },
            {
                "type": "FactSet",
                "facts": [
                    {"title": "Task:", "value": task_instance.task_id},
                    {"title": "Dag:", "value": task_instance.dag_id},
                    {
                        "title": "Ref Date:",
                        "value": ctx.get("logical_date").strftime("%Y-%m-%d"),
                    },
                    {"title": "Triggered By:", "value": trigger_info},
                ],
            },
        ],
        "actions": [
            {
                "type": "Action.OpenUrl",
                "title": "View Log",
                "url": url,
            }
        ],
    }

    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": card_content,
            }
        ],
    }
    webhooks_dict: dict = Variable.get(webhooks_dict_variable, deserialize_json=True)

    for channel in channels:
        r = post(
            webhooks_dict.get(channel, "URL_NOT_FOUND"),
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        r.raise_for_status()
