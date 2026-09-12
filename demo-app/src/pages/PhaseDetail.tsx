import { useParams, Link } from 'react-router-dom';
import { usePhaseRoles } from '../data/usePipeline';
import { useSurvey, useTimeAllocations, useRoleOpportunities, useWishlistTools } from '../data/useAppData';
import './PhaseDetail.css';

export function PhaseDetail() {
  const { phaseId } = useParams<{ phaseId: string }>();
  const { data, loading, error } = usePhaseRoles();
  const { getByRole: getSurvey } = useSurvey();
  const { getByRoleKey } = useTimeAllocations();
  const { getToolIdsForRole, getPriority } = useRoleOpportunities();
  const { getById: getTool } = useWishlistTools();

  if (loading || error || !data) {
    return (
      <div className="page-container phase-detail">
        {loading && <p style={{ color: '#4b5563' }}>Loading…</p>}
        {error && <p style={{ color: 'var(--df-accent)' }}>Error: {error.message}</p>}
        {!data && !loading && !error && <p style={{ color: '#4b5563' }}>No data.</p>}
      </div>
    );
  }

  const phase = data.phases.find((p) => p.id === phaseId);
  if (!phase) {
    return (
      <div className="page-container phase-detail">
        <p style={{ color: '#4b5563' }}>Phase not found.</p>
        <Link to="/">Back to pipeline</Link>
      </div>
    );
  }

  return (
    <div className="page-container phase-detail">
      <nav className="phase-detail-breadcrumb">
        <Link to="/">Pipeline</Link>
        <span aria-hidden> / </span>
        <span>{phase.phase}</span>
      </nav>
      <h1 className="phase-detail-title">{phase.phase}</h1>
      <p className="phase-detail-desc">{phase.description}</p>
      <div className="phase-detail-roles">
        <h2>Roles in this phase</h2>
        <div className="role-cards">
          {phase.role_ids.map((roleId) => {
            const survey = getSurvey(roleId);
            const roleKey =
              roleId === 'Post-Production Manager' ? 'Post Production Managers' :
              roleId === 'Production Coordinator' ? 'Production Coordinators' :
              roleId === 'Creative Director' ? 'Creative Directors' :
              roleId === 'Producer' ? 'Producers' : 'Editors';
            const timeAlloc = getByRoleKey(roleKey);
            const toolIds = getToolIdsForRole(roleId);

            return (
              <div key={roleId} className="role-card">
                <h3 className="role-card-title">{roleId}</h3>
                {survey && (
                  <div className="role-card-section">
                    <div className="role-card-label">Currently using</div>
                    <div className="role-card-value">
                      {survey.top_tools.slice(0, 4).map((t) => `${t.tool} ${Math.round(t.pct * 100)}%`).join(', ')}
                      {survey.use_cases.length > 0 && (
                        <> · Use cases: {survey.use_cases.slice(0, 3).join(', ')}</>
                      )}
                    </div>
                  </div>
                )}
                {timeAlloc?.key_notes && (
                  <div className="role-card-section">
                    <div className="role-card-label">Dream allocation</div>
                    <div className="role-card-dream">{timeAlloc.key_notes}</div>
                  </div>
                )}
                <div className="role-card-section">
                  <div className="role-card-label">Opportunities (wish list)</div>
                  <ul className="opportunity-list">
                    {toolIds.map((tid) => {
                      const tool = getTool(tid);
                      const priority = getPriority(tid);
                      return (
                        <li key={tid}>
                          <Link to={`/opportunity/${tid}`} className="opportunity-link">
                            <span className={`priority-badge ${priority.toLowerCase()}`}>{priority}</span>
                            {tool ? tool.name : tid}
                          </Link>
                        </li>
                      );
                    })}
                  </ul>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
