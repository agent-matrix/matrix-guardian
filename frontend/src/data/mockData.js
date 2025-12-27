/**
 * Mock Data for Matrix Guardian Admin Interface
 * This file contains all mock data used throughout the application
 */

export const MOCK_STATUS = {
  service: 'matrix-guardian',
  version: 'v2.1.0-autopilot',
  uptime: '4d 12h 30m',
  db_connection: 'CONNECTED',
  hub_connection: 'CONNECTED',
  ai_connection: 'CONNECTED',
  autopilot: {
    enabled: true,
    safe_mode: true,
    interval_sec: 60,
    active_threads: 14,
    last_cycle: '2025-10-24T14:30:00Z',
    cycle_duration_ms: 450
  }
};

export const MOCK_THREADS = [
  {
    id: 'th_8x992a',
    status: 'PAUSED',
    agent: 'RemediationAgent',
    node: 'human_approval',
    created_at: '2m ago',
    risk_score: 85,
    summary: 'High risk remediation plan proposed for Service: checkout-api',
    plan: {
      action: 'scale_down',
      target: 'checkout-api',
      reason: 'Cost optimization anomaly detected',
      impact: 'Potential availability reduction during peak'
    }
  },
  {
    id: 'th_7b221c',
    status: 'RUNNING',
    agent: 'ObserverAgent',
    node: 'analyze_metrics',
    created_at: '10s ago',
    risk_score: 10,
    summary: 'Routine health probe analysis',
    plan: null
  },
  {
    id: 'th_3c445d',
    status: 'PAUSED',
    agent: 'PolicyAgent',
    node: 'policy_gate',
    created_at: '15m ago',
    risk_score: 60,
    summary: 'Configuration change request: ALLOWLIST_UPDATE',
    plan: {
      action: 'update_config',
      target: 'firewall-rules',
      reason: 'New MCP server registration',
      impact: 'Security boundary modification'
    }
  }
];

export const MOCK_PROBES = [
  { id: 'pb_1', name: 'Matrix-AI /readyz', type: 'HTTP', status: 'OK', latency: 45, last_check: '5s ago' },
  { id: 'pb_2', name: 'Matrix-Hub /health', type: 'HTTP', status: 'OK', latency: 12, last_check: '5s ago' },
  { id: 'pb_3', name: 'MCP: Echo Server', type: 'MCP', status: 'OK', latency: 120, last_check: '30s ago' },
  { id: 'pb_4', name: 'MCP: Postgres Tool', type: 'MCP', status: 'DEGRADED', latency: 850, last_check: '10s ago' },
];

export const MOCK_POLICY_YAML = `# Guardian Autopilot Policy
# Defines safety rails for autonomous actions

risk_thresholds:
  low: 20
  medium: 50
  high: 80

safe_actions:
  - "restart_pod"
  - "clear_cache"
  - "scale_up"

requires_approval:
  - "scale_down"
  - "delete_resource"
  - "update_firewall"

rate_limits:
  max_actions_per_hour: 10
  max_retries: 3
`;

export const MOCK_CONFIG_FLAGS = [
  { key: 'AUTOPILOT_ENABLED', value: 'true', type: 'bool' },
  { key: 'AUTOPILOT_SAFE_MODE', value: 'true', type: 'bool' },
  { key: 'AUTOPILOT_INTERVAL_SEC', value: '60', type: 'int' },
  { key: 'LOG_LEVEL', value: 'INFO', type: 'string' },
];

export const MOCK_SETTINGS = {
  provider: 'openai',
  providers: ['openai', 'claude', 'watsonx', 'ollama'],
  openai: { api_key: '', model: 'gpt-4o' },
  claude: { api_key: '', model: 'claude-3-5-sonnet' },
  watsonx: { api_key: '', project_id: '', model_id: 'ibm/granite-13b-chat-v2' },
  ollama: { base_url: 'http://localhost:11434', model: 'llama3' }
};

export const MOCK_MODELS = {
  openai: ['gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo'],
  claude: ['claude-3-5-sonnet', 'claude-3-opus'],
  watsonx: ['ibm/granite-13b-chat-v2', 'meta-llama/llama-3-70b'],
  ollama: ['llama3', 'mistral', 'gemma:7b']
};
