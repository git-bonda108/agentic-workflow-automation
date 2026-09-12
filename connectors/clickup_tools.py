"""
ClickUp tools for OpenAI Agents SDK.
Expose connector functions as function_tool so the Producer (and PC) agent can use them.
"""
from __future__ import annotations

from agents import function_tool

from connectors.clickup_client import (
    clickup_create_task,
    clickup_get_lists,
    clickup_get_tasks,
    clickup_update_task_status,
)


@function_tool
def get_clickup_lists(space_id: str | None = None, folder_id: str | None = None) -> str:
    """
    List ClickUp lists (task lists) for a space or folder. Use this to find list_id before creating a task.
    Pass space_id (e.g. 'mango' or 'lemon' for Mango Pod / Lemon Pod in demo) or folder_id.
    Returns a summary of list id and name for each list.
    """
    lists = clickup_get_lists(folder_id=folder_id, space_id=space_id)
    if not lists:
        return "No lists found."
    lines = [f"- id: {l['id']}, name: {l['name']}" for l in lists]
    return "\n".join(lines)


@function_tool
def get_clickup_tasks(list_id: str, include_closed: bool = False) -> str:
    """
    Get tasks in a ClickUp list. Use list_id from get_clickup_lists.
    include_closed: whether to include completed/closed tasks.
    Returns a summary of task id, name, and status.
    """
    tasks = clickup_get_tasks(list_id=list_id, include_closed=include_closed)
    if not tasks:
        return "No tasks in this list."
    lines = []
    for t in tasks:
        name = t.get("name", "?")
        status = t.get("status", {}).get("status", "?") if isinstance(t.get("status"), dict) else t.get("status", "?")
        tid = t.get("id", "?")
        lines.append(f"- id: {tid}, name: {name}, status: {status}")
    return "\n".join(lines)


@function_tool
def create_clickup_task(
    list_id: str,
    name: str,
    due_date_ms: int | None = None,
    description: str | None = None,
) -> str:
    """
    Create a new task in ClickUp. Requires list_id (from get_clickup_lists), task name, and optionally due_date_ms (Unix timestamp in milliseconds) and description.
    Use the list_id that matches the pod (e.g. list_mango for Mango Pod in demo).
    Returns the created task id and name.
    """
    result = clickup_create_task(
        list_id=list_id,
        name=name,
        due_date_ms=due_date_ms,
        description=description,
    )
    tid = result.get("id", "?")
    demo = "(demo mode)" if result.get("_demo") else ""
    return f"Created task id: {tid}, name: {name} {demo}"


@function_tool
def update_clickup_task_status(task_id: str, status: str) -> str:
    """
    Update a ClickUp task's status. task_id from get_clickup_tasks or create_clickup_task.
    status: e.g. 'to do', 'in progress', 'complete'.
    """
    result = clickup_update_task_status(task_id=task_id, status=status)
    demo = "(demo mode)" if result.get("_demo") else ""
    return f"Updated task {task_id} to status: {status} {demo}"


# Collect all tools for the agent
CLICKUP_TOOLS = [
    get_clickup_lists,
    get_clickup_tasks,
    create_clickup_task,
    update_clickup_task_status,
]
