# the media agency MCP Servers

MCP servers used by the agentic MVP. Mock data is exposed so agents can query pipeline, time allocations, pods, and tooling **without** calling live APIs.

## 1. the media agency Mock Data Server

Exposes `mock_data/*.json` as **tools** and **resources** so any MCP client (the OpenAI Agents SDK, a desktop MCP client, etc.) can read:

- Pipeline stages and steps
- Current vs dream time allocations by role
- Pods and clients
- Tool stack and spend
- AI wish list (high/medium priority)
- AI survey summary by role

**Requires:** Python 3.10+ (MCP SDK requirement). Install: `pip install "mcp[cli]"`.

**Run (stdio):**
```bash
cd dragonfruit-workflow-agent
python mcp_servers/dragonfruit_mock_server.py
# or: uv run --with mcp python mcp_servers/dragonfruit_mock_server.py
```

**Use from OpenAI Agents SDK:** Add as `MCPServerStdio` with the command above, or run as HTTP and use `MCPServerStreamableHttp`.

**Use from a desktop MCP client:** Configure the server in your MCP settings (stdio or HTTP URL).

## 2. External MCP servers (optional)

- **ClickUp:** [Official MCP](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server) or community (e.g. Composio, maciejr81/clickup-mcp).
- **Notion:** [Official Notion MCP](https://developers.notion.com/docs/mcp) (`https://mcp.notion.com/mcp`).
- **Slack:** [Official Slack MCP](https://docs.slack.dev/ai/mcp-server/).
- **Frame.io:** [Pipedream Frame.io MCP](https://mcp.pipedream.com/app/frame) or custom connector.

Our **connectors/** (ClickUp, Slack, etc.) can stay as function tools, or you can switch to these MCP servers and keep the **mock data MCP** for context (pipeline, allocations, pods).
