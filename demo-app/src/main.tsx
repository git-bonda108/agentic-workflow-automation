import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { ErrorBoundary } from './ErrorBoundary';
import App from './App';
import './index.css';

function showError(msg: string): void {
  const rootEl = document.getElementById('root');
  if (rootEl) {
    rootEl.innerHTML =
      '<div style="padding:2rem;font-family:system-ui;max-width:560px;">' +
      '<h2 style="color:#c94b62;">App failed to start</h2>' +
      '<pre style="background:#f1f5f9;padding:1rem;overflow:auto;font-size:0.875rem;white-space:pre-wrap;">' +
      String(msg).replace(/</g, '&lt;') +
      '</pre>' +
      '<p><a href="http://localhost:3000" style="color:#E85D75;">Reload</a></p>' +
      '</div>';
  }
}

const rootElement = document.getElementById('root');
if (!rootElement) throw new Error('Failed to find the root element');
const root = createRoot(rootElement as HTMLElement);

try {
  root.render(
    <StrictMode>
      <ErrorBoundary>
        <App />
      </ErrorBoundary>
    </StrictMode>
  );
} catch (e) {
  const msg = e instanceof Error ? (e.message + (e.stack ? '\n\n' + e.stack : '')) : String(e);
  showError(msg);
}
