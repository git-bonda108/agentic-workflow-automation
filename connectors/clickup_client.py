"""
ClickUp connector for Dragonfruit agents.
Uses CLICKUP_API_KEY and CLICKUP_TEAM_ID when set; otherwise returns mock data (demo mode).
"""
from __future__ import annotations

import os
from pathlib import Path

import httpx

_BASE = Path(__file__).resolve().parent.parent
_MOCK_PODS = _BASE / "mock_data" / "pods_and_clients.json"

# Env
_API_KEY = os.environ.get("CLICKUP_API_KEY", "").strip()
_TEAM_ID = os.environ.get("CLICKUP_TEAM_ID", "").strip()
CLICKUP_API_BASE = "https://api.clickup.com/api/v2"


def is_clickup_configured() -> bool:
    return bool(_API_KEY and _TEAM_ID)


def _load_mock_pods():
    if not _MOCK_PODS.exists():
        return {"pods": []}
    import json
    with open(_MOCK_PODS, encoding="utf-8") as f:
        return json.load(f)


def _headers() -> dict:
    return {"Authorization": _API_KEY, "Content-Type": "application/json"}


def clickup_get_workspaces() -> list[dict]:
    """Return workspaces (teams) for the configured account. Demo: single mock workspace."""
    if not is_clickup_configured():
        return [{"id": _TEAM_ID or "mock_team", "name": "Dragonfruit (demo)"}]
    with httpx.Client(timeout=15) as client:
        r = client.get(f"{CLICKUP_API_BASE}/team", headers=_headers())
        r.raise_for_status()
        data = r.json()
        return data.get("teams", [])


def clickup_get_spaces(workspace_id: str | None = None) -> list[dict]:
    """Return spaces in the workspace. Demo: Mango Pod, Lemon Pod as spaces."""
    wid = workspace_id or _TEAM_ID
    if not is_clickup_configured():
        pods = _load_mock_pods().get("pods", [])
        return [{"id": p["id"], "name": p["name"]} for p in pods]
    with httpx.Client(timeout=15) as client:
        r = client.get(f"{CLICKUP_API_BASE}/team/{wid}/space", headers=_headers())
        r.raise_for_status()
        return r.json().get("spaces", [])


def clickup_get_folders(space_id: str) -> list[dict]:
    """Return folders in a space. Demo: one folder per space."""
    if not is_clickup_configured():
        return [{"id": f"{space_id}_folder", "name": "Production"}]
    with httpx.Client(timeout=15) as client:
        r = client.get(
            f"{CLICKUP_API_BASE}/space/{space_id}/folder", headers=_headers()
        )
        r.raise_for_status()
        return r.json().get("folders", [])


def clickup_get_lists(
    folder_id: str | None = None,
    space_id: str | None = None,
) -> list[dict]:
    """
    Return lists. If folder_id given, lists in that folder.
    If space_id only (no folder), return lists from first folder in space.
    Demo: returns list per pod (e.g. Mango Pod - Edits, Lemon Pod - Edits). space_id 'mango'/'lemon' filters to that pod.
    """
    if not is_clickup_configured():
        pods = _load_mock_pods().get("pods", [])
        if space_id:
            pods = [p for p in pods if p["id"] == space_id]
        out = []
        for p in pods:
            out.append({
                "id": f"list_{p['id']}",
                "name": f"{p['name']} — Edits",
                "folder_id": f"{p['id']}_folder",
            })
        return out
    if folder_id:
        with httpx.Client(timeout=15) as client:
            r = client.get(
                f"{CLICKUP_API_BASE}/folder/{folder_id}/list", headers=_headers()
            )
            r.raise_for_status()
            return r.json().get("lists", [])
    if space_id:
        folders = clickup_get_folders(space_id)
        if not folders:
            return []
        return clickup_get_lists(folder_id=folders[0]["id"])
    return []


def clickup_get_tasks(
    list_id: str,
    include_closed: bool = False,
) -> list[dict]:
    """Return tasks in a list. Demo: a few mock tasks."""
    if not is_clickup_configured():
        return [
            {"id": "task_1", "name": "Longform edit — Client Alpha", "status": "to do"},
            {"id": "task_2", "name": "Shortform batch — Client Gamma", "status": "in progress"},
        ]
    with httpx.Client(timeout=15) as client:
        r = client.get(
            f"{CLICKUP_API_BASE}/list/{list_id}/task",
            headers=_headers(),
            params={"include_closed": str(include_closed).lower()},
        )
        r.raise_for_status()
        return r.json().get("tasks", [])


def clickup_create_task(
    list_id: str,
    name: str,
    due_date_ms: int | None = None,
    assignees: list[int] | None = None,
    description: str | None = None,
    custom_fields: dict | None = None,
) -> dict:
    """
    Create a task in ClickUp.
    Demo: returns mock task payload without calling API.
    """
    payload = {
        "name": name,
        "description": description or "",
        "due_date": due_date_ms,
        "assignees": assignees or [],
    }
    if custom_fields:
        payload["custom_task_ids"] = True
        payload["custom_fields"] = custom_fields

    if not is_clickup_configured():
        return {
            "id": "demo_task_001",
            "name": name,
            "list_id": list_id,
            "status": "to do",
            "due_date": due_date_ms,
            "assignees": assignees or [],
            "description": description,
            "_demo": True,
        }

    with httpx.Client(timeout=15) as client:
        r = client.post(
            f"{CLICKUP_API_BASE}/list/{list_id}/task",
            headers=_headers(),
            json=payload,
        )
        r.raise_for_status()
        return r.json()


def clickup_update_task_status(task_id: str, status: str) -> dict:
    """Update a task's status. Demo: returns mock success."""
    if not is_clickup_configured():
        return {"id": task_id, "status": status, "_demo": True}
    # ClickUp uses status IDs; we'd need a mapping. For MVP we do a generic update.
    with httpx.Client(timeout=15) as client:
        r = client.put(
            f"{CLICKUP_API_BASE}/task/{task_id}",
            headers=_headers(),
            json={"status": status},
        )
        r.raise_for_status()
        return r.json()
