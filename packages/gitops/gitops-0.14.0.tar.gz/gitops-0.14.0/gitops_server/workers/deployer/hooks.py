"""Overwrite this file in kubernetes to inject custom code"""

import logging
import os
import time
from typing import Any

import httpx
from opentelemetry import trace

from gitops.common.app import App
from gitops_server import settings
from gitops_server.types import UpdateAppResult
from gitops_server.utils import github
from gitops_server.utils.slack import SlackGroup, SlackUser, find_commiter_slack_user

tracer = trace.get_tracer(__name__)

logger = logging.getLogger(__name__)


async def update_issue_from_deployment_url(app: App, deployment_url: str, **kwargs: Any) -> None:
    async with httpx.AsyncClient() as client:
        headers = github.get_headers()
        deployment_response = await client.get(deployment_url, headers=headers)
        try:
            sha = deployment_response.json().get("sha", "")
            issues_response = await client.get(f"https://api.github.com/search/issues?q={sha}+is:pr", headers=headers)
            issue_url = issues_response.json()["items"][0]["url"]
        except Exception:
            logging.warning(f"Could not find issue for {app.name}")
            return

        try:
            response = await client.post(issue_url + "/labels", json={"labels": ["NODEPLOY"]}, headers=headers)
            response.raise_for_status()
            dashboard_url = get_dashboard_url(
                workspace_name=app.name, from_timestamp=kwargs.get("from_timestamp"), to_timestamp=time.time()
            )
            comment = (
                ":poop: Failed to deploy :poop:\n Applying `NODEPLOY` label to shutdown the server"
                f" and prevent deploys until it has been fixed.\nCheck migration logs at {dashboard_url}"
            )
            response = await client.post(issue_url + "/comments", json={"body": comment}, headers=headers)
            response.raise_for_status()
        except Exception:
            logging.warning("Failed to update PR")
            return


async def handle_successful_deploy(app: App, result, deployer, **kwargs) -> UpdateAppResult:
    github_deployment_url = str(app.values.get("github/deployment_url", ""))
    await github.update_deployment(
        github_deployment_url,
        status=github.STATUSES.in_progress,
        description="Helm installed app into cluster. Waiting for pods to deploy.",
    )
    return result


DEFAULT_USER_GROUP = SlackGroup("devops", "", "devops", os.environ.get("DEFAULT_SLACK_USER_GROUP_ID", "S5KVCGSGP"))


def get_dashboard_url(
    workspace_name: str, from_timestamp: float | None = None, to_timestamp: float | None = None
) -> str:
    DASHBOARD_URL = "https://grafana.onuptick.com/d/workforce-failed-deploys/workforce-failed-deploys?from={from_timestamp}&to={to_timestamp}&var-workspace={workspace_name}"

    if from_timestamp:
        from_timestamp_grafana = str(int(from_timestamp * 1000))
    else:
        from_timestamp_grafana = "now-6h"

    if to_timestamp:
        to_timestamp_grafana = str(int(to_timestamp * 1000))
    else:
        to_timestamp_grafana = "now"

    return DASHBOARD_URL.format(
        workspace_name=workspace_name, from_timestamp=from_timestamp_grafana, to_timestamp=to_timestamp_grafana
    )


async def handle_failed_deploy(app: App, result: UpdateAppResult, deployer, **kwargs) -> UpdateAppResult:
    github_deployment_url = str(app.values.get("github/deployment_url", ""))
    if github_deployment_url:
        await github.update_deployment(
            github_deployment_url,
            status=github.STATUSES.failure,
            description=f"Failed to deploy app. {result['output']}",
        )
        await update_issue_from_deployment_url(app, github_deployment_url, **kwargs)

    email = deployer.author_email

    if "devops" in email.lower() or "tickforge" in email.lower():
        slack_user: SlackGroup | SlackUser = DEFAULT_USER_GROUP
    else:
        slack_user = (
            await find_commiter_slack_user(name=deployer.author_name, email=deployer.author_email) or DEFAULT_USER_GROUP
        )
    slack_user_msg = f" {slack_user} " if slack_user else ""
    log_msg = f"<{get_dashboard_url(workspace_name=app.name, from_timestamp=kwargs.get("from_timestamp"), to_timestamp=time.time())}|(Deployment Logs)>"
    result["slack_message"] = (
        f"Failed to deploy app `{result['app_name']}` for cluster"
        f" `{settings.CLUSTER_NAME}` :rotating_light:"
        f" {slack_user_msg} {log_msg}:\n>>>{result['output']}\n"
    )
    return result
