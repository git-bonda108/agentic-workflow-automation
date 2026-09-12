# Dragonfruit Demo — Script & Priority Focus

## What this demo is

**One priority win, end to end.** We show the **single high-priority automation** we demo live today (**PR-4 Claude-to-ClickUp**), and we **explicitly list all 8 client high-priority tools** so the client sees which one we address now and which (including **CD-2**) are on the roadmap.

---

## Client high-priority list (all 8 — from wish list brief)

From the client’s **AI Tool Wish List**: *“High Priority (8 tools). These tools address the most time-intensive manual processes or the highest-impact strategic needs. They should be scoped and prototyped first.”*

| ID | Name | Role | What our demo does |
|----|------|------|--------------------|
| **CD-1** | Predictive Retention Scoring | Creative Director | **Referenced** — roadmap / next. |
| **CD-2** | Competitive Outlier Ideation Engine | Creative Director | **Referenced** — roadmap / next (client called out CD-2). |
| **CD-3** | Visual Packaging & Thumbnail Intelligence | Creative Director | **Referenced** — roadmap / next. |
| **CD-4** | Competitor A/B Test Monitor | Creative Director | **Referenced** — roadmap / next. |
| **ED-1** | Frame.io Comment Sentiment Analyzer | Editor / PPM | **Referenced** — roadmap / next. |
| **ED-2** | Automated Video QC Checker | Editor / PPM | **Referenced** — roadmap / next. |
| **ED-3** | Automated Capacity-Based Task Assignment | Producer / PC | **Referenced** — roadmap / next. |
| **PR-4** | Claude-to-ClickUp Agent | Producer | **Demo addresses** — we show it live (natural language → ClickUp task). |

---

## Which ones our demo is going to address

- **Addressed in the demo (built and shown):** **PR-4** only. We demonstrate the Producer agent creating a ClickUp task from natural language; this targets the 21–25% of Producer/PC time on ClickUp admin.
- **Referenced as high-priority next (not built yet):** **CD-1, CD-2, CD-3, CD-4, ED-1, ED-2, ED-3.** We list them in the app under “What’s next” so the client sees we’re aligned on all 8 and that CD-2 (and the rest) are in scope for the roadmap.

**One-liner for the presenter:**  
*“Your brief has 8 high-priority tools, including CD-2 Outlier Ideation. This demo addresses one of them live: PR-4, the Claude-to-ClickUp agent, which cuts the 21–25% of Producer and PC time on ClickUp admin. We’ll show your data, the problem, and the agent creating a task from one sentence. The other seven—including CD-2—are on the roadmap and we can scope them next.”*

---

## Demo flow (in the app)

1. **Priority win** — Callout: PR-4; table with what it does and why it matters.
2. **The problem** — Metrics: Producers ~38% and PCs ~40% on ClickUp today; dream ~18–20%.
3. **Your data** — Pipeline phases + pods (Mango, Lemon), 4 → 7 clients per pod. Emphasize: not generic; your pipeline, time audit, and wish list.
4. **The win** — Producer agent: pre-filled command → Run → reply + tool calls (real or mock).
5. **What’s next** — Overall goal (4→7 clients); other high-priority tools; 30-day quick wins.

---

## How to run the demo

1. Open the app: `streamlit run mvp_app.py`.
2. In the sidebar, select **“Run Demo”** (first option).
3. Scroll through sections 1–4; at section 3 click **“Run Producer agent”** (with or without `OPENAI_API_KEY` for real vs mock).
4. Optionally open **Time Allocations**, **Pipeline**, or **Producer Agent** for deeper dives.

---

## Overall vs priority

- **Overall** = full proposal: 4→7 clients, three levers, 16 tools, roadmap, costs. (Use **Proposal Summary** and **Wish List & Tools** for that.)
- **This demo** = **one priority win (PR-4)** brought together with your data and a live (or mock) agent run. Specific, repeatable, and easy to explain in 5 minutes.
