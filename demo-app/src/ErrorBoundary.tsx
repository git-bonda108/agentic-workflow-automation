import { Component, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError && this.state.error) {
      return (
        <div style={{ padding: '2rem', fontFamily: 'system-ui', maxWidth: '600px', margin: '0 auto' }}>
          <h1 style={{ color: '#c94b62' }}>Something went wrong</h1>
          <pre style={{ background: '#f1f5f9', padding: '1rem', overflow: 'auto', fontSize: '0.875rem' }}>
            {this.state.error.message}
          </pre>
          <p>Try <a href="/">refreshing</a> or use <strong>http://localhost:3000</strong> instead of the IP.</p>
        </div>
      );
    }
    return this.props.children;
  }
}
