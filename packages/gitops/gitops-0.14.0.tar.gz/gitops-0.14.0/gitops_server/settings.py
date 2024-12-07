import os

CLUSTER_NAME = os.getenv("CLUSTER_NAME", "")
# Namespace to search/deploy into
CLUSTER_NAMESPACE = os.getenv("CLUSTER_NAMESPACE", "")
ACCOUNT_ID = os.getenv("ACCOUNT_ID", "")
GITHUB_WEBHOOK_KEY = os.getenv("GITHUB_WEBHOOK_KEY", "")

SLACK_API_USERS_URL = os.environ.get("SLACK_API_USERS_URL", "https://slack.com/api/users.list")
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
# The slack channel ID starts with C
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID", "")

# How many parallel deploys can be done at once
GITOPS_MAX_PARALLEL_DEPLOYS = os.environ.get("GITOPS_MAX_PARALLEL_DEPLOYS", "5")
