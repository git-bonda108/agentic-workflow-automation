import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useSurvey, useWishlistTools, useToolExtra, useRoleOpportunities, useToolAgentFlow } from '../data/useAppData';
import './OpportunityDetailPage.css';

const API_BASE = 'http://localhost:8000';

type DemoSource = 'mock' | 'mcp' | 'api' | null;

type ParsedPayload = {
  task_name: string;
  due_date: string;
  due_date_ms: number | null;
  assignee: string;
  list_or_pod: string;
  tags: string[];
  dependencies: string;
  message: string;
};

export function OpportunityDetailPage() {
  const { toolId } = useParams<{ toolId: string }>();
  const { getByRole: getSurvey } = useSurvey();
  const { getById: getTool } = useWishlistTools();
  const { getPriority } = useRoleOpportunities();
  const { io, integration, dream } = useToolExtra(toolId ?? undefined);
  const { flow, utilizationSummary } = useToolAgentFlow(toolId ?? undefined);
  const [demoRan, setDemoRan] = useState(false);
  const [demoOutput, setDemoOutput] = useState<string | null>(null);
  const [demoReasoning, setDemoReasoning] = useState<string | null>(null);
  const [demoSource, setDemoSource] = useState<DemoSource>(null);
  const [demoLoading, setDemoLoading] = useState(false);
  const [demoTaskLink, setDemoTaskLink] = useState<string | null>(null);
  // PR-4: LLM text box (replaces Slack) → parse → confirm → log to ClickUp
  const [agentPrompt, setAgentPrompt] = useState('');
  const [agentLoading, setAgentLoading] = useState(false);
  const [agentConfirming, setAgentConfirming] = useState(false);
  const [parsedPayload, setParsedPayload] = useState<ParsedPayload | null>(null);
  const [agentResult, setAgentResult] = useState<{ success: boolean; message: string; task_link?: string; reasoning: string; steps: string[] } | null>(null);

  const tool = toolId ? getTool(toolId) : null;
  const survey = tool ? getSurvey(tool.role) : null;
  const priority = toolId ? getPriority(toolId) : 'MEDIUM';

  if (!toolId) {
    return (
      <div className="opportunity-detail-page">
        <p style={{ color: 'var(--df-text)' }}>No tool selected.</p>
        <Link to="/">Back to pipeline</Link>
      </div>
    );
  }
  const gifId = integration?.gif_id ?? 'high_priority_tools_animated';
  const gifSrc = `/gifs/${gifId}.html`;

  return (
    <div className="opportunity-detail-page">
      <nav className="opportunity-breadcrumb">
        <Link to="/">Pipeline</Link>
        <span aria-hidden> / </span>
        <span>Opportunity</span>
        <span aria-hidden> / </span>
        <span>{tool?.name ?? toolId}</span>
      </nav>

      <header className="opp-header">
        <h1 className="opp-title">{tool?.name ?? toolId}</h1>
        <p className="opp-meta">
          {toolId} · {tool?.role ?? '—'}
          <span className={`priority-badge ${priority.toLowerCase()}`}>{priority}</span>
        </p>
        {tool?.description && <p style={{ color: 'var(--df-text)', fontSize: '0.9375rem', marginTop: '0.5rem' }}>{tool.description}</p>}
      </header>

      {survey && (
        <section className="opp-section">
          <h2 className="opp-section-title">This role today (AI Tool Survey)</h2>
          <p>
            {survey.top_tools.slice(0, 3).map((t) => `${t.tool} ${Math.round(t.pct * 100)}%`).join(', ')}
            {survey.use_cases.length > 0 && <> · {survey.use_cases.slice(0, 3).join(', ')}</>}
          </p>
        </section>
      )}

      {io && (
        <>
          <section className="opp-section">
            <h2 className="opp-section-title">Input</h2>
            <ul>
              {io.input.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </section>
          <section className="opp-section">
            <h2 className="opp-section-title">Output</h2>
            <ul>
              {io.output.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </section>
        </>
      )}

      {toolId === 'PR-4' && (
        <section className="opp-section opp-llm-card">
          <h2 className="opp-section-title">LLM text input (replaces Slack) — log task to ClickUp</h2>
          <p className="opp-section-desc">
            Enter task in plain language. The agent parses it (OpenAI LLM or fallback), extracts name, due date, tags (e.g. Mango, Lemon), and dependencies, then logs the task to ClickUp after you confirm (HITL).
          </p>
          <textarea
            className="opp-agent-input"
            placeholder="e.g. Create task for Mango Pod, longform edit Client Alpha, due Friday, tags Mango, Lemon. Depends on: style lock."
            value={agentPrompt}
            onChange={(e) => setAgentPrompt(e.target.value)}
            rows={3}
            disabled={agentLoading || agentConfirming}
          />
          <button
            type="button"
            className="opp-demo-btn"
            disabled={agentLoading || agentConfirming || !agentPrompt.trim()}
            onClick={async () => {
              if (!agentPrompt.trim()) return;
              setAgentLoading(true);
              setAgentResult(null);
              setParsedPayload(null);
              try {
                const res = await fetch(`${API_BASE}/api/agent/parse`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ prompt: agentPrompt.trim() }) });
                const json = await res.json();
                if (json.success) {
                  setParsedPayload({
                    task_name: json.task_name ?? '',
                    due_date: json.due_date ?? '',
                    due_date_ms: json.due_date_ms ?? null,
                    assignee: json.assignee ?? '',
                    list_or_pod: json.list_or_pod ?? '',
                    tags: Array.isArray(json.tags) ? json.tags : [],
                    dependencies: json.dependencies ?? '',
                    message: json.message ?? '',
                  });
                } else {
                  setAgentResult({ success: false, message: json.message ?? 'Parse failed.', reasoning: '', steps: [] });
                }
              } catch {
                setAgentResult({ success: false, message: 'Backend not reached. Start backend with: npm run backend', reasoning: '', steps: [] });
              } finally {
                setAgentLoading(false);
              }
            }}
          >
            {agentLoading ? 'Agent is planning…' : 'Plan & extract'}
          </button>
          {parsedPayload && (
            <div className="opp-agent-confirm">
              <h3 className="opp-agent-confirm-title">Confirm before create (HITL)</h3>
              <p className="opp-section-desc">{parsedPayload.message}</p>
              <dl className="opp-agent-confirm-fields">
                <dt>Task name</dt>
                <dd>{parsedPayload.task_name}</dd>
                {parsedPayload.due_date && (<><dt>Due date</dt><dd>{parsedPayload.due_date}</dd></>)}
                {parsedPayload.assignee && (<><dt>Assignee</dt><dd>{parsedPayload.assignee}</dd></>)}
                {parsedPayload.list_or_pod && (<><dt>List / pod</dt><dd>{parsedPayload.list_or_pod}</dd></>)}
                {parsedPayload.tags.length > 0 && (<><dt>Tags</dt><dd>{parsedPayload.tags.join(', ')}</dd></>)}
                {parsedPayload.dependencies && (<><dt>Dependencies</dt><dd>{parsedPayload.dependencies}</dd></>)}
              </dl>
              <div className="opp-agent-confirm-actions">
                <button type="button" className="opp-demo-btn" disabled={agentConfirming} onClick={async () => {
                  if (!parsedPayload || !agentPrompt.trim()) return;
                  setAgentConfirming(true);
                  setAgentResult(null);
                  try {
                    const res = await fetch(`${API_BASE}/api/agent/confirm-create`, {
                      method: 'POST', headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({
                        prompt: agentPrompt.trim(),
                        task_name: parsedPayload.task_name,
                        due_date: parsedPayload.due_date,
                        due_date_ms: parsedPayload.due_date_ms,
                        assignee: parsedPayload.assignee,
                        list_or_pod: parsedPayload.list_or_pod,
                        tags: parsedPayload.tags,
                        dependencies: parsedPayload.dependencies,
                      }),
                    });
                    const json = await res.json();
                    setAgentResult({ success: json.success ?? false, message: json.message ?? '', task_link: json.task_link, reasoning: json.reasoning ?? '', steps: Array.isArray(json.steps) ? json.steps : [] });
                    setParsedPayload(null);
                  } catch {
                    setAgentResult({ success: false, message: 'Backend not reached.', reasoning: '', steps: [] });
                  } finally {
                    setAgentConfirming(false);
                  }
                }}>
                  {agentConfirming ? 'Creating task…' : 'Confirm & create'}
                </button>
                <button type="button" className="opp-demo-btn opp-demo-btn-cancel" disabled={agentConfirming} onClick={() => setParsedPayload(null)}>Cancel</button>
              </div>
            </div>
          )}
          {agentResult && (
            <div className={`opp-demo-result-wrap ${agentResult.success ? 'success' : 'error'}`} style={{ marginTop: '1rem' }}>
              <p className="opp-demo-result">{agentResult.message}</p>
              {agentResult.task_link && <p><a href={agentResult.task_link} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--df-accent)' }}>Open task in ClickUp →</a></p>}
              {agentResult.steps.length > 0 && <ul className="opp-stages-list">{agentResult.steps.map((s, i) => <li key={i}>{s}</li>)}</ul>}
              <p className="opp-demo-reasoning">{agentResult.reasoning}</p>
            </div>
          )}
        </section>
      )}

      {flow?.hitl_gates && flow.hitl_gates.length > 0 && (
        <section className="opp-section">
          <h2 className="opp-section-title">HITL gates</h2>
          <p className="opp-section-desc">Human-in-the-loop checkpoints per DFM wish list documentation. Agent pauses for confirmation at these stages.</p>
          <ul className="opp-hitl-list">
            {flow.hitl_gates.map((gate, i) => (
              <li key={i}>
                <strong>{gate.stage}:</strong> {gate.description}
              </li>
            ))}
          </ul>
        </section>
      )}

      {flow && (
        <section className="opp-section">
          <h2 className="opp-section-title">Agent reasoning, planning & executing</h2>
          <p className="opp-section-desc">How the agent reasons, plans, and executes for this tool (per wish list documentation).</p>
          <div className="opp-agent-flow">
            <p><strong>Reasoning:</strong> {flow.reasoning}</p>
            <p><strong>Planning:</strong> {flow.planning}</p>
            <p><strong>Executing:</strong> {flow.executing}</p>
          </div>
        </section>
      )}

      {flow?.tool_calls && flow.tool_calls.length > 0 && (
        <section className="opp-section">
          <h2 className="opp-section-title">Tool calling</h2>
          <p className="opp-section-desc">Tools the agent invokes (MCP or API) and their purpose.</p>
          <ul className="opp-tool-calls-list">
            {flow.tool_calls.map((tc, i) => (
              <li key={i}><strong>{tc.tool}</strong> — {tc.purpose}</li>
            ))}
          </ul>
        </section>
      )}

      {flow?.outputs_by_stage && flow.outputs_by_stage.length > 0 && (
        <section className="opp-section">
          <h2 className="opp-section-title">Output at every stage</h2>
          <p className="opp-section-desc">Example outputs after each agent step (real ClickUp or mock).</p>
          <ul className="opp-stages-list">
            {flow.outputs_by_stage.map((s, i) => (
              <li key={i}><strong>{s.stage}:</strong> {s.output}</li>
            ))}
          </ul>
        </section>
      )}

      <section className="opp-section">
        <h2 className="opp-section-title">Run demo</h2>
        <p className="opp-section-desc">
          Start the backend in a second terminal (<code>npm run backend</code>) for live ClickUp (PR-4, ED-3). Otherwise uses local mock. Label: Mock, Live (MCP), or Live (API).
        </p>
        <button
          type="button"
          className="opp-demo-btn"
          disabled={demoLoading}
          onClick={async () => {
            setDemoLoading(true);
            setDemoRan(true);
            setDemoOutput(null);
            setDemoReasoning(null);
            setDemoSource(null);
            setDemoTaskLink(null);
            try {
              const url = toolId === 'PR-4'
                ? `${API_BASE}/api/demo/${toolId}?task_name=${encodeURIComponent('Demo: Script review by Fri')}`
                : `${API_BASE}/api/demo/${toolId ?? ''}`;
              const controller = new AbortController();
              const timeoutId = setTimeout(() => controller.abort(), 12000);
              const res = await fetch(url, { signal: controller.signal });
              clearTimeout(timeoutId);
              if (res.ok) {
                const data = await res.json();
                setDemoOutput(data.output ?? '');
                setDemoReasoning(data.reasoning ?? '');
                setDemoSource(data.source ?? 'mock');
                if (data.task_link) setDemoTaskLink(data.task_link);
              } else {
                throw new Error('Backend error');
              }
            } catch (e) {
              const msg = e instanceof Error && e.name === 'AbortError'
                ? 'Backend did not respond in 12s. Start it with: cd demo-app && npm run backend'
                : 'Backend not reached. Start with: cd demo-app && npm run backend';
              setDemoOutput(
                io
                  ? `Input (mock): ${io.input.slice(0, 2).join('; ')}\nOutput (mock): ${io.output.slice(0, 2).join('; ')}`
                  : `Mock run complete for ${tool?.name ?? toolId}.`
              );
              setDemoReasoning(msg);
              setDemoSource('mock');
            }
            setDemoLoading(false);
          }}
        >
          {demoLoading ? 'Running…' : 'Run demo'}
        </button>
        {demoRan && (
          <div className="opp-demo-result-wrap">
            {demoSource && (
              <span className={`opp-demo-badge opp-demo-badge-${demoSource}`}>
                {demoSource === 'mcp' ? 'Live (MCP)' : demoSource === 'api' ? 'Live (API)' : 'Mock'}
              </span>
            )}
            {demoOutput != null && (
              <div className="opp-demo-result">
                {demoOutput}
                {demoTaskLink && (
                  <p style={{ marginTop: '0.5rem' }}>
                    <a href={demoTaskLink} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--df-accent)' }}>Open task →</a>
                  </p>
                )}
              </div>
            )}
            {demoReasoning != null && (
              <div className="opp-demo-reasoning">
                <strong>Reasoning:</strong> {demoReasoning}
              </div>
            )}
          </div>
        )}
      </section>

      {integration && (
        <section className="opp-section opp-trajectory-section">
          <h2 className="opp-section-title">Agent trajectory</h2>
          <p className="opp-section-desc">How the agent reasons, plans, calls tools, and executes — same flow style as above. Integration: <strong>{integration.integration_type}</strong> ({integration.tools_or_services.join(', ')}).</p>
          <div className="opp-gif-wrap">
            <iframe title="Agent trajectory flow" src={gifSrc} />
          </div>
        </section>
      )}

      {integration && (
        <section className="opp-section">
          <h2 className="opp-section-title">Integration needs</h2>
          <p><strong>MCP or API:</strong> {integration.integration_type}</p>
          <p><strong>Tools used by agent:</strong> {integration.tools_or_services.join('; ')}</p>
          <p>{integration.description}</p>
        </section>
      )}

      {dream && (
        <section className="opp-section">
          <h2 className="opp-section-title">Dream allocation impact</h2>
          <p className="opp-dream-impact">{dream.dream_impact_short}</p>
          <p><strong>Current → dream:</strong> {dream.current_vs_dream}</p>
          {dream.categories_affected?.length > 0 && (
            <p>Categories affected: {dream.categories_affected.join(', ')}</p>
          )}
          {flow?.utilization_estimate && (
            <div className="opp-utilization-estimate">
              <p><strong>Est. utilization (agentic AI):</strong> {flow.utilization_estimate.hours_saved_per_week}</p>
              <p><strong>% shift:</strong> {flow.utilization_estimate.percent_shift}</p>
              <p><strong>Benefit beyond sheet:</strong> {flow.utilization_estimate.benefit_beyond_sheet}</p>
            </div>
          )}
        </section>
      )}

      {utilizationSummary && (
        <section className="opp-section opp-section-highlight">
          <h2 className="opp-section-title">Utilization & benefit (beyond sheet)</h2>
          <p className="opp-section-desc">From DFM Current vs. Dream Time Allocations; delivered via agentic AI with HITL gates.</p>
          <p className="opp-util-intro">{utilizationSummary.benefit_beyond_sheet}</p>
          {utilizationSummary.quantified_gains && utilizationSummary.quantified_gains.length > 0 && (
            <table className="opp-util-table">
              <thead>
                <tr>
                  <th>Metric</th>
                  <th>Value</th>
                  <th>Detail</th>
                </tr>
              </thead>
              <tbody>
                {utilizationSummary.quantified_gains.map((r, i) => (
                  <tr key={i}>
                    <td>{r.metric}</td>
                    <td><strong>{r.value}</strong></td>
                    <td>{r.detail}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          {utilizationSummary.utilization_table && utilizationSummary.utilization_table.length > 0 && (
            <table className="opp-util-table">
              <thead>
                <tr>
                  <th>Role</th>
                  <th>Utilization shift</th>
                  <th>Benefit</th>
                </tr>
              </thead>
              <tbody>
                {utilizationSummary.utilization_table.map((r, i) => (
                  <tr key={i}>
                    <td>{r.role}</td>
                    <td>{r.shift}</td>
                    <td><strong>{r.benefit}</strong></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          {(!utilizationSummary.utilization_table || utilizationSummary.utilization_table.length === 0) && (
            <ul className="opp-role-highlights">
              {utilizationSummary.role_highlights.map((h, i) => (
                <li key={i}>{h}</li>
              ))}
            </ul>
          )}
        </section>
      )}

      <p style={{ marginTop: '1.5rem' }}>
        <Link to="/" style={{ color: 'var(--df-accent)' }}>← Back to pipeline</Link>
      </p>
    </div>
  );
}
