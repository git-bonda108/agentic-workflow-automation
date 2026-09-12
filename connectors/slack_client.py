"""
Slack connector for Dragonfruit demo.
Uses SLACK_BOT_TOKEN when set; list channels and send messages.
"""
from __future__ import annotations

import os

import httpx

_SLACK_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "").strip() or os.environ.get("SLACK_TOKEN", "").strip()
SLACK_API_BASE = "https://slack.com/api"


def is_slack_configured() -> bool:
    return bool(_SLACK_TOKEN)


def _headers() -> dict:
    return {"Authorization": f"Bearer {_SLACK_TOKEN}", "Content-Type": "application/json; charset=utf-8"}


def slack_list_channels(limit: int = 50) -> list[dict]:
    """List public channels. Returns list of {id, name} when configured; else empty."""
    if not is_slack_configured():
        return []
    try:
        with httpx.Client(timeout=10) as client:
            r = client.get(
                f"{SLACK_API_BASE}/conversations.list",
                headers=_headers(),
                params={"types": "public_channel", "limit": limit, "exclude_archived": "true"},
            )
            if not r.json().get("ok"):
                return []
            return [{"id": c["id"], "name": c["name"]} for c in r.json().get("channels", [])]
    except Exception:
        return []


def slack_send_message(channel_id: str, text: str) -> dict:
    """Send a message to a channel. Returns API response or error dict."""
    if not is_slack_configured():
        return {"ok": False, "error": "Slack not configured"}
    try:
        with httpx.Client(timeout=10) as client:
            r = client.post(
                f"{SLACK_API_BASE}/chat.postMessage",
                headers=_headers(),
                json={"channel": channel_id, "text": text},
            )
            return r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}
