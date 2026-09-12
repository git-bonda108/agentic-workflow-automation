# Dragonfruit Agentic MVP — Plan & Work Batches

## 1. Framework recommendation: **OpenAI Agents SDK**

We recommend **[OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)** (Python) as the primary agentic framework for the MVP and production path.

| Criteria | Why OpenAI Agents SDK |
|----------|------------------------|
| **Role-based agents** | Agents are LLMs with a name + instructions + tools; we define one agent per role (Producer, PC, CD, PPM). |
| **Tools = connectors** | Tools are Python functions or MCP servers. Each connector (ClickUp, Slack, Notion, Frame.io) is exposed as tools the agent can call. |
| **Current landscape** | Production-oriented, supports MCP (Model Context Protocol), guardrails, human-in-the-loop, and tracing. Fits “as good as what can be used in the current landscape.” |
| **Integrations** | Works with **function tools** (our own API clients) and **MCP** (e.g. [Composio ClickUp MCP](https://composio.dev/toolkits/clickup/framework/open-ai-agents-sdk), or self-hosted MCP servers). |
| **Handoffs** | Supports handoffs and “agents as tools” so a Producer agent can delegate to a PC or CD agent when needed. |

**Alternatives considered**

- **LangGraph / LangChain:** More moving parts; SDK is lighter and Python-native for our use case.
- **CrewAI / AutoGen:** Heavier orchestration; we need clear role boundaries and connector-centric tools, which the SDK handles with one agent per role + tools.
- **Raw MCP only:** We still need an agent loop, memory, and guardrails; the SDK provides these and consumes MCP.

**Conclusion:** Use OpenAI Agents SDK for agent loop and roles; implement **connectors** as either **function tools** (Python wrappers around ClickUp/Slack/Notion/Frame.io APIs) or **MCP servers** (for reuse across clients). MVP uses function tools for speed; MCP can be added in a later batch.

**Requirements:** Python 3.10+ for the OpenAI Agents SDK; OpenAI API key for real agent runs.

---

## 2. What we can do (MVP and beyond)

| Capability | MVP (this phase) | Next batches |
|------------|------------------|--------------|
| **Define role agents** | Producer, Production Coordinator (PC), Creative Director (CD), Post-Production Manager (PPM) with instructions and tool access. | Editor-facing agent; handoffs between roles. |
| **ClickUp connector** | List spaces/folders/lists, create task, update task status, search tasks. Real API when `CLICKUP_API_KEY` + `CLICKUP_TEAM_ID` set; else **demo mode** (mock data). | Custom fields, dependencies, bulk create. |
| **Slack connector** | Send message to channel, post templated message. Real API when `SLACK_BOT_TOKEN` set; else demo mode. | Incoming webhooks, slash commands, sentiment triggers. |
| **Notion connector** | Read page, create page (stub or read-only in MVP). | Full CRUD, database query. |
| **Frame.io connector** | Stub: “get comments” for sentiment (MVP returns mock). | Real Frame.io API for ED-1 (sentiment). |
| **Dashboard** | Streamlit app: run Producer (and optionally PC) agent; show current vs dream time; pipeline; **live agent run** with natural language → ClickUp (or mock). | Trace viewer link; multi-agent runs; human-in-the-loop UI. |
| **Data in agents** | Agent receives context (e.g. “current tasks for Mango Pod”) via tools that call ClickUp (or mock). So **roles use data connected to ClickUp** (and later Slack/Notion). | Session memory; per-client context. |
| **Mock data in MCP** | **Dragonfruit Mock Data MCP server** exposes `mock_data/*.json` as tools and resources (pipeline, time allocations, pods, tool stack, wishlist, AI survey). Agents can query this via MCP in demo mode or alongside real ClickUp/Notion/Slack MCPs. | Add more datasets or filter by role/client. |
| **Human-in-the-loop** | Optional approval for “create task” / “send Slack” before execution (SDK supports this). | Full approval UI in dashboard. |

---

## 3. What we are not doing in MVP

- **No real Notion/Frame.io/Dropbox APIs in MVP** — Stubs or mock only; add in later batches.
- **MCP:** We *do* have a **Mock Data MCP server** (`mcp_servers/dragonfruit_mock_server.py`) that exposes pipeline, time allocations, pods, tool stack, wishlist, and AI survey. ClickUp/Notion/Slack can use official or community MCP servers; we keep function tools in MVP and can add those MCPs in Batch 5.
- **No auth UI** — API keys via env vars or `.env`; no OAuth flow in MVP.
- **No production deployment** — Local/Streamlit run; deployment is a separate batch.

---

## 4. High-level architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  User / Slack / Dashboard                                                     │
│  "Create task for Mango Pod, longform for Client Alpha, due Friday, assign   │
│   to Editor 1"                                                                │
└───────────────────────────────────────────┬─────────────────────────────────┘
                                             │
┌────────────────────────────────────────────▼─────────────────────────────────┐
│  OpenAI Agents SDK                                                            │
│  • Producer Agent (instructions + tools)                                      │
│  • PC Agent, CD Agent, PPM Agent (same pattern)                               │
│  • Runner.run(agent, message) → tool calls → result                          │
└────────────────────────────────────────────┬─────────────────────────────────┘
                                             │
┌────────────────────────────────────────────▼─────────────────────────────────┐
│  Connectors (function tools)                                                   │
│  clickup_tools: list_lists, create_task, update_task_status, get_tasks        │
│  slack_tools: send_message, list_channels (demo/real)                          │
│  notion_tools: get_page (stub), create_page (stub)                             │
└────────────────────────────────────────────┬─────────────────────────────────┘
                                             │
┌────────────────────────────────────────────▼─────────────────────────────────┐
│  External APIs (when configured)                                             │
│  ClickUp API | Slack API | Notion API | Frame.io (stub)                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Work distribution — batches

Work is split so different people or workstreams can run in **parallel batches** with clear inputs/outputs.

---

### Batch 1 — Foundation (Agent framework + ClickUp + Producer agent)

**Owner:** Backend / agent developer  
**Goal:** One role (Producer) can perform real or demo ClickUp actions from natural language.

| Task | Deliverable | Deps |
|------|-------------|------|
| 1.1 | Add `openai-agents` (and `openai`) to `requirements.txt`; create `connectors/` and `role_agents/` packages. Python 3.10+ required for SDK. | — |
| 1.2 | **ClickUp connector:** `connectors/clickup_client.py` — functions: `get_workspaces`, `get_folders`, `get_lists`, `get_tasks(list_id)`, `create_task(list_id, name, due_date, assignees, custom_fields)`, `update_task_status`. Use `requests` or `httpx`; env `CLICKUP_API_KEY`, `CLICKUP_TEAM_ID`; if unset, return mock data from `mock_data/`. | — |
| 1.3 | **ClickUp tools for SDK:** `connectors/clickup_tools.py` — wrap connector functions as `@function_tool` (or equivalent) so the SDK can register them. | 1.2 |
| 1.4 | **Producer agent:** `agents/producer_agent.py` — `Agent(name="Producer", instructions=..., tools=[clickup_tools])`. Instructions: create/update tasks, respect pod/client/assignee/due date from user message. | 1.3 |
| 1.5 | **CLI or minimal script:** `run_agent.py` — `Runner.run_sync(producer_agent, sys.argv[1])` so we can test “Create task for Mango Pod…” from command line. | 1.4 |
| 1.6 | **Docs:** In `README_MVP.md` / `AGENTIC_PLAN.md`: how to set `CLICKUP_*` for real API; how demo mode works. | 1.2 |

**Exit criteria:** From CLI, “Create a task for Mango Pod: longform edit for Client Alpha, due Friday, assign to Editor 1” creates a real ClickUp task (or returns a structured mock) via the Producer agent.

---

### Batch 2 — Slack connector + PC agent + dashboard wiring

**Owner:** Backend + frontend  
**Goal:** Production Coordinator agent can use Slack (demo/real); Streamlit dashboard runs Producer and PC agents and shows results.

| Task | Deliverable | Deps |
|------|-------------|------|
| 2.1 | **Slack connector:** `connectors/slack_client.py` — `send_message(channel_id, text)`, `list_channels()`; env `SLACK_BOT_TOKEN`; mock if unset. | — |
| 2.2 | **Slack tools:** `connectors/slack_tools.py` — `@function_tool` for send_message, list_channels. | 2.1 |
| 2.3 | **PC agent:** `agents/pc_agent.py` — instructions: coordinate tasks, send client-facing or internal Slack updates; tools: ClickUp (read/list) + Slack. | Batch 1, 2.2 |
| 2.4 | **Dashboard:** In `mvp_app.py`, “Mock: Claude-to-ClickUp” tab: call `Runner.run_sync(producer_agent, user_message)` (or async); display `result.final_output` and any tool call summary (e.g. “Created task: …”). Option to choose Producer vs PC agent. | Batch 1, 2.3 |
| 2.5 | **Env and docs:** `.env.example` with `CLICKUP_*`, `SLACK_*`, `OPENAI_API_KEY`; README updated. | 2.1 |

**Exit criteria:** In Streamlit, user selects Producer or PC, types a message, and sees the agent’s reply and (in real mode) the resulting ClickUp task or Slack message.

---

### Batch 3 — CD and PPM agents + Notion/Frame.io stubs

**Owner:** Backend  
**Goal:** Creative Director and PPM agents exist; they have tools that can be stubbed (Notion, Frame.io) so we can demo “ask CD for packaging advice” or “ask PPM for editor workload.”

| Task | Deliverable | Deps |
|------|-------------|------|
| 3.1 | **Notion stub:** `connectors/notion_client.py` — `get_page(page_id)`, `create_page(parent_id, title, content)`; return mock or 501 until real API. | — |
| 3.2 | **Frame.io stub:** `connectors/frameio_client.py` — `get_review_comments(asset_id)` returning mock list of comments (for future ED-1 sentiment). | — |
| 3.3 | **CD agent:** `agents/cd_agent.py` — instructions: ideation, packaging, thumbnails, script feedback; tools: Notion (read), optional “packaging score” stub. | 3.1 |
| 3.4 | **PPM agent:** `agents/ppm_agent.py` — instructions: editor workload, QC status, feedback routing; tools: ClickUp (read tasks, list assignees), Frame.io stub (comments). | Batch 1, 3.2 |
| 3.5 | **Dashboard:** Dropdown to select CD or PPM; same run flow as Producer/PC. | 3.3, 3.4 |

**Exit criteria:** CD and PPM agents run from dashboard with stub tools; no errors; responses consistent with role instructions.

---

### Batch 4 — Handoffs, guardrails, human-in-the-loop

**Owner:** Backend  
**Goal:** Producer can hand off to PC or CD when appropriate; optional approval before create_task / send_message.

| Task | Deliverable | Deps |
|------|-------------|------|
| 4.1 | **Handoffs:** Define Producer as router; `handoffs=[pc_agent, cd_agent]`; add handoff descriptions. | Batch 2, 3 |
| 4.2 | **Guardrails:** Validate “create task” inputs (e.g. list_id must belong to configured workspace); use SDK guardrails or pre-tool checks. | Batch 1 |
| 4.3 | **Human-in-the-loop:** For `create_task` and `send_message`, optionally require approval (SDK approval callback); in dashboard, show “Approve?” before executing. | Batch 2, 4.2 |
| 4.4 | **Tracing:** Document how to view runs in OpenAI Trace viewer (or export trace IDs from Runner result). | Batch 1 |

**Exit criteria:** One end-to-end flow where Producer hands off to PC; at least one tool behind approval in the UI.

---

### Batch 5 — MCP and production hardening (optional / later)

**Owner:** Backend / DevOps  
**Goal:** Expose ClickUp (and optionally Slack) as MCP server; run behind env-based config; Docker or deployment script.

| Task | Deliverable | Deps |
|------|-------------|------|
| 5.1 | **ClickUp MCP server:** Implement or wrap existing MCP server that exposes list_lists, create_task, etc.; run via stdio or Streamable HTTP. | Batch 1 |
| 5.2 | **Agent uses MCP:** Swap Producer’s ClickUp function tools for MCP client to same server; verify behavior unchanged. | 5.1 |
| 5.3 | **Config and deployment:** All keys from env; `.env.example` complete; optional Dockerfile for app + MCP. | Batch 2, 5.1 |

---

## 6. Summary table — who does what

| Batch | Focus | Owner | Can start when |
|-------|--------|--------|-----------------|
| **1** | ClickUp connector, Producer agent, CLI run | Backend | Immediately |
| **2** | Slack connector, PC agent, dashboard agent run | Backend + Frontend | After Batch 1 |
| **3** | CD/PPM agents, Notion/Frame.io stubs | Backend | After Batch 1 |
| **4** | Handoffs, guardrails, human-in-the-loop | Backend | After Batches 2 & 3 |
| **5** | MCP, deployment | Backend / DevOps | After Batch 2 |

---

## 7. Running in batches — checklist

- **Batch 1** must finish and be merged (or at least “Producer + ClickUp” working) before Batch 2 depends on it.
- **Batch 2** and **Batch 3** can run in parallel (different agents and connectors).
- **Batch 4** needs both 2 and 3 (all four role agents exist).
- **Batch 5** is optional and can start once Batch 2 is stable.

Use this document as the single source of truth for scope and work distribution; update the “Exit criteria” and “Owner” as you go.
