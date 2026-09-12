import { useState, useEffect } from 'react';
import type { PhaseRolesData } from './types';

const PHASE_ROLES_URL = '/mock_data/phase_roles.json';

export function usePhaseRoles(): {
  data: PhaseRolesData | null;
  loading: boolean;
  error: Error | null;
} {
  const [data, setData] = useState<PhaseRolesData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetch(PHASE_ROLES_URL)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  return { data, loading, error };
}
