# MVP Streamlit Plan — Dragonfruit AI & Automation Demo

**Goal:** Build a beautiful, compelling Streamlit MVP that (1) uses the color scheme from the attached Winning Proposal PDF, (2) has multiple tabs and role-centric views, (3) lists tools per role with mock demos, (4) clarifies MCP vs env API keys, (5) surfaces the GIF/HTML trajectory (agent start→finish), and (6) ties every use case to **dream allocation** so value is explicit.

---

## 1. Color scheme and UI

- **Source:** Apply palette from **Winning_Proposal_Document_f715f6b4.pdf** (user-attached). If that PDF uses different hex values than our current Dragonfruit set, we will:
  - Extract or infer primary, accent, background, and text colors from the PDF (or use existing **COLOR_PALETTE.md** / proposal HTML if PDF is not machine-readable).
  - Current Dragonfruit palette in app: `--df-accent: #E85D75`, `--df-bg: #FAFAFA`, `--df-surface: #FFFFFF`, `--df-text: #1a1a1a`, `--df-text-muted: #64748B`, Plus Jakarta Sans.
- **UI principles:** Premium, clean, bold; hero sections per section; pill badges for connection status and role; cards for each tool; tabs for Run Demo (by tool) and by Role; sidebar for nav + Connections (Mock, ClickUp, Slack, Frame.io, Notion). No clutter; every screen should answer “what does this role get?” and “how does this move us toward dream allocation?”

---

## 2. Top-level structure (tabs and pages)

| Area | Purpose |
|------|--------|
| **Run Demo** | Tabbed by **tool** (Overview, CD-1…CD-4, ED-1…ED-3, PR-4) — current behavior, kept and enhanced. |
| **By Role** | **New.** One tab per role: Producer, Production Coordinator, Creative Director, Post-Production Manager, Editor. Each tab: (1) role name + dream allocation one-liner, (2) **Tools this role uses** (from wish list + DFM-REFERENCE), (3) input/output per tool (from Wish List DOCX), (4) mock demo buttons that run with mock data and show result. |
| **Time Allocations** | Current vs dream by role (existing), add a short “How tools support dream” callout per role. |
| **Pipeline** | Existing overview; optional “Where agents plug in” from Appendix 2. |
| **Proposal Summary** | Existing; link to full proposal HTML/PDF. |
| **Agent Trajectory (GIFs)** | **New.** Single page that explains agent flow start→finish and **embeds or links** to the GIF folder HTMLs so reviewers see the trajectory. |
| **Wish List & Tools** | Existing; add “by role” grouping so each role’s tools are listed together. |

---

## 3. Roles and tools (from DFM-REFERENCE)

From **AI Tool Wish List (DOCX)** and **AI Tool Survey (PPTX)**:

| Role | Tools (IDs) | One-line dream link |
|------|------------|----------------------|
| **Producer** | PR-1, PR-2, PR-3, PR-4 | ClickUp 38%→18%; Slack 17%→10%; freed time → Client Strategy, Innovation Lab. |
| **Production Coordinator** | PR-3, PR-4, ED-3 (assign) | Coordination 70%→40%; “Free time” ~10% for extra client capacity. |
| **Creative Director** | CD-1, CD-2, CD-3, CD-4, CD-5, CD-6, CD-7, CD-8, CD-9 | Preproduction → 50%; V1/admin → 0%; more creative 1:1s. |
| **Post-Production Manager** | ED-1, ED-2, ED-3 | Reviews 35% / Editor Mgmt 30% / Hiring+Onboarding 15%; less manual QC. |
| **Editor** | ED-1 (sentiment view), ED-2 (QC report), ED-3 (assignee) | Core editing 66%→80%; idle 6.5%→2%; fewer revisions. |

Each tool in the app will show **input** and **output** as defined in the Wish List DOCX (e.g. CD-1: input = script, channel context, format; output = retention curve, drop-off flags, suggestions).

---

## 4. Input/output per tool (from DFM-REFERENCE Wish List)

We already have descriptions in `mock_data/wishlist_tools.json`. We will add an **input_output** structure (from the DOCX) so the UI can show “Input” and “Output” per tool:

| Tool | Input (from brief) | Output (from brief) |
|------|--------------------|---------------------|
| CD-1 | Script text, outlier script data, channel context, video format | Retention curve prediction, drop-off risk flags, improvement suggestions (incl. opening hook) |
| CD-2 | List of competitor channel URLs | Weekly digest of outlier videos, why they outperformed, theme/format/timing |
| CD-3 | Title + thumbnail image (or script) | Score + critique; thumbnail text candidates; shelf strategy |
| CD-4 | Competitor config | Title/thumbnail/description changes + performance delta; Slack alerts |
| ED-1 | Frame.io comments (per video / per client) | Video-level sentiment; client-level trend; alert if below threshold |
| ED-2 | Video export + client checklist | Timestamped error report (severity, rule) |
| ED-3 | ClickUp tasks + editor workload/skill/pod | Suggested assignees; human confirms |
| PR-1 | Content type, deliverables, complexity, turnaround | Schedule + milestones + buffer |
| PR-2 | Slack/email/Frame.io comms | Running sentiment per client; escalation flags |
| PR-3 | Template key + client/project vars | Templated message (kickoff, status, revision, reminder) |
| PR-4 | Natural language command | Proposed ClickUp task (fields, list, assignee, due); HITL confirm → create |

This table will drive (1) mock_data schema additions and (2) Streamlit “Input / Output” expanders per tool in Run Demo and By Role.

---

## 5. MCP vs env API keys — what we need

- **Env already has API keys:** We use them in **connectors** (function tools). No change required for MVP: ClickUp, Slack, Frame.io, Notion continue to use `.env` (e.g. `CLICKUP_API_KEY`, `SLACK_BOT_TOKEN`, `FRAMEIO_ACCESS_TOKEN`, `NOTION_API_KEY`). The app already checks `_connector_status()` and shows Connected / Demo mode.
- **MCP (what we need):**
  - **Mock context:** **Dragonfruit Mock Data MCP** (`mcp_servers/dragonfruit_mock_server.py`) — exposes `mock_data/*.json` as tools/resources. Used so agents (when running with SDK) can read pipeline, allocations, pods, wish list. For the Streamlit UI we don’t run MCP; we just load the same JSON. So for “mock demo” we **don’t need** to run the MCP server in the Streamlit process; we only need it when running the Producer (or other) agent with the SDK and want the agent to query mock data via MCP.
  - **ClickUp / Slack / Notion / Frame.io:** For **production** we can switch to **official MCPs** (ClickUp, Slack, Notion) or **build a thin Frame.io MCP**. For **MVP with env API keys**, we keep using **connectors** (function tools). The plan doc and sidebar can say: “Connections: Mock data (local JSON); ClickUp/Slack/Frame.io/Notion via .env API keys. Optional: attach official MCPs in SDK for production.”
- **Summary for Streamlit:** No new MCP setup required for the MVP. Env keys → connectors; mock data → `load_json()`. We add one **“MCP & connections”** subsection in the app (e.g. under Run Demo → Overview or in sidebar) that explains: “Today: API keys in .env drive ClickUp/Slack/Frame.io/Notion. Mock data from `mock_data/`. For agent runs with context, use Dragonfruit Mock Data MCP; for production, optional swap to official ClickUp/Slack/Notion MCPs.”

---

## 6. GIF / trajectory (GIF folder)

- **GIF folder:** `proposal_contract/GIFs/` — 9 HTML files (animated, not static GIFs). They show:
  - **agentic_architecture_animated.html** — Full 4-layer architecture (triggers → agents → connectors → external).
  - **producer_agent_flow_animated.html** — Producer: goal → task decompose → ClickUp → Slack → Frame.io → output.
  - **cd_agent_flow_animated.html** — CD: script → CD-1 → CD-2 → CD-4.
  - **ppm_ed_flow_animated.html** — PPM/ED: Frame.io → ED-1 → ED-2 → ED-3, with HITL.
  - **high_priority_tools_animated.html** — All 8 high-priority tools, role + input + output.
  - **sdk_primitives_numbered_agents.html** — SDK primitives, agents 1–5, handoffs, HITL.
  - **multi_agent_handoffs_orchestrator.html** — Producer orchestrator, handoffs to PC/CD/PPM.
  - **pr4_tool_use_react.html** — PR-4 ReAct + tool call + HITL confirm.
  - **ed3_capacity_react_hitl.html** — ED-3 capacity + HITL.
- **In Streamlit we can’t run HTML inline.** Options:
  - **A:** Add an **“Agent trajectory”** page with short descriptions of each flow and **links** to open the HTML files (e.g. `file:///.../GIFs/agentic_architecture_animated.html` or a path we serve). Label: “Open in browser to see full trajectory (start → finish).”
  - **B:** Serve the GIFs folder via a tiny static server (e.g. `streamlit run` with `--server.enableStaticServing` and mount `GIFs/`) and embed in an **iframe** (if Streamlit allows iframe to local files).
  - **C:** Export key frames as static images (or record short GIFs) and show those in the app with “Full animation: see proposal_contract/GIFs/”.
- **Recommendation:** **A + C.** (1) New **“Agent trajectory”** nav item: for each of the 4–5 “main” flows (architecture, producer flow, CD flow, PPM/ED flow, PR-4 ReAct), show a short bullet list + a static image or placeholder + “**View full animation:** [Open agentic_architecture_animated.html](path).” (2) Ensure paths are relative to project root so “Open” works when the user opens the HTML in a browser. No need to run a separate server if we document “double‑click the HTML in `proposal_contract/GIFs/`”.

---

## 7. Mock demo — show it works

- **Data:** All mock data lives in `mock_data/*.json` (pipeline_stages, pods_and_clients, time_allocations, wishlist_tools, tool_stack). We already use it in Run Demo tabs.
- **Enhancements:**
  - **Consistent input/output:** For each tool tab (and each role’s tool list), show an “Input” and “Output” section. Use the table in §4; for mock runs, prefill realistic inputs (e.g. sample script for CD-1, sample task list for ED-3) and show deterministic mock outputs (retention curve, outlier table, QC report, suggested assignees, proposed ClickUp task).
  - **Dream allocation callout:** On Overview and on each role tab, add one line: “This supports dream allocation: [e.g. Producer ClickUp 38%→18%].”
  - **Connection status:** Keep Mock ✅ and ClickUp/Slack/Frame.io/Notion from env; when an env key is set, show “Connected” and, where applicable, run real API (e.g. PR-4 create task in ClickUp when `CLICKUP_*` set).
- **No hallucination:** All copy for “input/output” and “dream allocation” comes from DFM-REFERENCE (Wish List DOCX, Dream Allocations XLSX). We can add `mock_data/role_tools.json` that maps role → list of tool IDs + one-line dream text.

---

## 8. Batched work plan

| Batch | Scope | Deliverables |
|-------|--------|--------------|
| **Batch 1 — Data & config** | Input/output and role→tools mapping from DFM-REFERENCE; color from Winning PDF if needed. | (1) Extend `mock_data/wishlist_tools.json` or add `mock_data/tool_io.json` with input/output per tool. (2) Add `mock_data/role_tools.json`: role → tools[] + dream_one_liner. (3) If Winning PDF colors differ, add to `COLOR_PALETTE.md` and a small `theme.py` or CSS snippet. |
| **Batch 2 — By Role page** | New “By Role” section in Streamlit: one tab per role (Producer, PC, CD, PPM, Editor). Each tab: role name, dream one-liner, list of tools with short description + Input/Output (from §4), and a “Run mock” button per tool that uses existing mock logic (or minimal stub). | (1) New nav item “By Role”. (2) Five role tabs; each shows tools from `role_tools.json` and `wishlist_tools` + input/output. (3) Buttons that expand or navigate to the same mock used in Run Demo (or inline mini demo). |
| **Batch 3 — Run Demo polish** | Align Run Demo tabs with DFM-REFERENCE input/output; add dream allocation one-liner on Overview; ensure every tool tab shows Input / Output. | (1) Overview: “Dream allocation” sentence per role. (2) Each tool tab: Input (bullet list), Output (bullet list or chart/table). (3) Reuse existing mock runs; no new backends. |
| **Batch 4 — Agent trajectory (GIFs)** | New “Agent trajectory” nav; describe start→finish for 4–5 flows; link to GIF folder HTMLs. | (1) Nav “Agent trajectory”. (2) Sections: Full architecture, Producer flow, CD flow, PPM/ED flow, PR-4 ReAct, ED-3 capacity. (3) Each section: 2–3 bullet description + “View animation: open `proposal_contract/GIFs/<file>.html` in browser.” (4) Optional: static image or placeholder per flow. |
| **Batch 5 — MCP & connections copy** | One place in the app that explains MCP vs env. | (1) Run Demo → Overview (or sidebar): short “MCP & connections” block. (2) Copy: env keys = connectors (ClickUp, Slack, etc.); mock = local JSON; optional Mock Data MCP for agent context; production = optional official MCPs. |
| **Batch 6 — UI polish & color** | Apply Winning Proposal color scheme if provided; ensure all tabs and role views are consistent and compelling. | (1) CSS variables from COLOR_PALETTE or PDF. (2) Hero, cards, pills, tables consistent. (3) Wish List page: group tools by role. (4) Footer and sidebar labels clear. |

---

## 9. How we build all use cases and show value (dream allocation)

- **Use cases = 16 tools** (8 high + 8 medium). Each has a **Run Demo** tab and appears under **By Role** for the role(s) that use it. We don’t need 16 separate backend services; we need:
  - **One** mock path per tool: when user clicks “Run” we either (a) call existing mock (e.g. CD-1 retention curve, ED-2 QC table, ED-3 assignees, PR-4 proposed task) or (b) show a stub “Output: [from DFM-REFERENCE]” with sample data.
  - **Shared data:** `mock_data/` + optional Dragonfruit Mock Data MCP when running agents.
- **Value = dream allocation.** For every tool we show:
  - **Producer/PC:** “Reduces ClickUp/Slack time (38%→18%, 17%→10%); frees time for Client Strategy and Innovation Lab.”
  - **CD:** “Moves preproduction toward 50%; reduces V1/admin so you focus on creative 1:1s.”
  - **PPM:** “Less manual QC; dream split Reviews 35% / Editor Mgmt 30% / Hiring+Onboarding 15%.”
  - **Editor:** “Fewer revisions and less idle; core editing 66%→80%.”
- **Placement:** (1) Run Demo → Overview: one sentence per role. (2) By Role: dream one-liner at top of each role tab. (3) Per-tool: in the tool card or under the output, one short line “Supports: [dream outcome].”

---

## 10. Summary

| Item | Approach |
|------|----------|
| **Color scheme** | From Winning_Proposal_Document PDF (or keep current Dragonfruit palette). |
| **Tabs** | Run Demo (by tool), **By Role** (new), Time Allocations, Pipeline, Proposal Summary, **Agent trajectory** (new), Wish List. |
| **Roles** | Producer, PC, CD, PPM, Editor — each lists tools and dream one-liner. |
| **Tools per role** | From wish list + `role_tools.json`; input/output from DFM-REFERENCE. |
| **MCP** | Env API keys = connectors (no change). Mock = local JSON. Optional Mock Data MCP for agent context. Copy in app. |
| **Mock demo** | Existing mock data + mock runs; add Input/Output labels and dream callouts. |
| **GIF/trajectory** | New “Agent trajectory” page: describe 4–5 flows, link to `proposal_contract/GIFs/*.html` to open in browser. |
| **Dream allocation** | One-liner per role on Overview and By Role; per-tool “Supports: …” where relevant. |
| **Batches** | 6 batches: data/config → By Role → Run Demo polish → Agent trajectory → MCP copy → UI/color. |

Once you confirm this plan, implementation can start with **Batch 1** (data + role→tools + optional color), then **Batch 2** (By Role page), and so on.
