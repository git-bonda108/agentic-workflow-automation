import { Link } from 'react-router-dom';
import type { Phase } from '../data/types';

interface PhaseTileProps {
  phase: Phase;
}

export function PhaseTile({ phase }: PhaseTileProps) {
  const roleCount = phase.role_ids.length;
  const rolesLabel = roleCount === 0 ? 'Client handoff' : `${roleCount} role${roleCount !== 1 ? 's' : ''}`;

  return (
    <Link
      to={roleCount > 0 ? `/phase/${phase.id}` : '#'}
      className="phase-tile"
      style={roleCount === 0 ? { pointerEvents: 'none', opacity: 0.85 } : undefined}
    >
      <span className="phase-tile-order">{phase.order}</span>
      <h2 className="phase-tile-name">{phase.phase}</h2>
      <p className="phase-tile-roles">{rolesLabel}</p>
      <p className="phase-tile-desc">{phase.description}</p>
      {roleCount > 0 && <span className="phase-tile-cta">View roles & opportunities →</span>}
    </Link>
  );
}
