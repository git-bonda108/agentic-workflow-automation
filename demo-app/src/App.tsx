import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Pipeline } from './pages/Pipeline';
import { PhaseDetail } from './pages/PhaseDetail';
import { OpportunityDetailPage } from './pages/OpportunityDetailPage';
import { TrajectoryPage } from './pages/TrajectoryPage';
import { MCPConfigPage } from './pages/MCPConfigPage';
import './theme/colors.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Pipeline />} />
          <Route path="phase/:phaseId" element={<PhaseDetail />} />
          <Route path="opportunity/:toolId" element={<OpportunityDetailPage />} />
          <Route path="trajectory" element={<TrajectoryPage />} />
          <Route path="mcp-config" element={<MCPConfigPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
