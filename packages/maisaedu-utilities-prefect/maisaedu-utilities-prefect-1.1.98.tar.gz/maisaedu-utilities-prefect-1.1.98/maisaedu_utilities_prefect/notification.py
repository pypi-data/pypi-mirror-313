import json
import requests


def send_teams_alert_on_failure(
    task_future, teams_webhook_path="data/teams_webhook_url.json"
):
    fallback_path = "data/teams_webhook_url.json"
    try:
        with open(teams_webhook_path) as file:
            teams_webhook = json.load(file)
    except Exception as e:
        with open(fallback_path) as file:
            teams_webhook = json.load(file)

    tasks_future = []
    if type(task_future) != list:
        tasks_future.append(task_future)
    else:
        tasks_future = task_future

    for task_future in tasks_future:
        task_future.wait()  # block until completion
        if task_future.get_state().is_failed():
            name_ = task_future.task_run.name
            id_ = task_future.task_run.flow_run_id
            message_ = task_future.task_run.state.message

            requests.post(
                teams_webhook["url"],
                json={
                    "text": f"The task `{name_}` failed in a flow run `{id_}` because of this reason -> `{message_}`"
                },
            )
