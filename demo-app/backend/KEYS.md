# Keys the demo looks for (real MCP / API)

The backend **reads ClickUp** when `CLICKUP_API_KEY` (or `CLICKUP_PERSONAL_TOKEN`) is set in the environment. All other tools still use mock data until you add keys.

**ClickUp MCP:** the ClickUp MCP was verified from an MCP-enabled client with `clickup_get_workspace_hierarchy` and `clickup_create_task`. See **MCP_VERIFICATION.md**. The demo app backend uses the **REST API** with the same token for PR-4/ED-3 when the key is set.

---

## ClickUp (wired for PR-4 and ED-3)

| Key | Where to set | Used for |
|-----|----------------|----------|
| **`CLICKUP_API_KEY`** or **`CLICKUP_PERSONAL_TOKEN`** | `.env` at **project root** (repo-root `.env`) or in `demo-app/backend/.env` | PR-4 (create task), ED-3 (list tasks / assignees). Backend loads this via `python-dotenv` and calls [ClickUp API v2](https://developer.clickup.com/) (create task, get lists, get tasks). |
| **`CLICKUP_TEAM_ID`** | Optional. If not set, the backend discovers the first team (workspace) and first list from the API. | When set, can be used to target a specific workspace. |

Personal tokens start with `pk_` and can be created in ClickUp: **Settings → Apps → API Token**. The backend uses the same token for REST API calls (official ClickUp MCP at https://mcp.clickup.com/mcp uses OAuth; for server-side we use the REST API with your token).

---

## OpenAI (used for “Create task with agent” — Plan, Reason, Act)

| Key | Where to set | Used for |
|-----|----------------|----------|
| **`OPENAI_API_KEY`** | `.env` at **project root** (repo-root `.env`) or `demo-app/backend/.env` | The **text box on the Pipeline page** sends your text to this backend; the backend calls the OpenAI API to parse the prompt (task name, due date, assignee, tags, dependencies). If the key is missing, a rule-based fallback is used and tasks are still created in ClickUp when `CLICKUP_API_KEY` is set. |

---

## For future real MCP / API connections

| Key | Where to set | Used for |
|-----|----------------|----------|
| **Slack token / bot token** | Depends on the Slack MCP server you use | CD-2, CD-3, CD-4 (alerts, commands). Set per your Slack MCP docs. |
| **Notion API token** | Depends on the Notion MCP server | CD-1, CD-6, CD-7 (scripts, knowledge bases). Set per your Notion MCP docs. |
| **Frame.io API token** | Environment or backend config | ED-1 (comment sentiment). Frame.io has no public MCP; use REST API. |
| **YouTube Data API key** | Environment or backend config | CD-1–CD-4 (retention, competitors, A/B). Google Cloud Console. |

---

## Summary

- **ClickUp:** Set **`CLICKUP_API_KEY`** (or **`CLICKUP_PERSONAL_TOKEN`**) in **the repo-root `.env`**. Backend loads it and uses real ClickUp API for PR-4 and ED-3. If the key is missing or invalid, the backend falls back to mock data from `MCP SYNTHESIZED DATA`.
- **All other tools:** Still mock. Add tokens when you wire Slack, Notion, Frame.io, or YouTube in `backend/main.py`.
- Keep `.env` out of version control (add to `.gitignore`).
