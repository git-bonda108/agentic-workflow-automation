import { Outlet, Link, useLocation } from 'react-router-dom';
import './Layout.css';

export function Layout() {
  const location = useLocation();
  return (
    <div className="layout">
      <header className="layout-header">
        <div className="layout-header-left">
          <Link to="/" className="layout-logo">
            Dragonfruit
          </Link>
          <span className="layout-tagline">Plan, Reason and Act</span>
        </div>
        <nav className="layout-nav" aria-label="Main">
          <Link to="/" className={location.pathname === '/' ? 'layout-nav-link active' : 'layout-nav-link'}>Pipeline</Link>
          <Link to="/trajectory" className={location.pathname === '/trajectory' ? 'layout-nav-link active' : 'layout-nav-link'}>Trajectory</Link>
          <Link to="/mcp-config" className={location.pathname === '/mcp-config' ? 'layout-nav-link active' : 'layout-nav-link'}>MCP config</Link>
        </nav>
        <div className="layout-pills">
          <span className="layout-pill layout-pill-mock" title="Run demo uses mock until backend is wired">Mock</span>
          <span className="layout-pill layout-pill-mcp" title="ClickUp, Slack, Notion">ClickUp MCP</span>
          <span className="layout-pill layout-pill-sdk" title="OpenAI Agents SDK">OpenAI Agents SDK</span>
          <span className="layout-pill layout-pill-api" title="Frame.io, YouTube via API">Frame.io API</span>
        </div>
        <span className="layout-url" title="Bookmark this URL">
          {typeof window !== 'undefined' && window.location.origin}
        </span>
      </header>
      <main className="layout-main">
        <Outlet />
      </main>
    </div>
  );
}
