# Deploy this app on Railway

1. **Set Root Directory to `demo-app`**
   - In your Railway project → **Settings** → **Service** (or "Source").
   - Set **Root Directory** to: `demo-app`
   - Save. Redeploy.

2. **Build & start (automatic)**
   - **Build:** `npm ci` then `npm run build` (Nixpacks uses `nixpacks.toml`).
   - **Start:** `npm start` → runs `node server.js`, which serves `dist/` on **0.0.0.0:PORT**. Railway injects **PORT**; the app uses it so the proxy can reach it.

3. **Env vars (optional)**
   - For the backend API (ClickUp, OpenAI), add a separate Railway service for `demo-app/backend` and set `CLICKUP_API_KEY`, `OPENAI_API_KEY` there. The frontend here works without them (mock data).

If you deployed from **repo root** (no root directory set), Railpack fails because the app and `package.json` live in `demo-app/`. Setting Root Directory to `demo-app` fixes it.

---

**If the build still fails with `TS18047: 'rootEl' is possibly 'null'`:**

1. **Confirm Root Directory**  
   Railway → your service → **Settings** → **Root Directory** must be **`demo-app`** (not blank, not the repo root). Save.

2. **Clear build cache and redeploy**  
   In the same service, open **Deployments** (or **Settings**), find **Clear build cache** / **Redeploy** and run it so the next build uses the latest code and no cached `main.tsx`.

3. **Redeploy**  
   Trigger a new deploy (e.g. **Deploy** from the latest commit or push an empty commit). The fix is in `demo-app/src/main.tsx` (null check + `as HTMLElement`); the build must run from `demo-app/` and without stale cache.

---

**If you see "Application failed to respond"** (domain loads but shows this error):

1. **Port must match**  
   Railway’s proxy sends traffic to the **target port** in your service. The app listens on **PORT** (injected by Railway, often **8080**). They must be the same.
   - Go to **Settings → Networking → Public Networking**. Check the **Port** (e.g. "Port 3000").
   - **Option A:** Set **Variables → PORT = 3000** so the app listens on 3000 and matches "Port 3000".
   - **Option B:** Change the **target port** in Networking to **8080** so it matches Railway’s default PORT.
   - Save and **Redeploy**.

2. **Confirm Root Directory** is **`demo-app`** and **Clear build cache** then redeploy so the latest `server.js` and start command are used.
