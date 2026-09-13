# AIGenX — Agentic Pipeline Demo

**Gateway to the overall project.** This demo app shows the pipeline-first hierarchy: **Pipeline → Phase → Role → Opportunity**, with MCP integration, GIFs (agent trajectory), and dream allocation mapping.

## Run

**Easiest:** In Finder, go to the repo's `demo-app` folder and **double‑click `START.command`**. A terminal will open, the server will start, and your browser should open to the app. Keep the terminal window open.

**Or from Terminal:**

```bash
cd demo-app
npm install   # first time only
npm run dev
```

**Important:** Use the URL that opens in your browser (e.g. **http://localhost:3000**). Do not type only “localhost” — you must include the port, e.g. `http://localhost:3000`.

## Data

- **Public data:** `public/mock_data/` — all JSON is loaded from here (phase_roles, wishlist_tools, tool_io, tool_integration, tool_dream_mapping, time_allocations, ai_survey_summary, role_opportunities).
- **GIFs:** `public/gifs/` — HTML animations for agent trajectory; each opportunity links to a `gif_id` (e.g. `pr4_tool_use_react.html`).
- **Data manifest:** See `../mock_data/DATA_MANIFEST.md` for dependency order and file ↔ UI mapping.

## Batches

- **Batch 1–2 (done):** Data model (phase_roles, tool_io, tool_integration, tool_dream_mapping, role_opportunities) + scaffold, theme, pipeline view, GIFs in public.
- **Batch 3:** Phase detail → Roles → Opportunities (role cards with “Currently using”, dream one-liner, opportunity list).
- **Batch 4:** Opportunity detail (run demo, GIF iframe, input/output, integration, dream allocation).
- **Batch 5:** Trajectory page + polish.

## Deploy to Railway

**Railway** is a good fit for this app:

- **Frontend:** Build the Vite app (`npm run build`), then serve the `demo-app/dist` folder (e.g. with `npx serve -s dist` or Railway’s static site support).
- **Backend (optional):** Add a second Railway service for the Python FastAPI backend in `demo-app/backend` (use `pip install -r requirements.txt` and run `uvicorn main:app`). Set env vars (e.g. `CLICKUP_API_KEY`, `OPENAI_API_KEY`) in the Railway dashboard.
- Connects to your GitHub repo for auto-deploy on push; free tier is usually enough for a demo.

See [Railway Docs](https://docs.railway.app/) for project setup and environment variables.

## Stack

- Vite + React 18 + TypeScript
- React Router 6
- CSS variables (AIGenX palette), Space Grotesk + Inter
