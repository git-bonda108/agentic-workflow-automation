import { useState } from 'react';
import { Link } from 'react-router-dom';
import './TrajectoryPage.css';

const GIF_LIST: { id: string; title: string; description: string }[] = [
  { id: 'agentic_architecture_animated', title: 'Agentic architecture', description: 'Orchestration layer and tool binding (MCP + API).' },
  { id: 'high_priority_tools_animated', title: 'High-priority tools overview', description: 'All 8 high-priority wish-list tools at a glance.' },
  { id: 'cd_agent_flow_animated', title: 'Creative Director agent flow', description: 'CD tools: retention, outlier ideation, packaging, A/B monitor.' },
  { id: 'ppm_ed_flow_animated', title: 'PPM / Editor flow', description: 'Frame.io sentiment, automated QC (ED-1, ED-2).' },
  { id: 'ed3_capacity_react_hitl', title: 'ED-3 Capacity assignment (HITL)', description: 'Suggested assignees and human-in-the-loop confirm.' },
  { id: 'producer_agent_flow_animated', title: 'Producer agent flow', description: 'Timeline calculator, sentiment tracker, Slack templates.' },
  { id: 'pr4_tool_use_react', title: 'PR-4 Claude-to-ClickUp', description: 'Natural language → task create via ClickUp MCP.' },
  { id: 'multi_agent_handoffs_orchestrator', title: 'Multi-agent handoffs', description: 'Orchestrator and role-agent delegation.' },
  { id: 'sdk_primitives_numbered_agents', title: 'SDK primitives', description: 'Agents, tools, guardrails, handoffs.' },
];

export function TrajectoryPage() {
  const [selectedId, setSelectedId] = useState<string | null>(GIF_LIST[0]?.id ?? null);
  const selected = GIF_LIST.find((g) => g.id === selectedId);

  return (
    <div className="trajectory-page">
      <nav className="trajectory-breadcrumb">
        <Link to="/">Pipeline</Link>
        <span aria-hidden> / </span>
        <span>Agent trajectory</span>
      </nav>
      <h1 className="trajectory-title">Agent trajectory</h1>
      <p className="trajectory-subtitle">
        Select a flow to see how the agent reasons, plans, and executes. All GIFs use the same palette and fonts as the app.
      </p>
      <div className="trajectory-layout">
        <aside className="trajectory-sidebar">
          <h2 className="trajectory-sidebar-title">Flows</h2>
          <ul className="trajectory-list">
            {GIF_LIST.map((g) => (
              <li key={g.id}>
                <button
                  type="button"
                  className={`trajectory-list-btn ${selectedId === g.id ? 'active' : ''}`}
                  onClick={() => setSelectedId(g.id)}
                >
                  <span className="trajectory-list-title">{g.title}</span>
                  <span className="trajectory-list-desc">{g.description}</span>
                </button>
              </li>
            ))}
          </ul>
        </aside>
        <section className="trajectory-viewer">
          {selected ? (
            <>
              <h2 className="trajectory-viewer-title">{selected.title}</h2>
              <p className="trajectory-viewer-desc">{selected.description}</p>
              <div className="trajectory-gif-wrap">
                <iframe title={selected.title} src={`/gifs/${selected.id}.html`} />
              </div>
            </>
          ) : (
            <p className="trajectory-placeholder">Select a flow from the list.</p>
          )}
        </section>
      </div>
      <p style={{ marginTop: '1.5rem' }}>
        <Link to="/" className="trajectory-back">← Back to pipeline</Link>
      </p>
    </div>
  );
}
