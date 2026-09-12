import { Link } from 'react-router-dom';
import './MCPConfigPage.css';

export function MCPConfigPage() {
  return (
    <div className="mcp-config-page">
      <nav className="mcp-config-breadcrumb">
        <Link to="/">Pipeline</Link>
        <span aria-hidden> / </span>
        <span>MCP configuration</span>
      </nav>
      <h1 className="mcp-config-title">Is it difficult to configure a prebuilt MCP server?</h1>
      <p className="mcp-config-lead">
        No. Three steps: choose a server, run it, wire it in the OpenAI Agents SDK. No custom protocol code.
      </p>
      <div className="mcp-config-steps">
        <section className="mcp-step">
          <span className="mcp-step-num">1</span>
          <h2 className="mcp-step-title">Choose a prebuilt server</h2>
          <p className="mcp-step-body">
            Use the <a href="https://github.com/modelcontextprotocol/servers" target="_blank" rel="noopener noreferrer">MCP servers registry</a> or npm. Examples: <code>@modelcontextprotocol/server-filesystem</code>, community <code>@nazruden/clickup-server</code>, Slack MCP, Notion MCP.
          </p>
        </section>
        <section className="mcp-step">
          <span className="mcp-step-num">2</span>
          <h2 className="mcp-step-title">Run the server</h2>
          <p className="mcp-step-body">
            <strong>Stdio (local):</strong> <code>npx -y @modelcontextprotocol/server-filesystem ./allowed-dir</code>. For ClickUp: set <code>CLICKUP_PERSONAL_TOKEN</code> and start the ClickUp MCP server (e.g. <code>npx -y @nazruden/clickup-server</code> or your chosen package).
          </p>
        </section>
        <section className="mcp-step">
          <span className="mcp-step-num">3</span>
          <h2 className="mcp-step-title">Wire it in the SDK</h2>
          <p className="mcp-step-body">
            In Python with the <a href="https://openai.github.io/openai-agents-python/" target="_blank" rel="noopener noreferrer">OpenAI Agents SDK</a>: create an MCP server instance (e.g. <code>MCPServerStdio</code> with <code>command</code> and <code>args</code>), then pass it to <code>Agent(mcp_servers=[server])</code>. The agent can now list and call the server’s tools like function tools.
          </p>
        </section>
      </div>
      <div className="mcp-config-refs">
        <h2 className="mcp-refs-title">References</h2>
        <ul className="mcp-refs-list">
          <li><a href="https://modelcontextprotocol.io/docs/getting-started/intro" target="_blank" rel="noopener noreferrer">Model Context Protocol — What is MCP?</a></li>
          <li><a href="https://openai.github.io/openai-agents-python/mcp/" target="_blank" rel="noopener noreferrer">OpenAI Agents SDK — MCP</a></li>
        </ul>
      </div>
      <p style={{ marginTop: '1.5rem' }}>
        <Link to="/" className="mcp-config-back">← Back to pipeline</Link>
      </p>
    </div>
  );
}
