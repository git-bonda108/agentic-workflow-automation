# Dragonfruit connectors: ClickUp, Slack, Notion, Frame.io.
# Used by OpenAI Agents SDK as function tools and by the Streamlit app for connection status.

import os

from connectors.clickup_client import is_clickup_configured
from connectors.slack_client import is_slack_configured

def is_frameio_configured() -> bool:
    return bool(os.environ.get("FRAMEIO_ACCESS_TOKEN", "").strip())

def is_notion_configured() -> bool:
    return bool(os.environ.get("NOTION_API_KEY", "").strip())

__all__ = ["is_clickup_configured", "is_slack_configured", "is_frameio_configured", "is_notion_configured"]
