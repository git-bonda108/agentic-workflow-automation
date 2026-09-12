# Evaluation

An honest account of how this system is tested today, what the code visibly defends against, and the harness it should have.

## What automated tests exist

**None.** There are no test files in the repository — no pytest/unittest modules, no Vitest/Jest specs, no CI workflow. `tsc -b` inside `npm run build` (demo-app) is the only automated correctness check of any kind (type-checking the React frontend at build time).

What exists instead is **manual test evidence**, recorded as documents:

| File | What it records |
|------|-----------------|
| `MVP_TEST_SUMMARY.md` | A manual end-to-end pass of the Streamlit dashboard: every section exercised, plus the one fix it produced (Python 3.9 type-hint compatibility via `from __future__ import annotations` in the three connector modules). |
| `demo-app/TEST_CLICKUP_REAL.md` | A manual procedure for verifying the live ClickUp integration through the backend (health check, PR-4 create, ED-3 list). |
| `demo-app/MCP_VERIFICATION.md` | A recorded manual verification that an MCP-connected client could read the ClickUp workspace hierarchy and create a task. |

No quantitative metrics (accuracy, latency, cost) exist anywhere in the code or docs; none are cited here.

## Edge cases the code visibly handles

Enumerated from the source, not from intent:

**Missing configuration**
- Every integration degrades rather than fails: ClickUp and Slack connectors return mock data / error dicts when keys are absent (`connectors/clickup_client.py`, `connectors/slack_client.py`); the backend parser falls back to a regex extractor when `OPENAI_API_KEY` is unset (`demo-app/backend/agent_llm.py:_parse_fallback`); the Streamlit PR-4 tab substitutes a mock proposal when the Agents SDK or key is unavailable.
- `ImportError` guards around `dotenv`, the Agents SDK, `mcp`, and the backend's own modules (`main.py` defines no-op stand-ins if `clickup_client`/`agent_llm` fail to import).

**Network and API failure**
- Explicit timeouts on all outbound HTTP: 15 s in `connectors/clickup_client.py`, 10 s in `connectors/slack_client.py`, 10–15 s in `demo-app/backend/clickup_client.py`.
- Two error styles: connectors raise via `raise_for_status()` (Streamlit catches and renders `st.error`), backend helpers catch every exception and return `None`, which endpoint logic converts into a mock response with an explanatory `reasoning` string.
- Non-2xx handling on task creation (`status_code not in (200, 201)` → `None`), and list discovery that walks team → space → folderless lists → folders and returns `None` at any empty level.

**Malformed or hostile input**
- LLM parse output: markdown code-fence stripping before `json.loads`, per-field re-coercion to `str`/`list`, and hard caps (prompt 2 000 chars, task name 255, tags 10×64, assignees 10).
- Empty prompt on `/api/agent/parse` returns a structured `success: False` message instead of a 422 or crash.
- `/api/clickup/synthesized/{name}` checks the name against a fixed allowlist, preventing path traversal into arbitrary files.
- Due-date parsing (`_due_date_to_ms`) accepts ISO dates, weekday names, and "next week", and returns `None` (create without due date) for anything else.

**Frontend resilience**
- `ErrorBoundary.tsx` plus global `onerror`/`unhandledrejection` handlers in `index.html`; every data hook `.catch`es to `null`/empty and the Pipeline page renders distinct loading / error / no-data states.
- Missing mock files: `load_json`/`_load` return `{}` and every consumer guards with `.get(...)` defaults; MCP tools answer "…not found." strings rather than raising.

**Human-in-the-loop as an error barrier**
- The two implemented gates (Streamlit PR-4 Confirm/Cancel; backend parse → confirm-create) put a human between model output and the side effect, which is the system's real defense against wrong-list/wrong-assignee agent mistakes — documented as gates #1–2 in `HUMAN_IN_THE_LOOP_GATES.md`.

## Known gaps

- Nothing verifies that the demo-mode mock shapes match real ClickUp responses (the two ClickUp clients could drift silently).
- The duplicated data (`mock_data/` vs `demo-app/public/mock_data/`) has no consistency check.
- The regex fallback parser and `_due_date_to_ms` have no unit tests despite being pure functions that are trivially testable.
- Backend exception-swallowing means an expired ClickUp token is indistinguishable from intentional demo mode except by reading the `reasoning` field.

## Proposed evaluation harness

*This section is design, not description — none of it exists yet.*

1. **Unit layer (pure functions first).** Pytest over `_parse_fallback`, `_due_date_to_ms`, the fence-stripping/coercion in `parse_task_prompt`, and the demo-mode branches of both ClickUp clients (no network needed). Golden inputs: the sample prompts already used in the UIs.
2. **Contract layer.** Recorded ClickUp v2 responses (httpx `MockTransport` fixtures) asserting that both clients produce the same normalized output for list/create/tasks, and that mock shapes match the recorded shapes field-for-field. This directly closes the drift gap.
3. **Agent behavior layer (golden dataset).** A small JSONL set of natural-language requests → expected tool-call sequence and final structured task (list id, name, due date), run against the Producer agent with the connector in demo mode. Shape: `{"prompt": ..., "expected_tools": [...], "expected_task": {...}}`, ~20–30 cases covering pods, due-date phrasings, missing fields, and the "do not invent IDs" rule. Score tool-sequence exact-match and field-level F1; assert the HITL invariant that no create occurs before confirmation.
4. **Gates.** CI (GitHub Actions) running layers 1–2 on every push (no keys required), layer 3 nightly or on demand behind an `OPENAI_API_KEY` secret with a budget cap. Merge gate: layers 1–2 green; regression gate for layer 3: no drop below the previously recorded pass rate.
5. **Metrics worth recording once live:** parse accuracy vs. human-confirmed fields (the confirm-create step already captures the human-corrected ground truth — log the diff), tool-loop iteration count, end-to-end latency, and HITL rejection rate per gate.
