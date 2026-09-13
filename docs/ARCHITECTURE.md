# Architecture

This document describes what is actually implemented in this repository — components, data flow, orchestration, and the design decisions visible in the code. The client is referred to generically as "the agency" (a YouTube growth agency); "the media agency" is used only as the project codename baked into module and package names.

## Component map

| Component | Files | Role |
|-----------|-------|------|
| Producer agent | `role_agents/producer_agent.py`, `role_agents/__init__.py` | OpenAI Agents SDK `Agent` (name, instructions, tools). The only role agent implemented. |
| ClickUp function tools | `connectors/clickup_tools.py` | Four `@function_tool` wrappers: `get_clickup_lists`, `get_clickup_tasks`, `create_clickup_task`, `update_clickup_task_status`. Docstrings double as the tool schema the model sees. |
| ClickUp connector | `connectors/clickup_client.py` | httpx client for ClickUp API v2 with a demo-mode branch in every function: no `CLICKUP_API_KEY`/`CLICKUP_TEAM_ID` → answers from `mock_data/pods_and_clients.json` and canned tasks, flagged `_demo: True`. |
| Slack connector | `connectors/slack_client.py` | Channel listing and `chat.postMessage`; returns empty/error dicts rather than raising when unconfigured or failing. |
| CLI entrypoint | `run_agent.py` | `Runner.run(agent, message)` with a tool-call trace printed after the final output. |
| Streamlit dashboard | `mvp_app.py` (791 lines) | Six navigation sections; the Run Demo section has 9 tabs — an overview plus the agency's 8 high-priority wish-list tools. Seven tabs are explicit simulations; the PR-4 tab runs the real Producer agent when `OPENAI_API_KEY` is set, and holds the proposal in `st.session_state` behind a Confirm/Cancel gate. |
| MCP server | `mcp_servers/agency_mock_server.py` | FastMCP (official MCP Python SDK) exposing 6 tools and 7 `agency://` resources over `mock_data/*.json`, stdio transport. |
| React demo | `demo-app/src/` | React 18 + Vite + react-router. Pipeline-first browsing: `/` (pipeline phases) → `/phase/:phaseId` (roles) → `/opportunity/:toolId` (tool detail with run-demo, agent-flow animation, integration and impact data). All content is fetched from static JSON in `demo-app/public/mock_data/`. |
| Demo backend | `demo-app/backend/main.py` (FastAPI), `agent_llm.py`, `clickup_client.py` | `/api/demo/{tool_id}` (mock or live per tool), `/api/agent/parse` and `/api/agent/confirm-create` (two-step HITL task creation), `/api/clickup/*` (serves synthesized workspace JSON), `/health`. |
| Deploy shims | `demo-app/server.js`, `nixpacks.toml`, `START.command` | Railway static serving of `dist/` on `0.0.0.0:$PORT`; local double-click launcher. |
| Domain data | `mock_data/` (13 JSON files), `MCP SYNTHESIZED DATA/` (6 JSON files) | Pipeline stages, role time allocations, pods/clients, tool stack and spend, wish list, survey summary; synthetic ClickUp-shaped responses for offline demos. |
| Data regeneration | `extract_docs.py` | One-shot extraction of the agency's source XLSX/DOCX into `extracted_*.txt`, from which the JSON files were curated by hand. |

## Data flow, end to end

**Agent path (Streamlit / CLI):**

1. A natural-language request enters via the PR-4 tab or `run_agent.py`.
2. `Runner.run` executes the Agents SDK tool loop: the model reads the Producer instructions and tool docstrings, calls `get_clickup_lists` to resolve a `list_id`, then `create_clickup_task` (or the read/update tools).
3. Each tool call lands in `connectors/clickup_client.py`, which either performs a real ClickUp v2 REST call (httpx, 15 s timeout, `raise_for_status`) or returns mock data tagged `_demo`.
4. In the Streamlit PR-4 tab the result is *not* committed: a proposal dict is parked in `st.session_state["pr4_pending"]` and rendered with Confirm/Cancel buttons. Only Confirm calls `clickup_create_task`; Cancel drops the proposal. This is the implemented instance of gate #1 in `HUMAN_IN_THE_LOOP_GATES.md`.

**React demo path:**

1. The frontend renders entirely from static JSON (`usePipeline.ts`, `useAppData.ts` — every hook `fetch`es a file under `/mock_data/` and degrades to `null`/empty state on failure). The app is fully functional with no backend.
2. With the backend running, "run demo" calls `/api/demo/{tool_id}`. PR-4 and ED-3 use the real ClickUp API when a key is present (list discovery via team → space → folderless list → folder → list in `get_first_list_id`); all other tool IDs return curated mocks, several loaded from `MCP SYNTHESIZED DATA/*.json`. Every response declares its provenance in a `source` field (`mock` | `mcp` | `api`).
3. Task creation is a two-request HITL sequence: `/api/agent/parse` extracts `task_name`, `due_date` (+ `due_date_ms` via a weekday-resolution helper), `assignee`, `tags`, `dependencies` — using `gpt-4o-mini` when `OPENAI_API_KEY` is set, otherwise a regex fallback — and returns the fields for human review; `/api/agent/confirm-create` then performs the ClickUp create and returns the task URL plus a `steps` audit trail.

**MCP path:** any MCP client launches `agency_mock_server.py` over stdio and queries the same `mock_data/` JSON through typed tools (`get_pipeline`, `get_time_allocations(role)`, …) or URI resources (`agency://pods`, …). The server is read-only.

## Orchestration analysis

- **The agent loop is sequential and bounded by the SDK.** One agent, one conversation, tools called serially until a final answer. There is no fan-out, no planner–critic pair, and no inter-agent handoff in code (handoffs are a stated SDK capability and appear in the plan documents only).
- **Async is used as plumbing, not concurrency.** `Runner.run` is awaited via `asyncio.run(...)` from synchronous Streamlit callbacks and the CLI. FastAPI endpoints are plain `def` functions (Starlette runs them in a threadpool); all HTTP out-calls use synchronous `httpx` clients. Nothing in the system runs in parallel by design.
- **HITL is a structural step, not a prompt instruction.** Both implementations split propose from act at the API/UI boundary — Streamlit session-state gate, and the parse/confirm-create endpoint pair — so a human decision is required between reasoning and the side effect.
- **Demo mode is a first-class branch, not a stub.** Every integration point checks configuration and returns shape-compatible mock data, so all three surfaces run end to end with zero keys and switch to live calls per integration as keys appear.

## State and context engineering

- **Session state:** `st.session_state` holds pending proposals and per-tab demo results across Streamlit reruns; the React app holds state in hooks. Nothing persists beyond the process; there is no database, cache, or conversation memory.
- **Context assembly:** the Producer agent's context is its instruction block (which encodes demo-mode conventions such as `space_id 'mango'`/`'lemon'` and `list_mango`-style IDs, and the rule "always use the tools; do not invent task IDs") plus tool docstrings and tool results. The backend parser constrains the model with a fixed system prompt demanding a strict-JSON reply with exactly six keys.
- **Bounding:** inputs and outputs are truncated defensively — parser input to 2 000 chars, task names to 255, tags to 10 items / 64 chars, assignees to 10, `max_tokens=500` on the parse call. LLM replies are stripped of markdown code fences before `json.loads`.
- **Retrieval:** none. The domain corpus is small enough to serve whole as structured JSON; the MCP server is the designed channel for giving future agents that context without live-API calls.

## Design decisions and trade-offs visible in the code

1. **Function tools now, MCP alongside.** Connectors are plain Python function tools (fast to build, easy to gate for demos), while the same data is separately exposed via MCP for client-agnostic reuse. `AGENTIC_PLAN.md` records the deliberate deferral of external MCP servers (ClickUp/Notion/Slack) in favor of REST clients.
2. **Two parallel implementations of the same capability.** The Agents SDK path (Streamlit/CLI) demonstrates the production architecture; the FastAPI path re-implements parse→confirm→act deterministically with a no-key fallback so the hosted demo cannot fail on a missing key or SDK version. Cost: duplicated ClickUp clients (`connectors/clickup_client.py` vs `demo-app/backend/clickup_client.py`) with different error styles — one raises, one returns `None`.
3. **Frontend decoupled from backend.** The React app reads only static JSON, so the deployed demo (Railway static serve) works with no server-side dependencies; the backend is additive. The trade-off is a second copy of the mock data under `demo-app/public/mock_data/` that must be kept in sync with `mock_data/`.
4. **Errors degrade to demo output rather than surfacing.** Backend ClickUp helpers catch all exceptions and return `None`, and endpoint logic falls back to mocks with a `reasoning` string explaining why. Good for a live client demo; the cost is silent failure (see HARDENING.md).
5. **Provenance labeling.** `source: mock|mcp|api` on every demo response and `(demo mode)` suffixes on tool results keep simulated output visibly distinct from live output — an honesty mechanism that also aids debugging.
6. **Python 3.9 compatibility shims** (`from __future__ import annotations` in connectors) keep the dashboard runnable on an older interpreter while the Agents SDK path requires 3.10+, with `ImportError` guards that downgrade the PR-4 tab to a mock proposal instead of crashing.

## Extending this system

Grounded next steps that the current structure makes cheap:

1. **Second role agent with handoff.** `role_agents/` and `CLICKUP_TOOLS` are already shaped for one-agent-per-role; adding a Production Coordinator agent and registering the Producer's handoff to it exercises the Agents SDK handoff primitive with no connector changes — the first real test of the multi-agent plan in `AGENTIC_PLAN.md`.
2. **Unify the two ClickUp clients.** Extract one client with an injectable error policy (raise vs. sentinel) and have both the connectors package and the demo backend consume it; this removes the current behavioral drift risk between the demo and the agent path.
3. **Point the agent at the MCP server.** The Agents SDK supports `MCPServerStdio`; wiring `agency_mock_server.py` into `get_producer_agent()` would let the agent ground its answers in pipeline/pods/wish-list context and would validate the MCP-first integration strategy before any external MCP server is adopted.
4. **Persist the HITL audit trail.** `confirm-create` already returns a `steps` list; appending those, with timestamps and the acting human, to a store (even SQLite) turns the existing gates into reviewable evidence — the precondition for the gate inventory in `HUMAN_IN_THE_LOOP_GATES.md` to be enforceable rather than aspirational.
5. **Generate the frontend's mock data copy at build time.** A small build step copying `mock_data/` into `demo-app/public/` eliminates the duplicated-data sync hazard while keeping the static-serve deployment model.
