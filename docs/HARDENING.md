# Hardening

Current security and operability posture, followed by a staged ladder to production. Grounded in what the code is: a demo-grade MVP with one live write-path (ClickUp task creation) behind human confirmation.

## Current posture

**Secrets handling — good for a demo.**
- No credentials are committed at HEAD (verified by sweep; only `pk_your_token_here`-style placeholders exist in docs). `.gitignore` excludes `.env`, `.env.*`, `*.pem`.
- All keys are read from environment variables via `python-dotenv` (`mvp_app.py` loads root `.env`; the backend also checks `demo-app/backend/.env`). Keys never appear in responses; the ClickUp key is sent only as an `Authorization` header to `api.clickup.com`.

**Authentication and authorization — absent.**
- The FastAPI backend has no auth of any kind. Anyone who can reach it can create real ClickUp tasks (`/api/agent/confirm-create`, `/api/demo/PR-4`) once a key is configured server-side. CORS is restricted to `localhost:3000`/`127.0.0.1:3000`, which protects browsers but not direct HTTP clients.
- The Streamlit app and MCP server are likewise unauthenticated; both are intended for local/stdio use.
- The HITL confirm step is a UX gate, not a security control — the confirm endpoint trusts whatever fields it is sent.

**Error handling — availability-biased.**
- Connectors raise and the UIs render the error; backend helpers swallow all exceptions and fall back to mock output with a `reasoning` note. The demo never hard-fails, but real failures (expired token, permission loss) are silent to operators.
- Input hygiene exists at the edges: length caps on names/tags/prompts, an allowlist on the synthesized-data endpoint, structured rejection of empty prompts, JSON-fence stripping of LLM output.
- Two code-level notes: `datetime.utcnow()` (deprecated, naive UTC) is used for due-date math, and Streamlit renders some strings with `unsafe_allow_html=True` (currently static or repo-controlled JSON, but it is an injection surface if mock data ever becomes user-supplied).

**Observability — none.**
- No logging framework, no request logs beyond uvicorn defaults, no tracing configuration for the Agents SDK, no metrics, no error reporting. The `source` field and `steps` list in API responses are the only built-in provenance.

**Deployment.**
- Frontend: static build served by `server.js` on Railway (binds `0.0.0.0:$PORT`). Backend: designed as a separate Railway service holding the keys. No TLS termination, rate limiting, or health-alerting configured in-repo beyond `/health`.

## Ladder to production

**Stage 1 — Identity and keys (before any shared deployment)**
1. Put the backend behind authentication: at minimum a static bearer token checked by FastAPI dependency; properly, the agency's Google Workspace SSO (OIDC) so HITL confirmations are attributable to a person.
2. Bind the HITL gate server-side: `parse` returns a signed, short-lived proposal token; `confirm-create` accepts only that token, so the confirm step can't be replayed or forged with altered fields.
3. Move keys to the platform secret store (Railway variables already fit); create a dedicated ClickUp service account with least-privilege scope on the target space rather than a personal token; document rotation.
4. Widen CORS deliberately (deployed frontend origin only), never `*`.

**Stage 2 — Monitoring and failure visibility**
1. Replace silent `except Exception: return None` with logged failures (structlog/std logging + Sentry or equivalent), keeping the mock fallback but making the degradation observable and alertable.
2. Enable Agents SDK tracing for tool-call sequences; persist the `steps` audit trail of every confirm-create with actor and timestamp.
3. Add uptime and budget guards: request logging, per-key OpenAI spend alerting, `/health` monitored externally.

**Stage 3 — Deployment hygiene**
1. Pin dependencies (both `requirements.txt` files use `>=`; produce a lock with pip-tools/uv, and rely on the existing `package-lock.json` via `npm ci`).
2. Add the CI gates from EVALUATION.md (type-check, unit, contract tests) as the merge barrier; build the frontend's mock-data copy from `mock_data/` instead of committing a duplicate.
3. Untrack build artifacts (`tsconfig.tsbuildinfo`, stale Vite timestamp configs) and add them to `.gitignore`.
4. Rate-limit the write endpoints and cap request body sizes at the proxy.

**Stage 4 — Compliance and client-data protection**
1. Real workspace data (task names, assignees, Frame.io comments, Slack messages) is client confidential: define retention for any persisted audit trail, and redact personal names/emails from logs.
2. Data-processing review before enabling the LLM parse path on real task text (what leaves the workspace, to which model provider, under what DPA).
3. Per-gate authorization matrix from `HUMAN_IN_THE_LOOP_GATES.md`: which roles may confirm which gate (task create vs. assignment vs. client-facing message), enforced in the backend, not the UI.
4. Quarterly key rotation and an offboarding checklist (service-account ownership, not personal tokens).
