# Dragonfruit — Proposal, Mock Data & MVP

## What’s here

- **Proposal:** `proposal_contract/Dragonfruit_Proposal_EOY2026_Final.html` — full proposal (architecture, AI toolkit, roadmap, costs) aligned to the brief and evaluation criteria.
- **Agentic plan:** `AGENTIC_PLAN.md` — framework choice (OpenAI Agents SDK), connectors, role agents, and **work batches** for parallel execution.
- **Mock data:** `mock_data/*.json` — pipeline stages, time allocations, tool stack, pods/clients, AI survey summary, wish list tools.
- **MVP app:** Streamlit dashboard + **Producer agent** (OpenAI Agents SDK + ClickUp connector). Roles use data connected to ClickUp (real or demo).
- **Connectors:** `connectors/` — ClickUp (real/demo); Slack/Notion/Frame.io in later batches.
- **Role agents:** `role_agents/` — Producer agent (more roles in Batches 2–3).
- **Mock data in MCP:** `mcp_servers/dragonfruit_mock_server.py` — MCP server that exposes `mock_data/*.json` as tools and resources so agents (and any MCP client) can query pipeline, time allocations, pods, tool stack, wishlist, and AI survey.

## Setup

**Producer agent (OpenAI Agents SDK):** requires **Python 3.10+**. Create the venv with `python3.10` or `python3.11` if your default is 3.9.

```bash
cd dragonfruit-workflow-agent
python3 -m venv .venv   # use python3.10+ for agent support
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the MVP dashboard

```bash
source .venv/bin/activate
streamlit run mvp_app.py
```

Then open the URL shown (e.g. http://localhost:8501).

## Run the Mock Data MCP server

Expose pipeline, time allocations, pods, tool stack, wishlist, and AI survey to any MCP client (e.g. the OpenAI Agents SDK or a desktop MCP client). **Requires Python 3.10+** (MCP SDK).

```bash
source .venv/bin/activate
pip install "mcp[cli]"
python mcp_servers/dragonfruit_mock_server.py
```

See `mcp_servers/README.md` for wiring into agents and external MCPs (ClickUp, Notion, Slack, Frame.io).

## Run the Producer agent (CLI)

```bash
source .venv/bin/activate
export OPENAI_API_KEY=sk-...   # required for real agent
# Optional: export CLICKUP_API_KEY and CLICKUP_TEAM_ID for real ClickUp
python run_agent.py "Create a task for Mango Pod: longform edit for Client Alpha, due Friday"
```

Without `OPENAI_API_KEY`, the dashboard still runs and shows a mock result. Without ClickUp env vars, the agent runs in **demo mode** (mock lists/tasks).

## MVP sections

1. **Run Demo** — **Start here.** One priority win (PR-4 Claude-to-ClickUp) end to end: problem (Producers/PCs on ClickUp %) → your data (pipeline, pods) → live Producer agent run → what’s next. See `DEMO_SCRIPT.md` for the exact focus and presenter one-liner.
2. **Time Allocations** — Current vs dream % by role (interactive chart).
3. **Pipeline Overview** — Phases and steps from your pipeline; pods and capacity.
4. **Proposal Summary** — Objective, levers, outcomes, roadmap, costs.
5. **Producer Agent (ClickUp)** — Natural language → Producer agent (OpenAI Agents SDK) → ClickUp tools (real or demo). Roles use data connected to ClickUp.
6. **Wish List & Tools** — High/medium priority tools and current tool stack (top 10).

## Work batches (see AGENTIC_PLAN.md)

- **Batch 1:** ClickUp connector + Producer agent + CLI ✅
- **Batch 2:** Slack connector, PC agent, dashboard wired to agents
- **Batch 3:** CD and PPM agents, Notion/Frame.io stubs
- **Batch 4:** Handoffs, guardrails, human-in-the-loop
- **Batch 5:** MCP, deployment

## Re-extracting from source docs (optional)

If you update the source Excel/Word files:

```bash
.venv/bin/python extract_docs.py
```

This overwrites `extracted_*.txt` in the project root. The MVP uses the `mock_data/*.json` files, which you can edit or regenerate from those extracts.
