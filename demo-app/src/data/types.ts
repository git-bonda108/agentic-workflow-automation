/** From phase_roles.json */
export interface Phase {
  id: string;
  phase: string;
  order: number;
  role_ids: string[];
  description: string;
}

export interface PhaseRolesData {
  pipeline_name: string;
  core_roles: string[];
  phases: Phase[];
}

/** From wishlist_tools.json (high_priority / medium_priority items) */
export interface WishlistTool {
  id: string;
  name: string;
  role: string;
  category: string;
  description: string;
}

/** From role_opportunities.json */
export interface RoleOpportunitiesData {
  role_tool_ids: Record<string, string[]>;
  priority_by_tool_id: Record<string, 'HIGH' | 'MEDIUM'>;
}

/** From tool_io.json */
export interface ToolIO {
  input: string[];
  output: string[];
}

/** From tool_integration.json */
export interface ToolIntegration {
  integration_type: string;
  tools_or_services: string[];
  description: string;
  gif_id: string;
}

/** From tool_dream_mapping.json */
export interface ToolDreamMapping {
  role: string;
  role_key: string;
  dream_impact_short: string;
  current_vs_dream: string;
  categories_affected: string[];
}

/** From time_allocations.json (role summary) */
export interface TimeAllocationRole {
  people: number;
  capacity_hours_per_week: number;
  current: Record<string, number>;
  dream: Record<string, number>;
  key_notes: string;
}

/** From ai_survey_summary.json */
export interface SurveyRole {
  role: string;
  count: number;
  pct: number;
  top_tools: { tool: string; count: number; pct: number }[];
  use_cases: string[];
  top_requests: string[];
}
