import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Service Layer for Matrix Guardian Backend

export const guardianAPI = {
  // Health & Readiness Checks
  healthz: () => api.get('/healthz'),
  readyz: () => api.get('/readyz'),

  // Autopilot Management
  getAutopilotStatus: () => api.get('/autopilot/status'),
  triggerPlanOnce: (targetUid = null) =>
    api.post('/autopilot/plan-once', null, {
      params: targetUid ? { target_uid: targetUid } : {}
    }),

  // Thread/Workflow Management (HITL)
  resumeThread: (threadId, decision, comment = null) =>
    api.post(`/threads/${threadId}/resume`, {
      decision,
      comment,
    }),

  // Additional endpoints for frontend features
  // Note: These need to be implemented in the backend
  getThreads: () => api.get('/threads'),
  getProbes: () => api.get('/probes'),
  getConfig: () => api.get('/config'),
  updateConfig: (config) => api.put('/config', config),

  // AI Provider Settings
  getAISettings: () => api.get('/settings/ai'),
  updateAISettings: (settings) => api.put('/settings/ai', settings),
  testAIConnection: (provider) => api.post(`/settings/ai/${provider}/test`),
  getAvailableModels: (provider) => api.get(`/settings/ai/${provider}/models`),
};

// Error handling interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default api;
