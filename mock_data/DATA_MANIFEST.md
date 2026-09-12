# Mock Data Manifest — Dragonfruit Demo App

Single source of truth for the **pipeline-first** hierarchy and how the UI consumes each file.

---

## Dependency order (load / use)

1. **phase_roles.json** — Pipeline phases and which core roles operate in each phase. Drives **Pipeline view** (phase tiles) and **Phase detail** (which roles to show).
2. **role_opportunities.json** — For each of the 5 core roles, list of tool IDs (e.g. Producer → PR-1, PR-2, PR-3, PR-4) and priority per tool. Used when rendering **Role card** opportunity list.
3. **wishlist_tools.json** — Tool id, name, role, category, description; high_priority vs medium_priority. Used for **Opportunity cards** and **Opportunity detail** header.
4. **tool_io.json** — Per tool id: `input` and `output` bullet arrays. Used in **Opportunity detail** for Input/Output section.
5. **tool_integration.json** — Per tool id: `integration_type`, `tools_or_services`, `description`, `gif_id`. Used in **Opportunity detail** for Integration block and **GIF iframe** (`/gifs/${gif_id}.html`).
6. **tool_dream_mapping.json** — Per tool id: `role`, `role_key`, `dream_impact_short`, `current_vs_dream`, `categories_affected`. Used in **Opportunity detail** for Dream allocation impact. `role_key` links to **time_allocations.json** (e.g. "Producers").
7. **time_allocations.json** — Per role (Producers, Production Coordinators, …): `current`, `dream`, `key_notes`. Used for **Role card** dream one-liner and **Opportunity detail** dream block.
8. **ai_survey_summary.json** — Per role: `top_tools`, `use_cases`, `top_requests`. Used for **Role card** and **Opportunity detail** “Currently using”.
9. **pipeline_stages.json** — Optional: full steps per phase for step-level display or tooltips.

---

## File ↔ UI mapping

| File | Where used |
|------|------------|
| phase_roles.json | Pipeline (phase list), Phase detail (roles in phase) |
| role_opportunities.json | Phase detail → Role card (list of opportunity tool IDs + priority) |
| wishlist_tools.json | Opportunity card (name, priority), Opportunity detail (name, role, description) |
| tool_io.json | Opportunity detail (Input, Output) |
| tool_integration.json | Opportunity detail (Integration, GIF iframe) |
| tool_dream_mapping.json | Opportunity detail (Dream allocation impact) |
| time_allocations.json | Role card (key_notes), Opportunity detail (key_notes + current/dream %) |
| ai_survey_summary.json | Role card (“Currently using”), Opportunity detail (“This role today”) |

---

## GIFs (public/gifs)

| gif_id | File | Typical tools |
|--------|------|----------------|
| cd_agent_flow_animated | cd_agent_flow_animated.html | CD-1 … CD-9 |
| ppm_ed_flow_animated | ppm_ed_flow_animated.html | ED-1, ED-2 |
| ed3_capacity_react_hitl | ed3_capacity_react_hitl.html | ED-3 |
| producer_agent_flow_animated | producer_agent_flow_animated.html | PR-1, PR-2, PR-3 |
| pr4_tool_use_react | pr4_tool_use_react.html | PR-4 |
| agentic_architecture_animated | agentic_architecture_animated.html | Overview |
| high_priority_tools_animated | high_priority_tools_animated.html | All 8 high-priority |

---

## Role name alignment

- **phase_roles.json** and **role_opportunities.json** use display names: `Producer`, `Production Coordinator`, `Creative Director`, `Post-Production Manager`, `Editor`.
- **time_allocations.json** and **ai_survey_summary.json** use plural keys: `Producers`, `Production Coordinators`, `Creative Directors`, `Post Production Managers`, `Editors`.
- **tool_dream_mapping.json** has both `role` (display) and `role_key` (for time_allocations lookup).
