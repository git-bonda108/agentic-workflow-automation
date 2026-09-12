# Pipeline Demo — Batch Plan (Complete)

**Principle:** No half-measures. Every screen, every card, every tile uses the agreed typography. Every high-priority opportunity has a full solution (input, output, run demo, reasoning, GIF, integration, dream). The plan is self-contained; implement to this spec.

---

## Canonical references (read with high attention)

- **Model Context Protocol (MCP):** [What is MCP?](https://modelcontextprotocol.io/docs/getting-started/intro) — MCP is an open-source standard for connecting AI applications to data sources, tools, and workflows. *"Think of MCP like a USB-C port for AI applications."* Clients (e.g. our demo backend) connect to MCP servers (ClickUp, Slack, Notion, filesystem) via stdio or Streamable HTTP; servers expose **tools**, **resources**, and **prompts**. [Architecture](https://modelcontextprotocol.io/docs/learn/architecture): client–server, primitives (tools/resources/prompts), transports (stdio, Streamable HTTP).
- **OpenAI Agents SDK (Python):** [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) — Production-ready agent framework: **Agents** (LLMs + instructions + tools), **Guardrails**, **Agents as tools / Handoffs**. Built-in **MCP server tool calling** (same as function tools), **agent loop**, **tracing**, **human-in-the-loop**. Use for all agent logic; connect prebuilt MCP servers via `mcp_servers=[...]` (HostedMCPTool, MCPServerStdio, MCPServerStreamableHttp).

---

## pipeline_demo folder — alignment (every document, every word)

The **`pipeline_demo/`** folder is the single source of truth for architecture, tool integration, and implementation. The React demo and backend must align to it.

| Document (in pipeline_demo/) | Content (summary) | How the React plan / demo aligns |
|-----------------------------|-------------------|----------------------------------|
| **aigenx_dragonfruit_agentic_architecture.pdf** (Batch 2) | Architecture philosophy: **Pipeline-First**, **Role-Aligned Agents**, **MCP-First API-Fallback**, **Human-in-the-Loop by Default**, **Async-First**, **Observable & Traceable**. Five layers: User Interface → Orchestration (OpenAI Agents SDK) → Tool binding (MCP client + function tools) → External systems. | Pipeline view = Layer 1; Phase → Role → Opportunity = pipeline-first; Run demo + reasoning + GIF = observable; HITL in ED-3 demo. |
| **aigenx_dragonfruit_agentic_architecture_part2-1.pdf** | Continued: agent taxonomy (Producer, PC, CD, PPM, Editor Support), handoffs, data flow, HITL gates, security, **Demo Mode & Mock Data Architecture**, tracing. | Mock data in `public/mock_data/`; Run demo (mock then live); tracing/reasoning in UI. |
| **batch3_role_playbooks_part1–3.pdf** | Role playbooks per Producer, PC, CD, PPM, Editor: tasks, tools, automation touchpoints. | Phase detail role cards; opportunity list per role; dream allocation and “Currently using” from survey. |
| **batch4_tool_integration_map_part1–2.pdf** | **Integration method per tool:** MCP (ClickUp, Slack, Notion), REST API/Function tool (Frame.io, YouTube, Dropbox), Webhook, Make/Zapier, Native. Tool-by-tool: spend, users, agent touchpoints. | tool_integration.json `integration_type` (MCP vs API); Opportunity detail “Integration” block; Batch 4 wiring (real MCP where available, API where not). |
| **batch5_impact_analysis_part1–2.pdf** | Impact analysis: time savings, dream allocation mapping, KPIs. | tool_dream_mapping.json; Dream allocation impact on Opportunity detail; time_allocations. |
| **batch6_implementation_roadmap_risk_framework_part1–2.pdf** | Phased roadmap, risk, buffers, rollout. | Batch order (1–5); Phase 1 quick wins; Phase 2 PR-4, ED-3; Phase 4 scale. |
| **aigenx_dragonfruit_proposal_master-1.pdf** | Master proposal: objective, quick wins, 16 tools, architecture, costs. | Proposal document and demo narrative match; same 8 high-priority tools and 16-tool wish list. |

**Rule:** Any new screen, tool, or integration in the demo must be traceable to pipeline_demo (architecture, role playbook, or tool integration map). When you receive real demo data for MCPs or APIs, plug it into: (1) backend env/config for MCP server URLs and API keys, (2) backend routes that call real MCP/API, (3) frontend labels “Live (MCP)” / “Live (API)”).

---

## Typography (apply everywhere)

| Use | Font |
|-----|------|
| **Headings** (titles, section labels, role names, phase names, priority badges, opportunity page headings) | Bebas Neue / Anton |
| **Body** (all other text: descriptions, values, links, meta, list text, breadcrumbs, tags inside tiles) | Inter / Helvetica |

**Where “everywhere” means:** Pipeline phase nodes (phase name, description, CTA), Phase detail (breadcrumb, phase title, “Roles in this phase”, each role card title, labels “CURRENTLY USING” / “DREAM ALLOCATION” / “OPPORTUNITIES”, body text in cards, **every opportunity tile** (priority badge + tool name), Opportunity detail page (breadcrumb, title, meta, all section titles, all paragraphs and lists). No screen or tile should fall back to generic system font.

---

## High-priority items (DFM wish list — all 8)

From `wishlist_tools.json` / DFM-REFERENCE, **high_priority**:

| ID | Name | Role | Solution must include |
|----|------|------|------------------------|
| **CD-1** | Predictive Retention Scoring | Creative Director | I/O, mock/live demo (curve + flags), reasoning, GIF (cd_agent_flow), MCP/API (Notion, retention APIs), dream |
| **CD-2** | Competitive Outlier Ideation Engine | Creative Director | I/O, mock/live demo (outlier digest), reasoning, GIF (cd_agent_flow), MCP/API (YouTube, ViewStats, Slack), dream |
| **CD-3** | Visual Packaging & Thumbnail Intelligence | Creative Director | I/O, mock/live demo (score + thumbnail text), reasoning, GIF (cd_agent_flow), MCP/API (vision, Slack), dream |
| **CD-4** | Competitor A/B Test Monitor | Creative Director | I/O, mock/live demo (changes + delta), reasoning, GIF (cd_agent_flow), MCP/API (YouTube, ViewStats, Slack), dream |
| **ED-1** | Frame.io Comment Sentiment Analyzer | Editor / PPM | I/O, mock/live demo (sentiment + alerts), reasoning, GIF (ppm_ed_flow), MCP/API (Frame.io, Slack), dream |
| **ED-2** | Automated Video QC Checker | Editor / PPM | I/O, mock/live demo (timestamped report), reasoning, GIF (ppm_ed_flow), MCP/API (QC service, ClickUp/Notion), dream |
| **ED-3** | Automated Capacity-Based Task Assignment | Producer / PC | I/O, mock/live demo (suggested assignees + HITL), reasoning, GIF (ed3_capacity_react_hitl), MCP/API (ClickUp, internal availability), dream |
| **PR-4** | Claude-to-ClickUp Agent | Producer | I/O, mock/live demo (NL → task create), reasoning, GIF (pr4_tool_use_react), MCP/API (ClickUp, optional Slack), dream |

**Requirement:** Each of the 8 has a dedicated Opportunity detail page with: tool name/id/role/priority, “This role today”, Input, Output, Run demo (mock then wire to backend where done), Reasoning block, **GIF iframe** (correct gif_id per tool_integration.json), Integration (MCP or API, tools used, description), Dream allocation impact. No high-priority tool is “coming later” or missing any of these sections.

---

## Batches (implementation order)

### Batch 1 — Data and theme (done)

- **Data:** phase_roles, tool_io, tool_integration, tool_dream_mapping, role_opportunities; wishlist_tools, time_allocations, ai_survey_summary. All 8 high-priority tools have entries in tool_io, tool_integration, tool_dream_mapping.
- **Theme:** Colors (#000000, #FFFFFF, #FF3B2E, etc.), **Bebas Neue / Anton** for all headings and labels, **Inter / Helvetica** for all body and tile text. Applied in: Layout, Pipeline (phase nodes), Phase detail (role cards + **opportunity tiles**), Opportunity detail (all sections).
- **GIFs:** public/gifs/ populated; tool_integration.gif_id set for CD-1..4, ED-1/2, ED-3, PR-4.

---

### Batch 2 — Pipeline and phase shell (done)

- **Pipeline:** Visual flow of phases; each phase node uses heading font for name/number and body font for description/CTA.
- **Phase detail:** Roles in phase; each role card uses heading font for role name and section labels, body font for values and dream text; **opportunity tiles** use body font for link text and heading font for priority badge.
- **Routing:** `/`, `/phase/:phaseId`, `/opportunity/:toolId`. All 8 high-priority tools reachable from at least one phase via role → opportunity link.

---

### Batch 3 — Opportunity detail: full solution for every tool

- **Single structure for every opportunity (all 16 tools; 8 high-priority must be complete):**
  - Header: name (heading font), id, role, priority (heading font for badge), description (body font).
  - “This role today” (survey) — body font.
  - Input list (tool_io) — body font.
  - Output list (tool_io) — body font.
  - **Reasoning / agent flow** — body font; text + optional backend-driven steps later.
  - **Run demo** — button; result area shows sample or live output (body font).
  - **Agent trajectory** — GIF iframe (gif_id from tool_integration); section title heading font.
  - **Integration** — MCP or API, tools used, description (body font); section title heading font.
  - **Dream allocation impact** — dream_impact_short, current_vs_dream (body font); section title heading font.
- **Checklist:** CD-1, CD-2, CD-3, CD-4, ED-1, ED-2, ED-3, PR-4 each have correct gif_id, full I/O, run demo (mock at minimum), reasoning block, integration block, dream block. Fonts applied to every element on the page.

---

### Batch 4 — Solutions for all 8 high-priority: Real MCP + OpenAI Agents SDK

- **Goal:** Each of the 8 has a **solution** the user can run (mock or live). **Prefer real prebuilt MCP servers** where applicable; where MCP is not available, use OpenAI Agents SDK with direct API and surface “MCP not available” in the UI. Run demo calls the backend and shows real or simulated output and reasoning.
- **OpenAI Agents SDK (primary framework):** [OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/). Use for all agent logic: tool calling, handoffs, tracing, human-in-the-loop. MCP tools are first-class: pass `mcp_servers=[...]` to `Agent()`; SDK supports HostedMCPTool, MCPServerStdio, MCPServerStreamableHttp, MCPServerSse.

#### 4.1 — Real MCP: where we use prebuilt MCP servers

| Tool / use case | Prebuilt MCP available? | Server / package | Config difficulty |
|-----------------|--------------------------|------------------|-------------------|
| **ClickUp** (PR-4, ED-3) | Yes (community) | e.g. `@nazruden/clickup-server` or `@taazkareem/clickup-mcp-server`; env: `CLICKUP_PERSONAL_TOKEN` | Easy: stdio or HTTP; run server, pass URL or command to SDK |
| **Slack** (CD-2, CD-3, CD-4, CD-5, CD-8) | Yes (official/community) | Official ref or community Slack MCP | Easy: env vars + stdio/HTTP in SDK |
| **Notion** (CD-1, CD-6, CD-7) | Yes (community) | Community Notion MCP implementations | Easy: token + server URL or stdio |
| **Filesystem** (demo / utility) | Yes (official) | `npx -y @modelcontextprotocol/server-filesystem /path` | Very easy: stdio, no auth; good for “config demo” |

**Deliverable:** Backend must **connect at least one real prebuilt MCP server** (e.g. ClickUp MCP for PR-4 and ED-3, or filesystem MCP for a config demo). Use `MCPServerStdio` (for npx/CLI servers) or `MCPServerStreamableHttp` (for HTTP MCP servers) in the OpenAI Agents SDK.

#### 4.2 — “Is it difficult to configure a prebuilt MCP server?” (show it’s not)

- **In-app / docs:** Add a small **“MCP configuration”** section (e.g. in Layout footer, or a `/mcp-config` info route, or a collapsible on Pipeline/Phase detail) that shows:
  1. **Choose a prebuilt server** (e.g. [MCP servers registry](https://github.com/modelcontextprotocol/servers), or npm: `@modelcontextprotocol/server-filesystem`, community ClickUp/Slack/Notion).
  2. **Run the server** — stdio example: `npx -y @modelcontextprotocol/server-filesystem ./allowed-dir`; or start a ClickUp MCP with `CLICKUP_PERSONAL_TOKEN` set.
  3. **Wire it in the SDK** — e.g. `MCPServerStdio(name="ClickUp", params={"command": "npx", "args": ["-y", "@nazruden/clickup-server"]})` (or equivalent); add to `Agent(mcp_servers=[...])`. Three steps; no custom protocol code.
- **Optional:** A minimal “Run MCP config demo” that starts the backend with a real stdio MCP (e.g. filesystem) and shows “Connected: Filesystem MCP” and one tool call result. This proves prebuilt MCP configuration is straightforward.

#### 4.3 — Where MCP is not available: use OpenAI Agents SDK + direct API

| Tool / use case | MCP available? | Approach |
|-----------------|----------------|----------|
| **Frame.io** (ED-1) | No (no widely adopted public MCP) | Agents SDK + function tools wrapping Frame.io REST API; UI shows “MCP not available — using Frame.io API”. |
| **YouTube / ViewStats** (CD-1–CD-4) | No | Agents SDK + function tools for YouTube Data API / ViewStats; UI shows “MCP not available — using YouTube/ViewStats API”. |
| **Internal QC / retention** (ED-2, CD-1) | No | Agents SDK + function tools (mock or real API); document in Integration section. |

**Deliverable:** For each such tool, Integration block and Run demo label (e.g. “Live (API)” or “Mock”) and a short line: “MCP not available for [X]; using [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) + [service] API.”

#### 4.4 — Wiring plan (order and backend)

- **PR-4:** Backend with OpenAI Agents SDK + **real ClickUp MCP** (prebuilt). Demo: NL → create_task; return task link + reasoning. **Priority 1.**
- **ED-3:** Backend with OpenAI Agents SDK + **real ClickUp MCP** (list_tasks, get_assignees) + mock availability. Demo: suggest assignees; HITL; show result. **Priority 2.**
- **CD-1:** Retention/analytics (mock or API) + **optional Notion MCP** if integrated. **Priority 3.**
- **ED-1:** Frame.io **API** (no MCP); document “MCP not available”. **Priority 4.**
- **ED-2:** QC (mock or API) + ClickUp/Notion (MCP or API). **Priority 5.**
- **CD-2, CD-3, CD-4:** YouTube/ViewStats **API** + **Slack MCP** for alerts; document “MCP: Slack only; YouTube/ViewStats via API”. **Priorities 6–8.**

- **Frontend:** “Run demo” calls backend (e.g. `/api/demo/:toolId` or `/api/run-pr4`). Show returned output and reasoning. Label: “Mock” | “Live (MCP)” | “Live (API)” so it’s clear when a real prebuilt MCP is used vs API-only.
- **Deliverable:** At least one **real prebuilt MCP server** connected (ClickUp MCP for PR-4/ED-3); “MCP configuration” guidance or demo in-app; all 8 have a path (MCP where available, API + SDK where not).

---

### Batch 5 — Trajectory page and polish

- **Trajectory route:** e.g. `/trajectory`. List all agent-flow GIFs (from tool_integration or a fixed list) with title/description; select one → iframe. Heading font for titles, body for descriptions.
- **Connection pills:** On home or layout: e.g. “Mock”, “ClickUp MCP”, “Slack MCP”, “OpenAI Agents SDK”, “Frame.io API (no MCP)” so it’s clear what uses **real prebuilt MCP** vs API-only. Link to MCP config section if present. Body or small heading font.
- **Polish:** Focus states, consistent spacing, no missing fonts. Verify every tile and card in the app uses Bebas Neue/Anton for headings and Inter/Helvetica for body. RUN.txt and START.command kept; server redirect IP→localhost so no blank on IP.

---

## Summary

- **Fonts:** Bebas Neue / Anton for every heading and label; Inter / Helvetica for every body and tile. Applied inside pipeline nodes, role cards, **opportunity tiles**, and every section of the opportunity detail page.
- **High-priority:** All 8 (CD-1, CD-2, CD-3, CD-4, ED-1, ED-2, ED-3, PR-4) have a full solution: I/O, run demo, reasoning, GIF, integration, dream. Batch 4 wires **real prebuilt MCP** where available (ClickUp, Slack, Notion) and **OpenAI Agents SDK** for all agent logic; where MCP is not available (Frame.io, YouTube), use SDK + direct API and surface "MCP not available" in the UI.
- **Real MCP:** Backend must connect at least one real prebuilt MCP server (e.g. ClickUp MCP for PR-4/ED-3). Show that **configuring a prebuilt MCP is not difficult** (3 steps: choose server → run server → pass to Agent in SDK); optional in-app "MCP config" section or minimal "Run MCP config demo" using e.g. filesystem MCP.
- **Batches:** 1 Data/theme/fonts everywhere, 2 Pipeline/phase/tiles, 3 Opportunity full solution for every tool, 4 Real MCP + SDK (with MCP config demo), 5 Trajectory + polish.
