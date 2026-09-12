# MCP Servers and Data — How Real Data Gets Into the Demo

This document clarifies: **where data lives**, **how you add it**, and **how the demo sees it** when we integrate MCP servers or APIs.

---

## 1. Where does the data live?

**Data lives in the products you already use.** You do **not** type data into the demo app to “fill” it.

| System     | Where you add data | What the demo will show when connected |
|-----------|--------------------|----------------------------------------|
| **ClickUp** | You log in to ClickUp and create spaces, lists, tasks, assignees. | Real spaces, lists, tasks. PR-4 creates real tasks there; the app can list and show them. |
| **Frame.io** | You log in to Frame.io; projects, assets, and review comments live there. | Real projects, assets, comments. ED-1 sentiment will read real comments when we connect. |
| **Slack** | Channels and messages are in your Slack workspace. | Real channels, messages. When we add Slack, templates and alerts send real messages (with human approval). |
| **Notion** | Pages and databases are in your Notion workspace. | Real pages, docs. When we connect, the app can read/write (e.g. CD-6, packaging docs). |

So: **you log in to ClickUp, Frame.io, Slack, Notion and add or use data there. When we integrate those systems into the demo, the app reads from (and, where appropriate, writes to) that same data.** No separate “demo database” — the source of truth is your workspace.

---

## 2. MCP vs API — which one, and can you “log in” to MCPs?

**MCP (Model Context Protocol)** = a standard way for AI apps (and our demo) to talk to a service. The service is exposed as an “MCP server” that offers tools (e.g. “create_task”, “list_comments”).

**API** = our app calls the product’s HTTP API directly (e.g. ClickUp API, Frame.io API).

- **For you:** You don’t “log in to an MCP server.” You log in to **ClickUp / Frame.io / Slack / Notion** (as you do today). You create tasks, comments, channels, pages there. Then you give the **demo** a way to access that product — either by connecting an **MCP server** that talks to that product, or by giving the app **API credentials** (keys, tokens) so it talks to the product’s API.
- **Data flow:**  
  - **With MCP:** The MCP server is already connected to ClickUp (or Frame.io, etc.). The demo app talks to the MCP server; the MCP server talks to the product. So the demo sees **real data** from that product.  
  - **With API:** The demo app uses credentials you provide (e.g. in `.env`) and calls ClickUp’s (or Frame.io’s, etc.) API. Again, the demo sees **real data** from that product.

So: **yes, you can add data in the real products and have it show up in the demo** — we just need either (a) the demo to use an MCP server that’s connected to that product, or (b) the demo to use the product’s API with credentials you provide.

---

## 3. How you add data so the demo can use it

| Step | What you do | Result when we integrate |
|------|-------------|---------------------------|
| 1 | Log in to **ClickUp**. Create spaces/lists that match your pods (e.g. Mango Pod, Lemon Pod). Add real tasks, assignees, due dates. | When we connect ClickUp (MCP or API), PR-4 and the demo will list and create tasks in those spaces. Real data flows through. |
| 2 | Log in to **Frame.io**. Have real projects, assets, and review comments. | When we connect Frame.io (MCP or API), ED-1 can read real comments and show sentiment. Real data flows through. |
| 3 | Use **Slack** as usual — channels, client channels, messages. | When we add Slack (MCP or API), the demo can send templated messages or alerts to real channels (with human-in-the-loop). |
| 4 | Use **Notion** as usual — client portals, SOPs, packaging docs. | When we connect Notion (MCP or API), the demo can read/write real pages. |

You do **not** need to paste data into the demo. You add data in the products; we integrate those products; the demo shows that data.

---

## 4. MCP vs API — when we use which

| Approach | Pros | Cons | When we use it |
|----------|------|------|----------------|
| **Official/third‑party MCP server** (e.g. ClickUp MCP, Notion MCP, Slack MCP) | Same tools available to any MCP client (desktop MCP clients, our app). You may already have the product connected via MCP. | We need to wire the demo to that MCP (e.g. stdio or HTTP). OAuth may be required. | When you want one connection (e.g. ClickUp) shared across multiple AI tools; or when the vendor provides an MCP. |
| **Direct API** (our connectors with `CLICKUP_API_KEY`, etc.) | We control exactly which endpoints we call. Simple for the demo: env vars, no MCP server to run. | Credentials and logic are in our app only. | When we need a simple, reliable integration for the demo and you’re fine providing API keys/tokens. |

**For the demo we can use either.** If you prefer to connect via MCP (e.g. you already use ClickUp’s MCP in a desktop client), we integrate that MCP so the demo uses it and you see real ClickUp data. If you prefer to give us API keys, we use our existing connectors and you still see real data. In both cases, **data you add in the product appears in the demo** once that product is connected.

---

## 5. Summary

- **You add data** by logging in to **ClickUp, Frame.io, Slack, Notion** and creating/editing data there.
- **The demo sees that data** when we integrate each product via **MCP server** or **direct API**.
- **MCP vs API:** Both can deliver real data; we choose per product (MCP if you want a shared connection, API if we want simplicity and you provide keys).
- **No need to “log in to MCP servers”** — you log in to the products; we connect the demo to those products so real data flows through.
