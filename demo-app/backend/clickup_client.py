"""
ClickUp API client — real integration for PR-4 (create task) and ED-3 (list tasks).
Uses CLICKUP_API_KEY from env. Official MCP is OAuth; we use REST API with API key for backend.
Ref: https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server-1
"""
import os
from pathlib import Path
from typing import List, Optional

# Load .env from DRAGONFRUIT root (parent of demo-app) or backend/.env
for _path in [Path(__file__).resolve().parent.parent.parent / ".env", Path(__file__).resolve().parent / ".env"]:
    if _path.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(_path)
        except Exception:
            pass
        break

CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY") or os.getenv("CLICKUP_PERSONAL_TOKEN")
CLICKUP_TEAM_ID = os.getenv("CLICKUP_TEAM_ID")  # optional; we discover from API if missing
BASE = "https://api.clickup.com/api/v2"


def _headers() -> dict:
    if not CLICKUP_API_KEY:
        return {}
    return {"Authorization": CLICKUP_API_KEY.strip().strip('"'), "Content-Type": "application/json"}


def get_teams() -> Optional[List[dict]]:
    """GET /team — returns list of workspaces (teams)."""
    import httpx
    try:
        r = httpx.get(f"{BASE}/team", headers=_headers(), timeout=10.0)
        if r.status_code != 200:
            return None
        data = r.json()
        return data.get("teams") or []
    except Exception:
        return None


def get_spaces(team_id: str) -> Optional[List[dict]]:
    """GET /team/{team_id}/space."""
    import httpx
    try:
        r = httpx.get(f"{BASE}/team/{team_id}/space", headers=_headers(), timeout=10.0)
        if r.status_code != 200:
            return None
        data = r.json()
        return data.get("spaces") or []
    except Exception:
        return None


def get_folders(space_id: str) -> Optional[List[dict]]:
    """GET /space/{space_id}/folder."""
    import httpx
    try:
        r = httpx.get(f"{BASE}/space/{space_id}/folder", headers=_headers(), timeout=10.0)
        if r.status_code != 200:
            return None
        data = r.json()
        return data.get("folders") or []
    except Exception:
        return None


def get_lists(folder_id: str) -> Optional[List[dict]]:
    """GET /folder/{folder_id}/list."""
    import httpx
    try:
        r = httpx.get(f"{BASE}/folder/{folder_id}/list", headers=_headers(), timeout=10.0)
        if r.status_code != 200:
            return None
        data = r.json()
        return data.get("lists") or []
    except Exception:
        return None


def get_first_list_id() -> Optional[str]:
    """Discover first available list ID: team → space → folder → list."""
    teams = get_teams()
    if not teams:
        return None
    team_id = str(teams[0]["id"])
    spaces = get_spaces(team_id)
    if not spaces:
        return None
    for space in spaces:
        # Folderless lists first
        try:
            import httpx
            r = httpx.get(f"{BASE}/space/{space['id']}/list", headers=_headers(), timeout=10.0)
            if r.status_code == 200:
                lists_data = r.json()
                lists_arr = lists_data.get("lists") or []
                if lists_arr:
                    return str(lists_arr[0]["id"])
        except Exception:
            pass
        folders = get_folders(str(space["id"]))
        if not folders:
            continue
        for folder in folders:
            lists_arr = get_lists(str(folder["id"]))
            if lists_arr:
                return str(lists_arr[0]["id"])
    return None


def create_task(
    list_id: str,
    name: str,
    description: str = "",
    tags: Optional[List[str]] = None,
    due_date_ms: Optional[int] = None,
    assignees: Optional[List[int]] = None,
) -> Optional[dict]:
    """POST /list/{list_id}/task. Returns task dict with url if successful."""
    import httpx
    payload = {"name": name[:255], "description": description or "Created via Dragonfruit Agentic AI Pipeline Demo."}
    if tags:
        payload["tags"] = [str(t)[:64] for t in tags[:10]]
    if due_date_ms is not None:
        payload["due_date"] = due_date_ms
    if assignees:
        payload["assignees"] = [int(a) for a in assignees[:10]]
    try:
        r = httpx.post(f"{BASE}/list/{list_id}/task", headers=_headers(), json=payload, timeout=15.0)
        if r.status_code not in (200, 201):
            return None
        return r.json()
    except Exception:
        return None


def get_tasks(list_id: str) -> Optional[List[dict]]:
    """GET /list/{list_id}/task. Returns tasks for ED-3 capacity view."""
    import httpx
    try:
        r = httpx.get(f"{BASE}/list/{list_id}/task", headers=_headers(), timeout=10.0)
        if r.status_code != 200:
            return None
        data = r.json()
        return data.get("tasks") or []
    except Exception:
        return None


def is_configured() -> bool:
    return bool(CLICKUP_API_KEY)
