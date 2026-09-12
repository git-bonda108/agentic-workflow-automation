import { Link } from 'react-router-dom';
import { usePhaseRoles } from '../data/usePipeline';
import { Phase } from '../data/types';
import './Pipeline.css';

function PhaseNode({ phase }: { phase: Phase }) {
  const roleCount = phase.role_ids.length;
  const to = roleCount > 0 ? `/phase/${phase.id}` : undefined;

  return (
    <div className="pipeline-phase-node">
      {to ? (
        <Link to={to} className="pipeline-phase-link card">
          <span className="pipeline-phase-num">{phase.order}</span>
          <h2 className="pipeline-phase-name">{phase.phase}</h2>
          <p className="pipeline-phase-roles">
            {roleCount === 0 ? 'Client handoff' : `${roleCount} role${roleCount !== 1 ? 's' : ''}`}
          </p>
          <p className="pipeline-phase-desc">{phase.description}</p>
          <span className="pipeline-phase-cta">View roles & opportunities →</span>
        </Link>
      ) : (
        <div className="pipeline-phase-link card" style={{ opacity: 0.85, cursor: 'default' }}>
          <span className="pipeline-phase-num">{phase.order}</span>
          <h2 className="pipeline-phase-name">{phase.phase}</h2>
          <p className="pipeline-phase-roles">Client handoff</p>
          <p className="pipeline-phase-desc">{phase.description}</p>
        </div>
      )}
    </div>
  );
}

const FLOW_NODES = [
  { key: 'input', title: 'User Input', sub: 'Create task\ntags: Mango', state: 'done' as const },
  { key: 'reason', title: 'Reason', sub: 'Agent Reasoning\nParse task\nExtract tags', state: 'done' as const },
  { key: 'tool', title: 'Tool Call', sub: 'ClickUp API\ncreate_task', state: 'done' as const },
  { key: 'hitl', title: 'HITL', sub: 'Human Approval\nApprove task', state: 'waiting' as const },
  { key: 'execute', title: 'Execute', sub: 'Log task\nApply tags', state: 'idle' as const },
  { key: 'result', title: 'Result', sub: 'Task Created\nClickUp updated', state: 'idle' as const },
];

export function Pipeline() {
  const { data, loading, error } = usePhaseRoles();

  if (loading) {
    return (
      <div className="page-container">
        <div className="pipeline pipeline--loading" style={{ color: '#4b5563' }}>
          <p>Loading pipeline…</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container">
        <div className="pipeline pipeline--error">
          <p>Failed to load pipeline: {error.message}</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="page-container">
        <div className="pipeline pipeline--error">
          <p>No pipeline data. Check that <code>/mock_data/phase_roles.json</code> exists.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container pipeline">
      <div className="pipeline-intro content">
        <h1 className="pipeline-title">{data.pipeline_name}</h1>
        <p className="pipeline-subtitle">
          Select a phase to see roles and agentic AI opportunities. Use the Claude-to-ClickUp agent (PR-4) to enter task text and log it to ClickUp with tags and dependencies.
        </p>
        <p style={{ marginTop: '12px' }}>
          <Link to="/opportunity/PR-4" className="pipeline-cta-link">Create task with natural language (Claude-to-ClickUp PR-4) →</Link>
        </p>
      </div>

      <section className="pipeline-visualization section">
        <h3>Pipeline visualization</h3>
        <div className="pipeline-container">
          {FLOW_NODES.flatMap((node, i) => [
            <div key={node.key} className={`pipeline-node ${node.state}`}>
              <div className="pipeline-node-title">{node.title}</div>
              <div className="pipeline-node-sub" style={{ whiteSpace: 'pre-line' }}>{node.sub}</div>
            </div>,
            ...(i < FLOW_NODES.length - 1
              ? [<div key={`arrow-${node.key}`} className={`pipeline-arrow ${node.state === 'done' ? 'active' : ''}`} aria-hidden />]
              : [])
          ])}
        </div>
        <div className="execution-log">
          <strong>Execution log</strong>
          <ul>
            <li>✔ Parsed input</li>
            <li>✔ Extracted tags</li>
            <li>✔ Resolved ClickUp list</li>
            <li>⏳ Waiting for approval</li>
          </ul>
        </div>
      </section>

      <h3 style={{ marginTop: '40px', marginBottom: '12px' }}>Phases & roles</h3>
      <div className="pipeline-flow" role="list">
        {data.phases.map((phase) => (
          <PhaseNode key={phase.id} phase={phase} />
        ))}
      </div>
    </div>
  );
}
