# ClickUp MCP — Verification

The ClickUp MCP integration was tested from an MCP-enabled client against a live workspace. The following was verified.

## Tests run

1. **`clickup_get_workspace_hierarchy`**  
   - **Arguments:** `max_depth: 2`, `limit: 10`  
   - **Result:** Success. Returned the workspace tree with spaces and lists.  
   - **Conclusion:** MCP is authenticated and can read the ClickUp workspace.

2. **`clickup_create_task`**  
   - **Arguments:** `name: "Dragonfruit demo verification"`, a `list_id` resolved from the hierarchy, and a test description.  
   - **Result:** Success. Returned a `task_id` and `task_url` for the created task.  
   - **Conclusion:** Create-task flow works end-to-end via MCP.

## Using ClickUp MCP from a client

- **Workspace hierarchy:** Use `clickup_get_workspace_hierarchy` to see spaces and lists and resolve list IDs.
- **Create task:** Use `clickup_create_task` with `name` and `list_id` (and optional `description`, `assignees`, `due_date`, etc.).
- **Other tools:** The ClickUp MCP exposes more tools (e.g. `clickup_get_task`, `clickup_update_task`, `clickup_get_task_comments`). Use your client's MCP tool list to discover and call them.

## Demo app vs client MCP

- **In an MCP client:** You use the ClickUp MCP directly (as above). No extra setup.
- **In the demo app (browser):** The backend uses the **ClickUp REST API** with `CLICKUP_API_KEY` from `.env` for PR-4 and ED-3. The same workspace is used; the app cannot call a desktop MCP process. For a single “real ClickUp” path, the backend is wired to the REST API and is ready when the key is set.

## MCP synthesized data

Mock and demo data for the app are loaded from **`MCP SYNTHESIZED DATA`**:

- `clickup_workspace.json` — workspace structure (pods and lists).  
  Served by backend at **`GET /api/clickup/workspace`** when using mock data.
- `clickup_create_task_response.json` — PR-4 create-task response.  
  Used by backend for PR-4 when no API key or when API is unavailable.
- `clickup_assign_editor_response.json` — ED-3 assignee suggestion response.  
  Used by backend for ED-3 mock.
- `clickup_editor_capacity.json`, `clickup_tasks_mango_batch14.json`, `clickup_timeline_calculator_response.json` — available for richer mock or future endpoints.  
  Served by backend at **`GET /api/clickup/synthesized/{name}`** (e.g. `clickup_editor_capacity`).

All of the above keep mock data aligned with the MCP synthesized folder and make one real ClickUp path (REST API in the app + MCP in a client) ready.
