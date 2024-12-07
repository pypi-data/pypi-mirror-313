import dataclasses
import logging
from collections.abc import Iterable

import httpx
import slack_sdk

from gitops_server import settings

logger = logging.getLogger("gitops")
client = slack_sdk.WebClient(token=settings.SLACK_TOKEN)


@dataclasses.dataclass
class SlackUser:
    name: str
    email: str
    real_name: str
    id: str

    def __str__(self) -> str:
        return f"<@{self.id}>"


class SlackGroup(SlackUser):
    def __str__(self) -> str:
        return f"<!subteam^{self.id}|{self.name}>"


async def post(message: str) -> str | None:
    """Post a message to a slack channel"""
    logger.info("POSTING TO SLACK")
    if settings.SLACK_TOKEN and settings.SLACK_CHANNEL_ID:
        response = client.chat_postMessage(channel=settings.SLACK_CHANNEL_ID, text=message)
        if response.status_code >= 300:
            logger.warning("Failed to post a message to slack (see below):")
            logger.error(f"{message}", exc_info=True)
        else:
            return response.data["ts"]  # type: ignore
    return None


async def update(*, ts: str, message: str) -> str | None:
    """Update an existing  message to a slack channel

    https://api.slack.com/methods/chat.update
    """
    if settings.SLACK_TOKEN and settings.SLACK_CHANNEL_ID:
        response = client.chat_update(channel=settings.SLACK_CHANNEL_ID, ts=ts, text=message)
        if response.status_code >= 300:
            logger.warning("Failed to post a message to slack (see below):")
            logger.error(f"{message}", exc_info=True)
        else:
            return response.data["ts"]  # type: ignore
    return None


async def find_commiter_slack_user(name: str, email: str) -> SlackUser | None:
    """Find a slack user by name or email using the slack API"""
    if not settings.SLACK_TOKEN:
        return None

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.SLACK_API_USERS_URL}?limit=5&pretty=1",
            headers={"Authorization": f"Bearer {settings.SLACK_TOKEN}"},
            params={"name": name, "email": email},
        )
        data = response.json()

    if not data["ok"]:
        raise Exception(data["error"])
    users = [
        SlackUser(
            m["name"].lower(),
            m["profile"].get("email", "").lower(),
            m.get("real_name", "").lower(),
            m["id"],
        )
        for m in data["members"]
        if not m["is_bot"]
    ]

    matched_user = search(name, email, users)
    return matched_user


def jaccard_similarity(x: Iterable, y: Iterable) -> float:
    """returns the jaccard similarity between two lists or strings"""
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)


def pairwise_tuples(x: str) -> list[tuple[str, str]]:
    """Given William returns [(W,i), (i,l), (l,l), (l,i), (i,a), (a, m)]"""
    if not x or len(x) < 2:
        return [("", "")]
    else:
        return [(letter, x[i + 1]) for i, letter in enumerate(x[:-1])]


def search(name: str, email: str, users: list[SlackUser]) -> SlackUser | None:
    def scoring_fn(user: SlackUser) -> float:
        return (
            jaccard_similarity(pairwise_tuples(user.email.lower()), pairwise_tuples(email.lower()))
            + jaccard_similarity(pairwise_tuples(name.lower()), pairwise_tuples(user.name.lower()))
            + jaccard_similarity(pairwise_tuples(name.lower()), pairwise_tuples(user.real_name.lower()))
        )

    matches = sorted([(scoring_fn(u), u) for u in users], key=lambda x: x[0], reverse=True)
    if matches[0][0] > 0.5:
        return matches[0][1]
    return None
