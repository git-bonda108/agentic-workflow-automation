import { useState, useEffect, useMemo } from 'react';

const BASE = '/mock_data';

export interface SurveyRole {
  role: string;
  count: number;
  pct: number;
  top_tools: { tool: string; count: number; pct: number }[];
  use_cases: string[];
  top_requests: string[];
}

export interface TimeAllocationRole {
  people: number;
  capacity_hours_per_week: number;
  current: Record<string, number>;
  dream: Record<string, number>;
  key_notes: string;
}

export interface WishlistTool {
  id: string;
  name: string;
  role: string;
  category: string;
  description: string;
}

const ROLE_TO_SURVEY_KEY: Record<string, string> = {
  'Producer': 'Producers',
  'Production Coordinator': 'Production Coordinators',
  'Creative Director': 'Creative Directors',
  'Post-Production Manager': 'Post Production Managers',
  'Editor': 'Editors',
};

export function useSurvey() {
  const [data, setData] = useState<{ roles: SurveyRole[] } | null>(null);
  useEffect(() => {
    fetch(`${BASE}/ai_survey_summary.json`).then((r) => r.json()).then(setData).catch(() => setData(null));
  }, []);
  const getByRole = useMemo(() => {
    if (!data?.roles) return () => null;
    const map = new Map(data.roles.map((r) => [r.role, r]));
    return (displayRole: string) => map.get(ROLE_TO_SURVEY_KEY[displayRole] ?? displayRole) ?? null;
  }, [data]);
  return { data, getByRole };
}

export function useTimeAllocations() {
  const [data, setData] = useState<{ roles: Record<string, TimeAllocationRole> } | null>(null);
  useEffect(() => {
    fetch(`${BASE}/time_allocations.json`).then((r) => r.json()).then(setData).catch(() => setData(null));
  }, []);
  const getByRoleKey = useMemo(() => {
    if (!data?.roles) return () => null;
    return (roleKey: string) => data.roles[roleKey] ?? null;
  }, [data]);
  return { data, getByRoleKey };
}

export function useRoleOpportunities() {
  const [data, setData] = useState<{
    role_tool_ids: Record<string, string[]>;
    priority_by_tool_id: Record<string, string>;
  } | null>(null);
  useEffect(() => {
    fetch(`${BASE}/role_opportunities.json`).then((r) => r.json()).then(setData).catch(() => setData(null));
  }, []);
  const getToolIdsForRole = (role: string) => (data?.role_tool_ids[role] ?? []);
  const getPriority = (toolId: string) => (data?.priority_by_tool_id[toolId] ?? 'MEDIUM');
  return { data, getToolIdsForRole, getPriority };
}

export function useWishlistTools() {
  const [tools, setTools] = useState<WishlistTool[]>([]);
  useEffect(() => {
    fetch(`${BASE}/wishlist_tools.json`)
      .then((r) => r.json())
      .then((d: { high_priority?: WishlistTool[]; medium_priority?: WishlistTool[] }) => {
        const list = [...(d.high_priority ?? []), ...(d.medium_priority ?? [])];
        setTools(list);
      })
      .catch(() => setTools([]));
  }, []);
  const getById = (id: string) => tools.find((t) => t.id === id) ?? null;
  return { tools, getById };
}

export function useToolExtra(toolId: string | undefined) {
  const [io, setIO] = useState<{ input: string[]; output: string[] } | null>(null);
  const [integration, setIntegration] = useState<{
    integration_type: string;
    tools_or_services: string[];
    description: string;
    gif_id: string;
  } | null>(null);
  const [dream, setDream] = useState<{
    role: string;
    role_key: string;
    dream_impact_short: string;
    current_vs_dream: string;
    categories_affected: string[];
  } | null>(null);

  useEffect(() => {
    if (!toolId) return;
    Promise.all([
      fetch(`${BASE}/tool_io.json`).then((r) => r.json()),
      fetch(`${BASE}/tool_integration.json`).then((r) => r.json()),
      fetch(`${BASE}/tool_dream_mapping.json`).then((r) => r.json()),
    ])
      .then(([ioData, intData, dreamData]) => {
        setIO(ioData.tools?.[toolId] ?? null);
        setIntegration(intData.tools?.[toolId] ?? null);
        setDream(dreamData.tools?.[toolId] ?? null);
      })
      .catch(() => {
        setIO(null);
        setIntegration(null);
        setDream(null);
      });
  }, [toolId]);

  return { io, integration, dream };
}

export interface AgentFlowTool {
  hitl_gates: { stage: string; description: string }[];
  reasoning: string;
  planning: string;
  executing: string;
  tool_calls: { tool: string; purpose: string }[];
  outputs_by_stage: { stage: string; output: string }[];
  utilization_estimate?: {
    hours_saved_per_week: string;
    percent_shift: string;
    benefit_beyond_sheet: string;
  };
}

export interface UtilizationSummary {
  source_sheet: string;
  benefit_beyond_sheet: string;
  role_highlights: string[];
  utilization_table?: { role: string; shift: string; benefit: string }[];
  quantified_gains?: { metric: string; value: string; detail: string }[];
}

export function useToolAgentFlow(toolId: string | undefined) {
  const [flow, setFlow] = useState<AgentFlowTool | null>(null);
  const [utilizationSummary, setUtilizationSummary] = useState<UtilizationSummary | null>(null);

  useEffect(() => {
    if (!toolId) return;
    fetch(`${BASE}/tool_agent_flow.json`)
      .then((r) => r.json())
      .then((data: { tools?: Record<string, AgentFlowTool>; utilization_summary?: UtilizationSummary }) => {
        setFlow(data.tools?.[toolId] ?? null);
        setUtilizationSummary(data.utilization_summary ?? null);
      })
      .catch(() => {
        setFlow(null);
        setUtilizationSummary(null);
      });
  }, [toolId]);

  return { flow, utilizationSummary };
}
