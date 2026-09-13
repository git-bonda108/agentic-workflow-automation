# How to Connect Your Real Data (ClickUp, Frame.io, Slack, Notion)

Use this **before or while testing** so the demo uses your real workspace data. The app reads **environment variables**; you can also use **MCP servers** and (for mock context) edit the **Mock Data MCP** JSON files.

**For how data and MCPs work** (where data lives, MCP vs API, how your data in ClickUp/Frame.io/Slack flows into the demo): see **[MCP_SERVERS_AND_DATA.md](MCP_SERVERS_AND_DATA.md)**.

---

## 1. Where to put your credentials

**Option A — `.env` file (easiest for local testing)**

1. In the repo root, create a `.env` file:
   ```bash
   touch .env
   ```
2. Edit `.env` and add your keys (see sections below for how to get them).
3. The Streamlit app loads `.env` automatically when it starts, so **restart the app** after changing `.env`.
4. In the app, go to **Run Demo → Overview**. The **Connections (MCP / APIs)** table shows live status: ClickUp, Slack, Frame.io, and Notion show **Connected** or **Configured** when the right variables are set in `.env`.

**Option B — Export in the terminal**

```bash
export OPENAI_API_KEY=sk-...
export CLICKUP_API_KEY=pk_...
export CLICKUP_TEAM_ID=123456
# then run: streamlit run mvp_app.py
```

---

## 2. ClickUp (PR-4 tab + real tasks)

**What it does when connected:** The Producer agent creates and updates **real** tasks in your ClickUp workspace (your spaces, your lists). No more demo-mode mock.

**How to get credentials**

1. Go to [ClickUp Settings → Apps](https://app.clickup.com/settings/apps) (or your profile → Apps).
2. Create or use an **API token** (personal or app). Copy the token (starts with `pk_`).
3. Get your **Team ID**:  
   - In ClickUp, open your workspace URL: `https://app.clickup.com/123456/v/...` — the number is your team ID.  
   - Or use the [ClickUp API](https://clickup.com/api) “Get Authorized Teams” with your token and read the `id` from the response.

**What to put in `.env`**

```env
CLICKUP_API_KEY=pk_your_token_here
CLICKUP_TEAM_ID=your_team_id_number
```

**Testing:** Restart the app, open the **PR-4 ClickUp** tab, run a command like “Create a task for [Your Space]…”. The task should appear in ClickUp.

**MCP option:** You can instead use the [official ClickUp MCP](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server) (OAuth). That’s configured in your MCP client, not in `.env`. The app’s **connectors** use the env vars above; MCP is for other clients.

---

## 3. Frame.io (ED-1 tab — sentiment later)

**What it does when connected:** ED-1 (Frame.io Comment Sentiment) can read real projects/assets/comments and show sentiment. The demo tab will use live data when we wire it (Batch 3+).

**How to get credentials**

1. Go to [Frame.io Developer](https://developer.frame.io/) and create an app (or use an existing one).
2. Get an **access token** (OAuth or personal token depending on the app type).  
   Or use [Pipedream Frame.io MCP](https://mcp.pipedream.com/app/frame) and connect your Frame.io account there.

**What to put in `.env`** (when we add the connector)

```env
FRAMEIO_ACCESS_TOKEN=your_token_here
# Optional: FRAMEIO_PROJECT_ID=... if you want to default to one project
```

**For now:** Leave this for when ED-1 is wired. You can still add the token so it’s ready.

**MCP option:** Use [Pipedream’s Frame.io MCP](https://mcp.pipedream.com/app/frame); connect Frame.io in Pipedream. The app can then talk to Frame.io via that MCP if we add an MCP client in the app.

---

## 4. Slack (templates, routing, ED-1/PR alerts later)

**What it does when connected:** Enables Slack message sending (templates, routing), and later alerts (e.g. ED-1 sentiment, CD-4 A/B alerts) to Slack.

**How to get credentials**

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → Create New App → From scratch (or use existing).
2. If you see **“Generate Your App Configuration Token”**: choose the **workspace** where the demo should run, then Generate. That token is for app configuration only. For the demo we need the **Bot User OAuth Token** (next step).
3. In the app sidebar go to **OAuth & Permissions**. Add **Bot Token Scopes** (e.g. `chat:write`, `channels:read`, `users:read`).
4. **Install to Workspace** (same workspace you use for the demo). After install, copy the **Bot User OAuth Token** (starts with `xoxb-`) — that is what you put in `.env`.

**What to put in `.env`**

```env
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
```

**MCP option:** Use the [official Slack MCP](https://docs.slack.dev/ai/mcp-server/). Configure it in your MCP host. The app’s own Slack connector uses `SLACK_BOT_TOKEN` above.

---

## 5. Notion (CD-6, context, docs)

**What it does when connected:** Can read/write Notion pages and databases (e.g. client knowledge bases, packaging docs).

**How to get credentials**

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations) and create an integration.
2. Copy the **Internal Integration Token** (secret).
3. Share the pages/databases you need with that integration (page → Share → invite the integration).

**What to put in `.env`** (when we add the connector)

```env
NOTION_API_KEY=your_integration_secret
# Optional: NOTION_DATABASE_ID=... for a default database
```

**MCP option:** Use [official Notion MCP](https://developers.notion.com/docs/mcp) (`https://mcp.notion.com/mcp`) with OAuth. For the app, we’d use the API key above in a Notion client.

---

## 6. Mock Data MCP — add or edit data for testing

The **Mock Data MCP server** (`mcp_servers/agency_mock_server.py`) serves data from the `mock_data/*.json` files. So:

- **To change what the “mock” context is** (e.g. pipeline, pods, time allocations, wish list):  
  Edit the JSON files in **`mock_data/`** and restart the Mock Data MCP server. Any MCP client (or the app, if we wire it to that MCP) will then see the updated data.

- **Files you can edit:**
  - `mock_data/pipeline_stages.json` — pipeline phases and steps
  - `mock_data/time_allocations.json` — current vs dream by role
  - `mock_data/pods_and_clients.json` — pods, clients, capacity (4→7)
  - `mock_data/tool_stack.json` — tools and spend
  - `mock_data/wishlist_tools.json` — high/medium priority tools
  - `mock_data/ai_survey_summary.json` — survey by role

- **No JSON change needed for ClickUp/Frame.io/Slack:** Once you add real credentials (above), the app uses **live** data from those systems. The JSON mock data is only for pipeline/pods/wish list **context** and for when those services aren’t connected.

**Run Mock Data MCP (optional)**

```bash
# Python 3.10+ required
pip install "mcp[cli]"
python mcp_servers/agency_mock_server.py
```

Then point your MCP host at this server (stdio or HTTP) to query pipeline, allocations, pods, etc.

---

## 7. Summary — what to provide before Batch 3

| System      | Where to get it              | Where to put it     | When you can test      |
|------------|------------------------------|---------------------|-------------------------|
| **OpenAI** | platform.openai.com → API keys | `OPENAI_API_KEY` in `.env` | PR-4 real agent now    |
| **ClickUp**| ClickUp Settings → Apps → API token; URL for team ID | `CLICKUP_API_KEY`, `CLICKUP_TEAM_ID` in `.env` | PR-4 real tasks now     |
| **Frame.io** | developer.frame.io or Pipedream | `FRAMEIO_ACCESS_TOKEN` in `.env` (when we add it) | After ED-1 is wired      |
| **Slack**  | api.slack.com/apps → Bot token | `SLACK_BOT_TOKEN` in `.env` | When we add Slack tools |
| **Notion** | notion.so/my-integrations   | `NOTION_API_KEY` in `.env` (when we add it) | When we add Notion      |
| **Mock data** | Edit `mock_data/*.json`     | No env needed       | Anytime; restart MCP if you use it |

**Recommended before Batch 3:**  
Add at least **OPENAI_API_KEY** and **ClickUp** (API key + team ID) to `.env`, restart the app, and test the **PR-4** tab with a real task. Optionally edit `mock_data/pods_and_clients.json` (and others) so labels match your real pods/clients. Then we proceed with Batch 3 (ED-1, ED-2, ED-3) and can wire Frame.io when you’re ready.
