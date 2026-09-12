"""
Dragonfruit Demo Backend — Batch 4.
Real ClickUp API for PR-4 and ED-3 (MCP wish list); rest mock.
Uses CLICKUP_API_KEY from .env (DRAGONFRUIT root or backend/.env).
"""
from pathlib import Path
import json

from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Literal, Optional

try:
    from clickup_client import (
        is_configured as clickup_configured,
        get_first_list_id,
        create_task as clickup_create_task,
        get_tasks as clickup_get_tasks,
    )
except Exception:
    def clickup_configured() -> bool:
        return False
    def get_first_list_id() -> None:
        return None
    def clickup_create_task(*args, **kwargs):
        return None
    def clickup_get_tasks(*args, **kwargs):
        return None

app = FastAPI(title="Dragonfruit Demo API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to MCP SYNTHESIZED DATA (sibling of demo-app)
MCP_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "MCP SYNTHESIZED DATA"


class DemoResponse(BaseModel):
    output: str
    reasoning: str
    source: Literal["mock", "mcp", "api"]
    task_link: Optional[str] = None


class AgentCreateTaskRequest(BaseModel):
    prompt: str


class AgentCreateTaskResponse(BaseModel):
    success: bool
    message: str
    task_link: Optional[str] = None
    reasoning: str
    steps: List[str]


class AgentParseResponse(BaseModel):
    success: bool
    task_name: str = ""
    due_date: str = ""
    due_date_ms: Optional[int] = None
    assignee: str = ""
    list_or_pod: str = ""
    tags: List[str] = []
    dependencies: str = ""
    message: str = ""


class AgentConfirmCreateRequest(BaseModel):
    prompt: str
    task_name: str
    due_date: str = ""
    due_date_ms: Optional[int] = None
    assignee: str = ""
    list_or_pod: str = ""
    tags: List[str] = []
    dependencies: str = ""


def _load_mock_pr4() -> DemoResponse:
    p = MCP_DATA_DIR / "clickup_create_task_response.json"
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            conf = data.get("agent_confirmation", {})
            msg = conf.get("message", "Task created (mock).")
            url = None
            resp = data.get("mcp_response") or {}
            if isinstance(resp.get("url"), str):
                url = resp["url"]
            return DemoResponse(output=msg[:500], reasoning="Mock from MCP synthesized data (PR-4).", source="mock", task_link=url)
        except Exception:
            pass
    return DemoResponse(
        output="Task created in ClickUp (mock): 'Schedule client kickoff for Q2 batch'.",
        reasoning="Mock; no ClickUp key or synthesized data.",
        source="mock",
        task_link=None,
    )


def _load_mock_ed3() -> DemoResponse:
    p = MCP_DATA_DIR / "clickup_assign_editor_response.json"
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            cands = data.get("agent_reasoning", {}).get("candidates_evaluated", [])
            best = next((c for c in cands if "Best match" in str(c.get("verdict", ""))), cands[0] if cands else None)
            name = best.get("editor", "Editor") if best else "Editor"
            out = f"Suggested assignees (mock): {name} — best match. Awaiting HITL confirm."
            return DemoResponse(output=out, reasoning="Mock from MCP synthesized data (ED-3).", source="mock", task_link=None)
        except Exception:
            pass
    return DemoResponse(
        output="Suggested assignees: Editor A (capacity 12h), Editor B (capacity 8h). Awaiting HITL confirm.",
        reasoning="Mock; no ClickUp key or synthesized data.",
        source="mock",
        task_link=None,
    )


# Fallback mocks for all tools (when no real integration)
MOCK_RESPONSES: Dict[str, DemoResponse] = {
    "CD-1": DemoResponse(
        output="Retention curve generated. Drop-off flags at 0:45 and 2:10. Suggestions: shorten intro, add hook at 1:30.",
        reasoning="Script + channel context → retention model (mock). Notion MCP optional.",
        source="mock",
        task_link=None,
    ),
    "ED-1": DemoResponse(
        output="Comment sentiment: 2 neutral, 1 positive. No alert threshold exceeded.",
        reasoning="Frame.io comments (mock) → sentiment pass.",
        source="mock",
        task_link=None,
    ),
    "ED-2": DemoResponse(
        output="QC report: 3/5 checks passed. Timestamps: 0:00–0:30 (intro), 2:00 (B-roll gap).",
        reasoning="Video + checklist (mock) → QC service.",
        source="mock",
        task_link=None,
    ),
    "CD-2": DemoResponse(
        output="Outlier digest: 5 videos above threshold. Top performer: 'How to X' (+40% retention at 1:00).",
        reasoning="YouTube/ViewStats (mock) → outlier aggregation.",
        source="mock",
        task_link=None,
    ),
    "CD-3": DemoResponse(
        output="Thumbnail score: 7.2/10. Suggested title variants: 'The Truth About X', 'Why X Matters'.",
        reasoning="Thumbnail + script → vision (mock).",
        source="mock",
        task_link=None,
    ),
    "CD-4": DemoResponse(
        output="Competitor A/B: 2 title changes, 1 thumbnail change. Performance delta: +12% on Channel Y.",
        reasoning="YouTube/ViewStats (mock) → diff detection.",
        source="mock",
        task_link=None,
    ),
}


@app.get("/api/demo/{tool_id}", response_model=DemoResponse)
def run_demo(
    tool_id: str,
    task_name: Optional[str] = Query(None, description="For PR-4: task name to create"),
) -> DemoResponse:
    tool_id = tool_id.upper()

    # PR-4 — Claude-to-ClickUp: real ClickUp API when key present
    if tool_id == "PR-4":
        if clickup_configured():
            list_id = get_first_list_id()
            if list_id:
                name = (task_name or "Demo: Script review by Fri")[:255]
                task = clickup_create_task(list_id, name, "Created via Dragonfruit PR-4 demo (real ClickUp API).")
                if task:
                    url = task.get("url") or f"https://app.clickup.com/t/{task.get('id', '')}"
                    return DemoResponse(
                        output=f"Task created in ClickUp: \"{name}\". List ID: {list_id}.",
                        reasoning="Real ClickUp API: parsed intent → create_task. HITL can be enabled in production.",
                        source="mcp",
                        task_link=url,
                    )
            return DemoResponse(
                output="ClickUp API: could not find a list (no spaces/folders or permission). Using mock.",
                reasoning="Real key present; list discovery failed. Check workspace has at least one list.",
                source="mock",
                task_link=None,
            )
        return _load_mock_pr4()

    # ED-3 — Capacity-based assignment: real tasks from ClickUp when key present
    if tool_id == "ED-3":
        if clickup_configured():
            list_id = get_first_list_id()
            if list_id:
                tasks = clickup_get_tasks(list_id)
                if tasks is not None:
                    # Use real task count; assignees from task assignees or mock
                    open_tasks = [t for t in tasks if str(t.get("status", {}).get("status", "")).lower() in ("open", "to do", "")]
                    assignees = []
                    for t in open_tasks[:3]:
                        for a in t.get("assignees") or []:
                            un = a.get("username") or a.get("email") or str(a.get("id", ""))
                            if un and un not in assignees:
                                assignees.append(un)
                    if assignees:
                        return DemoResponse(
                            output=f"Suggested assignees (from ClickUp): {', '.join(assignees[:5])}. Awaiting HITL confirm.",
                            reasoning="Real ClickUp API: list_tasks → capacity (mock) → suggested assignees. HITL confirm in production.",
                            source="mcp",
                            task_link=None,
                        )
                    return DemoResponse(
                        output=f"List has {len(tasks)} task(s). No assignees on open tasks; suggest manually or add capacity data.",
                        reasoning="Real ClickUp API: fetched tasks; no assignee suggestion without capacity store.",
                        source="mcp",
                        task_link=None,
                    )
            return DemoResponse(
                output="ClickUp API: could not find list. Using mock.",
                reasoning="Real key present; list discovery failed.",
                source="mock",
                task_link=None,
            )
        return _load_mock_ed3()

    return MOCK_RESPONSES.get(
        tool_id,
        DemoResponse(
            output=f"Demo run complete for {tool_id} (mock).",
            reasoning="No real integration for this tool; using generic mock.",
            source="mock",
            task_link=None,
        ),
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "dragonfruit-demo-api", "clickup_configured": clickup_configured()}


# --- Agent: natural language → LLM → ClickUp (plan, reason, act) ---
try:
    from agent_llm import parse_task_prompt, is_llm_configured
except Exception:
    def parse_task_prompt(prompt: str) -> dict:
        return {"task_name": (prompt or "Task")[:255], "due_date": "", "assignee": "", "list_or_pod": "", "tags": [], "dependencies": ""}
    def is_llm_configured() -> bool:
        return False


def _due_date_to_ms(due_date: str) -> Optional[int]:
    """Convert 'Friday', 'next week', or ISO date to unix ms. Returns None if not parseable."""
    if not (due_date or due_date.strip()):
        return None
    import re
    from datetime import datetime, timedelta
    s = due_date.strip().lower()
    now = datetime.utcnow()
    if re.match(r"\d{4}-\d{2}-\d{2}", s):
        try:
            dt = datetime.strptime(s[:10], "%Y-%m-%d")
            return int(dt.replace(tzinfo=None).timestamp() * 1000)
        except Exception:
            pass
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for i, day in enumerate(weekdays):
        if day in s:
            # Next occurrence of that weekday
            current = now.weekday()  # 0 = Monday
            target = i
            days_ahead = (target - current + 7) % 7
            if days_ahead == 0 and "next" in s:
                days_ahead = 7
            elif days_ahead == 0:
                days_ahead = 7  # default to next week if same day
            dt = now + timedelta(days=days_ahead)
            return int(dt.replace(tzinfo=None).timestamp() * 1000)
    if "next week" in s:
        dt = now + timedelta(days=7)
        return int(dt.replace(tzinfo=None).timestamp() * 1000)
    return None


@app.post("/api/agent/parse", response_model=AgentParseResponse)
def agent_parse(body: AgentCreateTaskRequest = Body(...)) -> AgentParseResponse:
    """
    HITL step 1: Parse user prompt with LLM (or fallback). Returns extracted fields for human confirmation.
    """
    prompt = (body.prompt or "").strip()
    if not prompt:
        return AgentParseResponse(success=False, message="Please enter a task description.")
    parsed = parse_task_prompt(prompt)
    task_name = (parsed.get("task_name") or "Task from agent")[:255]
    due_date_str = (parsed.get("due_date") or "").strip()
    due_date_ms = _due_date_to_ms(due_date_str) if due_date_str else None
    return AgentParseResponse(
        success=True,
        task_name=task_name,
        due_date=due_date_str,
        due_date_ms=due_date_ms,
        assignee=(parsed.get("assignee") or "").strip(),
        list_or_pod=(parsed.get("list_or_pod") or "").strip(),
        tags=list(parsed.get("tags") or [])[:10],
        dependencies=(parsed.get("dependencies") or "").strip(),
        message="Review the extracted fields below. Click Confirm & create to create the task in ClickUp (HITL: confirm before create).",
    )


@app.post("/api/agent/confirm-create", response_model=AgentCreateTaskResponse)
def agent_confirm_create(body: AgentConfirmCreateRequest = Body(...)) -> AgentCreateTaskResponse:
    """
    HITL step 2: After human confirms parsed fields, create the task in ClickUp.
    """
    steps = ["Human confirmed the parsed fields (HITL).", "Creating task in ClickUp with tags and due date."]
    prompt = (body.prompt or "").strip()
    task_name = (body.task_name or "Task from agent")[:255]
    tags = list(body.tags or [])[:10]
    deps = (body.dependencies or "").strip()
    description = f"Created via Dragonfruit Agentic AI Pipeline Demo — Plan, Reason and Act.\n\nRequest: {prompt[:500]}"
    if deps:
        description += f"\n\nDependencies: {deps}"

    if not clickup_configured():
        return AgentCreateTaskResponse(
            success=False,
            message="ClickUp is not configured. Add CLICKUP_API_KEY to .env.",
            reasoning="HITL confirmed; ClickUp API key missing for create.",
            steps=steps,
        )
    list_id = get_first_list_id()
    if not list_id:
        return AgentCreateTaskResponse(
            success=False,
            message="Could not find a ClickUp list. Check workspace has at least one list.",
            reasoning="HITL confirmed; list discovery failed.",
            steps=steps,
        )
    task = clickup_create_task(
        list_id,
        name=task_name,
        description=description,
        tags=tags if tags else None,
        due_date_ms=body.due_date_ms,
        assignees=None,
    )
    if not task:
        return AgentCreateTaskResponse(
            success=False,
            message="ClickUp API rejected the request. Check list permissions and payload.",
            reasoning="create_task returned no result.",
            steps=steps,
        )
    url = task.get("url") or f"https://app.clickup.com/t/{task.get('id', '')}"
    steps.append("Task created. Open link to review (HITL: human reviews after create).")
    return AgentCreateTaskResponse(
        success=True,
        message=f"Task \"{task_name}\" created.",
        task_link=url,
        reasoning="Human confirmed (HITL) → agent acted (ClickUp create_task with tags).",
        steps=steps,
    )


# --- MCP synthesized data (from MCP SYNTHESIZED DATA folder) ---

@app.get("/api/clickup/workspace")
def get_clickup_workspace() -> dict:
    """Return workspace structure for demo. When real API is not configured, serves from MCP synthesized data."""
    if clickup_configured():
        # Optional: could call clickup_client get_teams/get_spaces and format here
        pass
    p = MCP_DATA_DIR / "clickup_workspace.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"_meta": {"source": "none"}, "workspace": {"name": "Dragonfruit Media"}, "spaces": []}


@app.get("/api/clickup/synthesized/{name}")
def get_synthesized(name: str) -> dict:
    """Return a single MCP synthesized file by base name (e.g. clickup_create_task_response, clickup_editor_capacity)."""
    allowed = {
        "clickup_create_task_response", "clickup_assign_editor_response", "clickup_editor_capacity",
        "clickup_tasks_mango_batch14", "clickup_timeline_calculator_response", "clickup_workspace",
    }
    if name not in allowed:
        return {"error": "unknown synthesized file"}
    p = MCP_DATA_DIR / f"{name}.json"
    if not p.exists():
        return {"_meta": {"source": "missing"}, "name": name}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {"error": "read failed"}
