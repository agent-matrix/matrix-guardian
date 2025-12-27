/**
 * Application Constants
 * Centralized location for all application-wide constants
 */

export const NAV_ITEMS = [
  { id: 'dashboard', label: 'Guardian Control', icon: 'ShieldCheck' },
  { id: 'threads', label: 'Interventions (HITL)', icon: 'GitBranch' },
  { id: 'probes', label: 'Probes & Status', icon: 'Radio' },
  { id: 'config', label: 'Policy Config', icon: 'Settings' },
];

export const GRAPH_NODES = [
  { id: 'schedule', label: 'Scheduler', icon: 'Clock', status: 'active' },
  { id: 'observe', label: 'Observer', icon: 'Eye', status: 'active' },
  { id: 'plan', label: 'Planner', icon: 'Cpu', status: 'processing' },
  { id: 'policy', label: 'Policy Gate', icon: 'ShieldAlert', status: 'waiting' },
  { id: 'act', label: 'Executor', icon: 'Zap', status: 'idle' }
];

export const RISK_THRESHOLDS = {
  LOW: 20,
  MEDIUM: 50,
  HIGH: 80
};

export const STATUS_COLORS = {
  CONNECTED: 'bg-emerald-500',
  OK: 'bg-emerald-500',
  DEGRADED: 'bg-amber-500',
  ERROR: 'bg-rose-500',
  DISCONNECTED: 'bg-rose-500'
};

export const THREAD_STATUS = {
  RUNNING: 'RUNNING',
  PAUSED: 'PAUSED',
  COMPLETED: 'COMPLETED',
  FAILED: 'FAILED'
};

export const PROBE_TYPES = {
  HTTP: 'HTTP',
  MCP: 'MCP',
  TCP: 'TCP'
};
