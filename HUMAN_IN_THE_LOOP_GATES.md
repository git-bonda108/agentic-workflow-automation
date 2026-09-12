# Human-in-the-Loop — Critical Gates

From your **architecture brief** (“Risk mitigation plan: human-in-the-loop, rollback strategies”), **proposal** (“All task creation, assignment, and client-facing messages require review or one-click confirm”), and **pipeline** (ECD, CD, PPM, Client approvals at multiple stages), these are the **critical gates** where a human must review or approve before the system proceeds.

---

## 1. Critical gates (where HITL is required)

| # | Gate | System / tool | Who approves | What happens without HITL |
|---|------|----------------|--------------|---------------------------|
| **1** | **ClickUp task creation** | PR-4 (Claude-to-ClickUp) | Producer or PC | Agent could create wrong list, wrong assignee, or duplicate tasks. |
| **2** | **ClickUp task assignment** | ED-3 (Capacity assignment) | PC or Producer | Auto-assign could overload an editor or assign wrong skill (e.g. longform to shortform specialist). |
| **3** | **Client-facing Slack message** | PR-3 (Slack templates), any bot sending to client channels | Producer or PC | Wrong tone, wrong client, or sensitive info could be sent. |
| **4** | **QC report → action** | ED-2 (Automated QC) | PPM | Automated report is fine; **escalation** to editor or client must be decided by PPM (which items to flag, how to phrase feedback). |
| **5** | **Sentiment alert → response** | ED-1 (Frame.io sentiment) | PPM or Producer | Alert is informational; **response** to client or internal must be human-decided (no auto-send). |
| **6** | **Publish / final client handoff** | Pipeline (publish prep) | Producer or designated role | Client provides final approval; system must not publish or mark “final” without human confirmation. |
| **7** | **Competitor alert → action** | CD-4 (A/B Test Monitor) | Creative Director | Alert is informational; CD decides whether to act (test similar packaging, etc.). |

---

## 2. Pipeline approval points (already human gates)

Your **current pipeline** already has these approval points; automation must **not** bypass them:

| Phase | Approval point | Responsible |
|-------|----------------|-------------|
| Onboarding | ECD approves Channel Audit; ECD and CD approve Content Strategy; ECD approves Style Edit; Client approves Style Edit | ECD, CD, Client |
| Pre-Production | Client approves ideation; CD approves script; Client approves script | CD, Client |
| Post-Production | PPM V1/V2/V3 reviews; CD V2/V3 reviews; Client review; CD or PPM V4 approve; **Client provides final approval** before publish | PPM, CD, Client |

**HITL in the demo:** Any automation that touches these steps (e.g. “mark task as client-approved”) must require an explicit human action, not an auto-check.

---

## 3. How we implement HITL in the demo

| Gate | Implementation in demo |
|------|-------------------------|
| **PR-4 (task creation)** | Before the agent creates a task: show **proposed task** (list, name, due date, assignee); user must click **Confirm** or **Edit**; only on Confirm do we call ClickUp (or mock). |
| **ED-3 (assignment)** | After system suggests assignees: show **suggested assignees** per task; user must **Confirm** or **Override**; only on Confirm do we write to ClickUp. |
| **Slack (client message)** | Before sending: show **draft message** and target channel; user must **Approve** or **Edit**; only on Approve do we send (when Slack is connected). |
| **ED-2 (QC escalation)** | After QC report: show **report**; PPM chooses **Escalate to editor**, **Escalate to client**, or **Dismiss** per item (or in bulk). No auto-escalation. |
| **ED-1 (sentiment)** | When sentiment drops: show **alert** and summary; user chooses **Acknowledge**, **Notify Producer**, or **Add to client call**. No auto-message to client. |
| **Publish / final handoff** | Demo shows a **Final approval** step: “Ready for client?” or “Ready to publish?” — user must click **Confirm** before any automated state change. |
| **CD-4 (competitor alert)** | Alert is read-only; CD sees it and acts in Slack/ClickUp/Notion as they do today. No HITL UI needed in demo beyond “alert delivered.” |

---

## 4. Rollback (from architecture brief)

- **Feature flags / toggles:** Per pod or per client, we can turn off PR-4 (task creation), ED-3 (assignment), or Slack sending so the team falls back to manual process.
- **Rollback in demo:** We can show a **“Pause automation”** or **“Revert to manual”** control for the relevant tool so the client sees that we take rollback seriously.

---

## 5. Summary table — critical gates for the demo

| Gate | Tool | Human action before system proceeds |
|------|------|-------------------------------------|
| Task creation | PR-4 | Confirm or edit proposed task |
| Task assignment | ED-3 | Confirm or override suggested assignees |
| Client Slack | PR-3 / alerts | Approve or edit draft message |
| QC escalation | ED-2 | PPM decides escalate / dismiss |
| Sentiment response | ED-1 | Human decides response; no auto-send |
| Publish / final handoff | Pipeline | Confirm “ready for client” / “publish” |
| Competitor alert | CD-4 | Informational; CD decides action |

These are the gates we will implement in the demo so the client sees human-in-the-loop at every critical action.
