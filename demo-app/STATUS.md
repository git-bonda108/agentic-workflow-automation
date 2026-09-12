# Pipeline Demo — Build Status

## Already built

### Batch 1 — Data and theme
- **Data (public/mock_data/):** phase_roles.json, tool_io.json, tool_integration.json, tool_dream_mapping.json, role_opportunities.json, wishlist_tools.json, time_allocations.json, ai_survey_summary.json, pipeline_stages.json. All 8 high-priority tools have I/O, integration, and dream mapping.
- **Theme:** Colors (#000000, #FFFFFF, #FF3B2E, etc.) in `src/theme/colors.css`.
- **Typography:** Bebas Neue / Anton (headings) and Inter / Helvetica (body) in `index.html` and CSS; applied to Layout, Pipeline, Phase detail (role cards + opportunity tiles), Opportunity detail (all sections).
- **GIFs:** All 9 HTML animations in `public/gifs/` (e.g. cd_agent_flow_animated, pr4_tool_use_react, ed3_capacity_react_hitl). `tool_integration.json` has `gif_id` per tool.

### Batch 2 — Pipeline and phase shell
- **Pipeline view:** Phases as a horizontal flow; click phase → Phase detail. Fonts applied to phase names, numbers, descriptions, CTA.
- **Phase detail:** For each phase, list of roles; each role card shows: role name, “Currently using” (survey), “Dream allocation” (key_notes), list of **opportunity tiles** (priority badge + tool name) linking to `/opportunity/:toolId`. Fonts applied inside every card and tile.
- **Routing:** `/`, `/phase/:phaseId`, `/opportunity/:toolId`. All 16 tools (including 8 high-priority) reachable from phase → role → opportunity.

### Batch 3 — Opportunity detail (full solution UI)
- **Single structure for every tool:** Header (name, id, role, priority), “This role today”, Input list, Output list, **Reasoning / agent flow** block, **Run demo** button (mock: sample input → output from tool_io), **Agent trajectory** (GIF iframe from tool_integration.gif_id), **Integration** (type, tools, description), **Dream allocation impact**. Data loaded from mock_data for any `:toolId`; all 8 high-priority have correct gif_id and full sections.
- **Run demo:** Mock only (button shows sample I/O). No backend call yet.

### Infrastructure
- **Vite:** Redirect non-localhost → localhost so IP doesn’t show blank.
- **START.command:** Starts dev server, opens browser after delay; RUN.txt has run instructions.
- **Error handling:** Error boundary, global onerror/unhandledrejection in index.html.

---

## Built in this pass (Batch 4 & 5)

### Batch 4 — Live solutions (real MCP + OpenAI Agents SDK)
- **Backend:** FastAPI in `backend/main.py`. `GET /api/demo/{tool_id}` returns output, reasoning, `source` (mock | mcp | api), and optional `task_link`. PR-4 and ED-3 use ClickUp REST API when `CLICKUP_API_KEY` is set; otherwise mock from MCP SYNTHESIZED DATA. `GET /api/clickup/workspace` and `GET /api/clickup/synthesized/{name}` serve synthesized data.
- **Frontend:** “Run demo” does not call any backend; no “Live (MCP)” / “Live (API)” path, no display of backend-returned reasoning or task link.
- **To build (see REACT_DEMO_PLAN.md Batch 4):**  
  1. **Real prebuilt MCP:** Connect at least one real prebuilt MCP server (e.g. ClickUp MCP: `@nazruden/clickup-server` + `CLICKUP_PERSONAL_TOKEN`) via OpenAI Agents SDK. PR-4 and ED-3 use real ClickUp MCP; CD-2–CD-4 use Slack MCP where applicable.  
  2. **MCP config demo:** In-app "MCP configuration" section or minimal "Run MCP config demo" (e.g. filesystem MCP) to show prebuilt MCP config is straightforward.  
  3. **Where MCP not available:** Use SDK + direct API for Frame.io, YouTube/ViewStats; label "MCP not available — using [service] API" in UI.  
  4. Backend routes for PR-4, ED-3 (then others). Frontend: label "Mock" | "Live (MCP)" | "Live (API)".

### Batch 5 — Trajectory page and polish
- **Trajectory page:** `/trajectory` lists agent-flow GIFs; select one → iframe. Fonts and theme applied.
- **Connection pills:** No “Mock”, “ClickUp MCP”, “OpenAI Agents SDK”, etc. on home or layout.
- **Polish:** No formal pass for focus states, spacing, or “every tile/card uses correct font” verification.

---

## Summary

| Batch | Status | What’s done | What’s left |
|-------|--------|-------------|-------------|
| **1** | Done | Data, theme, fonts everywhere, GIFs in public | — |
| **2** | Done | Pipeline flow, Phase detail, role cards, opportunity tiles, routing | — |
| **3** | Done | Opportunity detail: full UI for every tool (I/O, reasoning, run demo mock, GIF, integration, dream) | — |
| **4** | Done | Backend API, Run demo wiring, source badge, MCP config page | Wire real ClickUp/Slack MCP when keys available |
| **5** | Done | Trajectory page, connection pills, focus states, card hover, RUN.txt | — |

**Next steps (optional):** Add more real integrations (Slack, Notion, etc.) when keys are available. ClickUp MCP is verified in IDE and backend uses REST API for PR-4/ED-3; see **MCP_VERIFICATION.md**.
