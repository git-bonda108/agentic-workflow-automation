#!/usr/bin/env python3
"""
Dragonfruit Mock Data MCP Server

Exposes mock_data/*.json as MCP tools and resources so agents (and any MCP client)
can query pipeline, time allocations, pods, tool stack, wishlist, and AI survey
without calling live APIs. Use in demo mode or alongside real ClickUp/Notion/Slack MCPs.
"""
import json
from pathlib import Path

# FastMCP from official MCP Python SDK
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    raise ImportError('Install with: pip install "mcp[cli]"') from None

_BASE = Path(__file__).resolve().parent.parent
_MOCK = _BASE / "mock_data"

mcp = FastMCP(
    "Dragonfruit Mock Data",
    instructions="Dragonfruit Media mock data: pipeline, time allocations, pods, tool stack, wishlist, AI survey.",
)


def _load(name: str) -> dict | list:
    path = _MOCK / f"{name}.json"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---- Tools (for agent tool-calling) ----

@mcp.tool()
def get_pipeline() -> str:
    """Return the Dragonfruit production pipeline: phases and steps with role and tool per step."""
    data = _load("pipeline_stages")
    if not data:
        return "Pipeline data not found."
    return json.dumps(data, indent=2)


@mcp.tool()
def get_time_allocations(role: str | None = None) -> str:
    """Return current vs dream time allocation by role. Pass role (e.g. Producers, Editors) or omit for all roles."""
    data = _load("time_allocations")
    roles = data.get("roles", {})
    if not roles:
        return "Time allocation data not found."
    if role:
        if role not in roles:
            return f"Unknown role. Available: {', '.join(roles.keys())}"
        return json.dumps(roles[role], indent=2)
    return json.dumps(roles, indent=2)


@mcp.tool()
def get_pods_and_clients() -> str:
    """Return pods (e.g. Mango, Lemon), clients per pod, and target clients per pod (4 → 7)."""
    data = _load("pods_and_clients")
    if not data:
        return "Pods data not found."
    return json.dumps(data, indent=2)


@mcp.tool()
def get_tool_stack(top_n: int = 20) -> str:
    """Return current tool stack and monthly spend. Optional top_n to limit number of tools (default 20)."""
    data = _load("tool_stack")
    if not data:
        return "Tool stack not found."
    tools = data.get("tools", [])[:top_n]
    total = data.get("total_monthly_usd", 0)
    out = {"total_monthly_usd": total, "tools": tools}
    return json.dumps(out, indent=2)


@mcp.tool()
def get_wishlist_tools(priority: str | None = None) -> str:
    """Return AI wish list tools. priority: 'high', 'medium', or None for both."""
    data = _load("wishlist_tools")
    if not data:
        return "Wishlist not found."
    if priority == "high":
        return json.dumps(data.get("high_priority", []), indent=2)
    if priority == "medium":
        return json.dumps(data.get("medium_priority", []), indent=2)
    return json.dumps({"high_priority": data.get("high_priority", []), "medium_priority": data.get("medium_priority", [])}, indent=2)


@mcp.tool()
def get_ai_survey_summary(role: str | None = None) -> str:
    """Return AI tool survey summary by role (tools used, use cases, requests). Pass role or omit for all."""
    data = _load("ai_survey_summary")
    roles = data.get("roles", [])
    if not roles:
        return "Survey data not found."
    if role:
        for r in roles:
            if r.get("role") == role:
                return json.dumps(r, indent=2)
        return f"Unknown role. Available: {', '.join(r.get('role', '') for r in roles)}"
    return json.dumps(roles, indent=2)


# ---- Resources (URI-based read) ----

@mcp.resource("dragonfruit://pipeline")
def resource_pipeline() -> str:
    """Production pipeline phases and steps."""
    return get_pipeline()


@mcp.resource("dragonfruit://time_allocations")
def resource_time_allocations() -> str:
    """Current vs dream time allocations for all roles."""
    return get_time_allocations(role=None)


@mcp.resource("dragonfruit://time_allocations/{role}")
def resource_time_allocations_role(role: str) -> str:
    """Time allocations for one role (Producers, Production Coordinators, etc.)."""
    return get_time_allocations(role=role)


@mcp.resource("dragonfruit://pods")
def resource_pods() -> str:
    """Pods, clients per pod, target capacity."""
    return get_pods_and_clients()


@mcp.resource("dragonfruit://tool_stack")
def resource_tool_stack() -> str:
    """Current tool stack and monthly spend."""
    return get_tool_stack()


@mcp.resource("dragonfruit://wishlist")
def resource_wishlist() -> str:
    """AI wish list (high and medium priority)."""
    return get_wishlist_tools()


@mcp.resource("dragonfruit://ai_survey")
def resource_ai_survey() -> str:
    """AI tool survey summary by role."""
    return get_ai_survey_summary(role=None)


if __name__ == "__main__":
    mcp.run()
