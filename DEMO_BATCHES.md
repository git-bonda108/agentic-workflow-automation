# Demo Build — Batches (Confirm After Each)

Goal: **All 8 high-priority tools** in one demo. Client feels **in their current environment but faster**, **best value**, **coordination addressed via agentic workflow**. Use Streamlit tabs, MCP callouts, polish. Contract-winning.

---

## Batch 1 — Shell + narrative + Overview + PR-4 tab ✅ (this batch)

**Deliverables:**
- **Hero**: “Your environment. Faster.” + one line on coordination + agentic workflow.
- **Tabs**: 9 tabs — **Overview** | CD-1 | CD-2 | CD-3 | CD-4 | ED-1 | ED-2 | ED-3 | PR-4.
- **Overview tab**: Narrative (your pipeline, pods, wish list; agents + MCP make it faster; coordination solved). Metrics: 4→7, coordination %. **MCP/connector status** (Mock Data, ClickUp, Slack, Frame.io, Notion) — what’s connected, what’s “coming”.
- **PR-4 tab**: Full Producer agent (natural language → ClickUp task), polished; “Connected to ClickUp” callout.
- **Other 7 tabs**: Placeholder per tool — title, short description, “Simulated with your data in next batch” so structure is ready.

**After Batch 1:** You confirm; then we do Batch 2.

---

## Batch 2 — CD-1, CD-2, CD-3, CD-4 tabs (Creative Director) ✅

**Deliverables:**
- **CD-1** (Predictive Retention): Text area for script paste → “Run” → mock retention curve (Plotly), drop-off flags, improvement suggestions. Copy: “In production: [model/API]. Your script, your format.”
- **CD-2** (Outlier Ideation): Select client/pod → “Weekly digest” of outlier videos (mock table: video, theme, format, why it outperformed). Data from pods_and_clients. “Monitors ~20 competitor channels.”
- **CD-3** (Visual Packaging): Input: script snippet or “thumbnail concept” → mock “packaging score” + thumbnail text suggestions.
- **CD-4** (A/B Test Monitor): Mock “Recent alerts” — competitor X changed title/thumbnail, before/after, performance delta. “Slack alert” badge.

**After Batch 2:** You confirm; then Batch 3.

---

## Batch 3 — ED-1, ED-2, ED-3 tabs (Editor / PPM) ✅

**Deliverables:**
- **ED-1** (Frame.io Sentiment): Select client + video → “Run sentiment analysis” → video-level sentiment bar chart + client-level trend line chart; alert threshold slider; Frame.io connected/demo callout.
- **ED-2** (Automated QC): Select client + video → “Run checklist” → timestamped QC report table (timestamp, rule, status, severity); client-specific checklist copy.
- **ED-3** (Capacity Assignment): “Batch ready” task list; “Suggest assignees” → table (editor, workload, skill match, suggested, notes); ClickUp connected/demo callout.

**After Batch 3:** You confirm; then Batch 4.

---

## Batch 4 — Polish + MCP callouts + “Your environment” feel ✅

**Deliverables:**
- **Color palette:** Centralized in `COLOR_PALETTE.md` and CSS variables + `PALETTE` in app (aligned with Dragonfruit / AI Gen X proposal).
- Sidebar: **Connections** line with status badges (Mock Data ✅, ClickUp/Slack/Frame.io/Notion ✅ or 🔶).
- Footer on every page: “Your pipeline · Your pods · Your wish list · Running faster.”
- Copy: Tabs and captions reference “your data” or “your workflow” where relevant.
- DEMO_SCRIPT.md: all 8 tools, MCP map (update as needed).

**After Batch 4:** You confirm. Final pass if needed.

---

## What we need from you (before/during testing)

See **CONNECT_YOUR_DATA.md** for step-by-step:

- **ClickUp**: API key + team ID in `.env` → PR-4 creates real tasks. Get token from ClickUp Settings → Apps; team ID from workspace URL.
- **Frame.io**: Access token in `.env` when we wire ED-1; or use Pipedream Frame.io MCP.
- **Slack**: Bot token in `.env` when we add Slack; get from api.slack.com/apps.
- **Notion**: API key in `.env` when we add Notion; get from notion.so/my-integrations.
- **Mock data**: Edit `mock_data/*.json` to match your pods/clients/pipeline; Mock Data MCP will serve it. No env needed.

---

**Next step:** I implement **Batch 1** and stop for your confirmation.
