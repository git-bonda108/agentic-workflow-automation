# DFM-REFERENCE Summary: Document Expectations, Agentic Opportunities, and Tech Recommendations

This document summarizes what is expected from each reference document in **DFM -REFERENCE**, maps agentic AI opportunities to benefits, documents the toolkit and dream allocations per role, and provides an honest recommendation on the OpenAI Agents SDK and MCP strategy. All content is grounded in the extracted PDF, PPTX, XLSX, and DOCX materials—no invented data.

---

## 1. What Is Expected for Each Document

### 1.1 Execution Brief (PDF / PPTX)

**Documents:** `Dragonfruit_AI_Automation Enabled Pipeline & System Architecture Brief.pdf`, `Dragonfruit_AI_Automation Enabled Pipeline & System Architecture Brief .pptx`

**Purpose:** Define what the proposal must include and how it will be evaluated.

**Expected use:**

- The proposal must address **four requirement areas:**
  - **A — System architecture & vision:** Map the current pipeline and identify every automation opportunity; define where agentic workflows could be implemented (e.g. Claude-to-ClickUp MCP, Slack routing agents, automated QC); recommend which integrations to build vs replace or add; include a diagram or system map.
  - **B — AI toolkit per role:** Recommend specific AI tools for each of the 5 core roles based on survey data and dream allocations (reference the Wish List); justify each tool (cost, capability, learning curve); account for current adoption (e.g. editors as power users, CDs with knowledge gap); include licensing/cost estimates per tool.
  - **C — Implementation roadmap:** Phased rollout with milestones and timelines; quick wins (first 30 days) vs longer-term builds; measurable KPIs per phase; risk mitigation (human-in-the-loop, rollback); training and adoption plan per role.
  - **D — Costs & engagement structure:** Rate structure (hourly, retainer, project-based, or hybrid); estimated total labour cost; system architecture costs (tools, integrations, infrastructure, ongoing maintenance); cadence, communication, decision-making; team composition.
- **Evaluation criteria (due March 13th):** Specificity to workflow 30%, Clarity of architecture 25%, Realistic roadmap 20%, Cost transparency 15%, Engagement fit 10%.
- **Objective (from brief):** Scale pod capacity from 4 → 7 clients by EOY 2026 without proportional headcount increase, via workflow automation, agentic infrastructure, and the AI wish list toolkit.

**Critical refs:** The “Materials Provided” section states that all other reference documents are mandatory inputs. The brief explicitly names “Claude-to-ClickUp MCP” and “Slack routing agents, automated QC” as examples of agentic workflows.

---

### 1.2 AI Tool Wish List (DOCX)

**Document:** `DFM_AI_Tool_Wishlist_Consultant_Brief_Updated.docx`

**Purpose:** Consultant brief for recommended approach (build vs buy vs configure), timeline, maintenance, and cost range per tool.

**Expected use:**

- For **each tool** in the wish list, the proposal should include: recommended approach (build vs buy vs configure), estimated development timeline, ongoing maintenance requirements, and approximate cost range.
- Justify why each tool was selected and how tools can **share underlying infrastructure**.
- Primary systems to integrate: **ClickUp** (project management), **Frame.io** (review), **Slack** (internal and client communication). Any tools built should integrate with these.
- Mix of approaches: bespoke tools where off-the-shelf does not exist; configured SaaS where it does; lightweight automations (Zapier, Make, custom bots) for integration glue.
- **Tool categories in the wish list:** Creative Director (CD-1–CD-5), Editor/PPM (ED-1–ED-5), Producer (PR-1–PR-4), Finance & Accounting (FA-1–FA-5), HR & Recruitment (HR-1–HR-5), Internal Ops (IO-1). The proposal’s “16-tool core” focuses on CD, ED, and PR tools; FA, HR, and IO can be scoped as Phase 5 or a separate engagement.

---

### 1.3 AI Tool Survey — Role Breakdown (PPTX)

**Document:** `DFM_AI_Tool_Survey_Role_Breakdown.pptx`

**Purpose:** Evidence base for tool choice and adoption strategy by role.

**Expected use:**

- Justify tool selection and **training** by role using survey data (73 respondents, 5 core roles):
  - **Editors (46, 63%):** Power users; need creative tools (video, image, audio generation). Top tools: ChatGPT 89%, Gemini 67%, Freepik, ElevenLabs, Adobe Firefly. Use cases: ideation, image gen, video gen, audio/voice, frame extension, code/expressions. Top requests: ChatGPT Paid, Higgsfield, Gemini Premium.
  - **Production Coordinators (9, 12%):** Use AI for communication, not creation. ChatGPT 100%; use cases: client comms, captions, reports, task management. “Anything that can cut down task time is good by me.”
  - **Creative Directors (5, 7%):** All use ChatGPT; many have not explored beyond it. “I haven’t sat down to learn the other tools despite knowing they’re highly valuable.” Need discovery and training; ideation, scripting, thumbnail mockups.
  - **Post-Production Managers (4, 5%):** 100% ElevenLabs; heaviest Runway users. Use cases: audio fixes, SOPs, video concepting, team support. Top requests: ChatGPT Paid, Midjourney, Runway.
  - **Producers (4, 5%):** 50% use Claude (highest of any role). Strategic planning, client research; “ChatGPT primarily as a strategic thinking partner.” Both Claude users want DFM to provide it company-wide.
- Avoid “one size fits all”; tailor AI investments by role to maximize ROI. Reference specific tools and respondent quotes where it strengthens the proposal.

---

### 1.4 Current Pipeline Tool Stack (XLSX)

**Document:** `DFM Current Pipeline Tool Stack.xlsx`

**Purpose:** Inventory of existing tools, subscription spend, and role coverage.

**Expected use:**

- Proposals must **not ignore** the current stack: ~**$12.8K/month** across 40+ subscriptions (SaaS Bills sheet).
- Recommend a **“layer on top”** of existing systems (ClickUp, Notion, Frame, Slack, Make, Dropbox, etc.), not wholesale replacement.
- Reference **who uses what** (e.g. ClickUp: CD, Data Analyst, Editor, PPM, Producer, PC, Publisher, Scriptwriter, Thumbnail Designer) for adoption planning and licensing.
- Identify which integrations to **extend** (e.g. Make, Zapier for ClickUp↔Slack) and where new AI/tooling sits relative to current spend.

---

### 1.5 Current vs Dream Time Allocations (XLSX)

**Document:** `DFM_Current_vs_Dream_Time_Allocations.xlsx`

**Purpose:** Define efficiency gaps and target state per role (50-hour work week, 7 clients per pod).

**Expected use:**

- Every automation and agent recommendation must map to a **concrete time shift** from the audit. Example (Producers): coordination 74.5% → 41%; ClickUp 38% → 18% with “Claude-to-ClickUp MCP”; Internal Meetings 20% → 15%; Slack 17% → 10%; freed time → Client Strategy, Production Strategy & QC, Innovation Lab.
- **KPIs** should align to: “Zero increase in missed deadlines or client escalations vs control pod”; time allocation within ~10% of dream targets.
- Use the **rationale** in the sheets (e.g. “Slack-to-ClickUp routing automated,” “AI auto-generates from ClickUp,” “Human-in-the-loop review”) to justify each tool or workflow.
- Sheets: **Producers**, **Production Coordinators**, **Post-Production Managers**, **Creative Directors**, **Editors** — each has current % of capacity, dream %, and notes/rationale.

---

### 1.6 Current Pipeline (XLSX)

**Document:** `DFM Current Pipeline.xlsx`

**Purpose:** Single source of truth for end-to-end workflow and automation touchpoints.

**Expected use:**

- Map every **stage** (Onboarding, Pre-Production, Production, Post-Production, Publish) to: responsible role, general task, specific actions, software, and “Automation or AI tool used.”
- Identify where **agents and tools plug in:** e.g. Producer “Updates ClickUp,” “applies template batch,” “assigns tasks”; PPM “reviews,” “leaves feedback” on Frame.io; CD “reviews Roadmap,” “approves”; YPC “shares link to Client,” “notifies publisher”; Make/Zapier for subtask creation, status webhooks, editor linking.
- Use the pipeline to ensure the proposal’s architecture diagram and tool list **cover every step** that has automation potential and to avoid generic advice.

---

## 2. Agentic AI Opportunities and How They Drive Benefits

| Opportunity | Where it appears | Benefit |
|-------------|------------------|--------|
| **Claude-to-ClickUp agent (PR-4)** | Brief, Wish list, Dream allocations | Cuts Producer/PC ClickUp admin (38%→18%); batch setup, statuses, routing; human-in-the-loop for task create/assign. |
| **Slack routing / templates (PR-3)** | Brief, Wish list, Dream allocations | Reduces ad-hoc Slack (17%→10%); templated kickoffs, status, revisions; one source of truth with ClickUp. |
| **Frame.io sentiment (ED-1)** | Wish list, Pipeline | Video-level + client-level sentiment; early escalation; less reactive firefighting for PPMs. |
| **Automated QC (ED-2)** | Wish list, Pipeline | Client checklist → timestamped report; fewer missed items and revision cycles; frees PPM time for reviews/1:1s. |
| **Capacity-based assignment (ED-3)** | Wish list, Dream allocations | ClickUp + workload + skill/pod → suggested assignees; human confirms; replaces manual PC assignment. |
| **Predictive retention (CD-1)** | Wish list | Script → predicted retention curve; “AI focus group”; better structure before production. |
| **Outlier ideation (CD-2)** | Wish list, Pipeline | Competitor scripts/patterns; weekly digest; feeds CD-1 and ideation. |
| **Packaging/thumbnail (CD-3)** | Wish list | Thumbnail analysis + script→thumbnail text; shelf strategy. |
| **A/B test monitor (CD-4)** | Wish list | Competitor title/thumbnail/description + performance; Slack alerts. |
| **Timeline calculator (PR-1)** | Wish list, Quick wins | Content type, deliverables, complexity, turnaround → schedule; reduces manual date-setting. |
| **Client sentiment tracker (PR-2)** | Wish list | Cross-channel (Slack, email, Frame.io) sentiment; proactive relationship risk. |
| **Client knowledge bases (CD-6)** | Wish list | Claude Projects (or equivalent) per client; on-brand, consistent ideation and reference. |

**Agentic infrastructure (per brief):** Agents for task routing, status updates, feedback distribution, and content-prep workflows; each role (Producer, PC, CD, PPM) gets an agent with defined scope and **human approval at critical steps**.

---

## 3. Toolkit and Dream Allocation (From the Documents)

### 3.1 Tools in the toolkit (Wish list + Proposal)

- **16-tool core (proposal):** CD-1–CD-9, ED-1–ED-3, PR-1–PR-4. PR-1 (Timeline calculator) and PR-3 (Slack templates) are quick wins (first 30–35 days).
- **Wish list also includes:** FA-1–FA-5 (invoicing, late reminders, reports, pricing optimizer, modelling assistant), HR-1–HR-5 (resume screening, hiring pipeline, onboarding, HR Q&A bot, leadership reporting), IO-1 (IT support bot). These can be scoped as “Phase 5” or a separate engagement.

### 3.2 Dream allocation per role (from XLSX)

- **Producers:** ClickUp 38%→18%; Internal Meetings 20%→15%; Slack 17%→10%; freed time → Client Strategy, Production Strategy & QC, Innovation Lab. Key note: “Deploy AI-assisted automation layer (Claude to ClickUp MCP) for routine task creation, batch setup, status updates, Slack-to-ClickUp routing.” Coordination overhead 74.5%→41%.
- **Production Coordinators:** Coordination down; “Free time (additional client allocation)” ~10%; YouTube Publishing maintained; agenda prep reduced via AI from ClickUp.
- **Post-Production Managers:** Slack/internal comms reduced; Onboarding 2%→15% (freed admin time redirected); dream split: Reviews 35% / Editor Management 30% / Hiring+Onboarding 15%.
- **Creative Directors:** Preproduction toward ~50%; onboarding one-time (0% recurring); Slack reduced; more creative 1:1s.
- **Editors:** Core editing 66%→80%; idle 6.5%→2%; revisions reduced with clearer briefs and capacity-based assignment.

---

## 4. OpenAI Agents SDK — Honest Recommendation

**Recommendation: Use the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)** for the agentic layer, consistent with the existing [AGENTIC_PLAN.md](AGENTIC_PLAN.md).

**Reasons (from the brief and SDK docs):**

- **Agents + tools:** One agent per role (Producer, PC, CD, PPM) with instructions and tools fits the brief. Built-in agent loop (tool call → LLM → next step) reduces custom orchestration.
- **MCP server tool calling:** The SDK provides “built-in MCP server tool integration that works the same way as function tools.” ClickUp, Slack, and Notion can be attached via official MCPs where available; function tools cover the rest.
- **Handoffs / agents as tools:** Producer as orchestrator delegating to PC, CD, PPM matches “agentic workflows” and “task routing, status updates, feedback distribution.”
- **Human-in-the-loop and guardrails:** The brief and dream allocations require approval at task create, assign, client message, QC escalation; the SDK supports these patterns.
- **Sessions / context:** Persistent context per run supports “current tasks for Mango Pod” and multi-step flows.
- **Python-first, few primitives:** Aligns with the existing codebase (connectors, Streamlit, mock data).

**Alternatives considered (honest):**

- **LangGraph / LangChain:** More flexible but more moving parts; for “concrete system we can hand to an engineer,” the SDK’s smaller surface is an advantage.
- **CrewAI / AutoGen:** Heavier; the brief asks for clear role boundaries and connector-centric tools, which the SDK already models.
- **Raw MCP only:** No agent loop, memory, or guardrails out of the box; we would rebuild what the SDK provides.

**Conclusion:** Keep the OpenAI Agents SDK as the core; use **function tools** (existing connectors) for speed and **MCP** where official servers exist and OAuth is acceptable.

---

## 5. MCP: What Exists vs Build vs Other

| System | Official MCP? | Recommendation |
|--------|----------------|----------------|
| **ClickUp** | Yes — [official MCP](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server) (public beta, OAuth 2.1). Tasks, comments, time, reports. | **Use official** when OAuth is acceptable; else keep existing **function tools** (connectors) with API key for MVP; document “swap to MCP in Batch 5” as in AGENTIC_PLAN. |
| **Slack** | Yes — [Slack MCP](https://docs.slack.dev/ai/mcp-server) (Feb 2026). Search, messages, canvases, user info. OAuth scopes. | **Use official** for Slack-native agents/dashboards; for “Slack templates + ClickUp sync,” Make/Zapier plus optional MCP is sufficient. |
| **Notion** | Yes — [Notion MCP](https://developers.notion.com/docs/get-started-with-mcp) at `https://mcp.notion.com/mcp`, OAuth 2.0 PKCE. | **Use official** for CD-6 (knowledge bases) and doc read/write from agents. |
| **Frame.io** | No official MCP in public docs. | **Build a small MCP server** (or thin wrapper) that calls the Frame.io API for comments/projects (ED-1 sentiment), or use **Pipedream Frame.io MCP** ([mcp.pipedream.com](https://mcp.pipedream.com/app/frame)) if it exposes comments and fits; otherwise **function tools** only. |

**Summary:**

- **Use existing MCP servers:** ClickUp, Slack, Notion all have official MCPs; integrate them for production and for the “Claude-to-ClickUp MCP” narrative.
- **Frame.io:** Either adopt Pipedream’s MCP if it covers comments, or **build a lightweight MCP** that wraps the Frame.io API (comments, projects) for ED-1 and future ED tools.
- **Mock/context:** Keep the **Dragonfruit Mock Data MCP** ([mcp_servers/README.md](mcp_servers/README.md)) for pipeline, allocations, tool stack, wishlist, and AI survey in demo/dev.

There is no need to recommend other frameworks instead of MCP for these four systems; the brief explicitly names “Claude-to-ClickUp MCP,” and the ecosystem now has official options for three of the four; only Frame.io requires a build or third-party MCP.

---

## References

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [ClickUp MCP](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server)
- [Slack MCP](https://docs.slack.dev/ai/mcp-server)
- [Notion MCP](https://developers.notion.com/docs/get-started-with-mcp)
- Internal: [AGENTIC_PLAN.md](AGENTIC_PLAN.md), [mcp_servers/README.md](mcp_servers/README.md)
