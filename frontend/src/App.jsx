import React, { useState, useEffect, useRef } from 'react';
import {
  Activity,
  ShieldCheck,
  ShieldAlert,
  Server,
  Terminal,
  Bot,
  Play,
  Square,
  GitBranch,
  Command,
  Settings,
  Menu,
  Search,
  Clock,
  CheckCircle,
  XCircle,
  AlertTriangle,
  FileJson,
  Workflow,
  Cpu,
  Radio,
  Lock,
  Eye,
  EyeOff,
  RefreshCw,
  Zap,
  Network,
  X as XIcon
} from 'lucide-react';

import { guardianAPI } from './services/api';

/**
 * MATRIX GUARDIAN // CONTROL PLANE
 * Dedicated Admin Interface for the Matrix-Guardian Microservice
 */

// --- COMPONENTS ---

const StatusIndicator = ({ status, label }) => (
  <div className="flex items-center gap-2 bg-zinc-900/50 border border-white/5 px-3 py-1.5 rounded-lg">
    <div className={`w-2 h-2 rounded-full ${status === 'CONNECTED' || status === 'OK' ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
    <div className="flex flex-col">
      <span className="text-[10px] text-zinc-500 uppercase font-bold tracking-wider">{label}</span>
      <span className="text-xs text-zinc-300 font-mono">{status}</span>
    </div>
  </div>
);

const RiskBadge = ({ score }) => {
  let color = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
  if (score > 50) color = 'bg-amber-500/10 text-amber-400 border-amber-500/20';
  if (score > 80) color = 'bg-rose-500/10 text-rose-400 border-rose-500/20';

  return (
    <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${color}`}>
      RISK: {score}/100
    </span>
  );
};

const Card = ({ title, icon: Icon, children, className = '', action }) => (
  <div className={`bg-[#09090b] border border-white/10 rounded-xl overflow-hidden flex flex-col shadow-xl ${className}`}>
    {(title || Icon) && (
      <div className="px-4 py-3 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
        <div className="flex items-center gap-2">
          {Icon && <Icon size={16} className="text-emerald-500" />}
          <span className="text-xs font-bold text-zinc-300 uppercase tracking-widest">{title}</span>
        </div>
        {action}
      </div>
    )}
    <div className="p-4 flex-1 relative">{children}</div>
  </div>
);

// --- SETTINGS MODAL ---

const SettingsModal = ({ isOpen, onClose }) => {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('openai');
  const [models, setModels] = useState([]);
  const [loadingModels, setLoadingModels] = useState(false);
  const [saveStatus, setSaveStatus] = useState('');

  // Initial Load
  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      guardianAPI.getAISettings()
        .then(response => {
          setSettings(response.data);
          setLoading(false);
        })
        .catch(() => {
          // Fallback to default settings if API not available
          setSettings({
            provider: 'openai',
            providers: ['openai', 'claude', 'watsonx', 'ollama'],
            openai: { api_key: '', model: 'gpt-4o' },
            claude: { api_key: '', model: 'claude-3-5-sonnet' },
            watsonx: { api_key: '', project_id: '', model_id: 'ibm/granite-13b-chat-v2' },
            ollama: { base_url: 'http://localhost:11434', model: 'llama3' }
          });
          setLoading(false);
        });
    } else {
      setSaveStatus('');
    }
  }, [isOpen]);

  // Sync tab with active provider
  useEffect(() => {
    if (settings?.provider && !loading) {
      setActiveTab(settings.provider);
    }
  }, [settings?.provider, loading]);

  const updateField = (section, field, value) => {
    setSettings(prev => {
      if (!prev) return prev;
      return {
        ...prev,
        [section]: {
          ...prev[section],
          [field]: value
        }
      };
    });
  };

  const handleSave = () => {
    setSaveStatus('Saving...');
    guardianAPI.updateAISettings(settings)
      .then(() => {
        setSaveStatus('Settings Saved!');
        setTimeout(() => setSaveStatus(''), 2000);
      })
      .catch(() => {
        setSaveStatus('Failed to save');
        setTimeout(() => setSaveStatus(''), 2000);
      });
  };

  const loadProviderModels = (provider) => {
    setLoadingModels(true);
    setModels([]);
    guardianAPI.getAvailableModels(provider)
      .then(response => {
        setModels(response.data.models || []);
        setLoadingModels(false);
      })
      .catch(() => {
        // Fallback to mock data
        const mockModels = {
          openai: ['gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo'],
          claude: ['claude-3-5-sonnet', 'claude-3-opus'],
          watsonx: ['ibm/granite-13b-chat-v2', 'meta-llama/llama-3-70b'],
          ollama: ['llama3', 'mistral', 'gemma:7b']
        };
        setModels(mockModels[provider] || []);
        setLoadingModels(false);
      });
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] bg-black/80 backdrop-blur-sm flex items-center justify-center p-4" onClick={onClose}>
      <div className="w-full max-w-2xl bg-zinc-900 border border-white/10 rounded-xl shadow-2xl overflow-hidden flex flex-col max-h-[80vh]" onClick={e => e.stopPropagation()}>

        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-white/10 bg-zinc-900/50">
          <div className="flex items-center gap-2">
            <Settings size={18} className="text-emerald-400" />
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">System Configuration</h2>
          </div>
          <button onClick={onClose} className="text-zinc-400 hover:text-white transition-colors">
            <XIcon size={20} />
          </button>
        </div>

        {/* Content */}
        <div className="flex flex-1 overflow-hidden">
          {loading || !settings ? (
            <div className="flex-1 flex items-center justify-center p-12 text-zinc-500 gap-2">
              <RefreshCw size={16} className="animate-spin" /> Loading settings...
            </div>
          ) : (
            <>
              {/* Sidebar Tabs */}
              <div className="w-48 border-r border-white/5 bg-black/20 p-2 space-y-1">
                {settings.providers.map(p => (
                  <button
                    key={p}
                    onClick={() => setActiveTab(p)}
                    className={`w-full text-left px-3 py-2 rounded text-xs font-medium transition-all flex items-center justify-between ${
                      activeTab === p
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : 'text-zinc-400 hover:bg-white/5 hover:text-white border border-transparent'
                    }`}
                  >
                    {p.charAt(0).toUpperCase() + p.slice(1)}
                    {settings.provider === p && <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_5px_currentColor]" />}
                  </button>
                ))}
              </div>

              {/* Form Area */}
              <div className="flex-1 p-6 overflow-y-auto">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-bold text-white capitalize">{activeTab} Settings</h3>
                  <button
                    onClick={() => setSettings(prev => ({...prev, provider: activeTab}))}
                    disabled={settings.provider === activeTab}
                    className={`px-3 py-1 rounded text-[10px] font-bold uppercase tracking-wider border transition-all ${
                      settings.provider === activeTab
                        ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30 cursor-default'
                        : 'bg-zinc-800 text-zinc-400 border-zinc-700 hover:text-white hover:border-white/20'
                    }`}
                  >
                    {settings.provider === activeTab ? 'Active Provider' : 'Set as Active'}
                  </button>
                </div>

                <div className="space-y-4">
                  {/* Common Fields */}
                  {activeTab !== 'ollama' && (
                    <div>
                      <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-1.5">API Key</label>
                      <input
                        type="password"
                        value={settings[activeTab]?.api_key || ''}
                        onChange={(e) => updateField(activeTab, 'api_key', e.target.value)}
                        placeholder={`Enter ${activeTab} API key...`}
                        className="w-full bg-black border border-white/10 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                      />
                    </div>
                  )}

                  {activeTab === 'watsonx' && (
                    <div>
                      <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-1.5">Project ID</label>
                      <input
                        type="text"
                        value={settings[activeTab]?.project_id || ''}
                        onChange={(e) => updateField(activeTab, 'project_id', e.target.value)}
                        placeholder="WatsonX Project ID"
                        className="w-full bg-black border border-white/10 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                      />
                    </div>
                  )}

                  <div>
                    <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-1.5">Model Identifier</label>
                    <div className="flex gap-2">
                      <input
                        type="text"
                        value={settings[activeTab]?.model || settings[activeTab]?.model_id || ''}
                        onChange={(e) => updateField(activeTab, activeTab === 'watsonx' ? 'model_id' : 'model', e.target.value)}
                        className="flex-1 bg-black border border-white/10 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                      />
                      <button
                        onClick={() => loadProviderModels(activeTab)}
                        disabled={loadingModels}
                        className="px-3 bg-zinc-800 border border-white/10 rounded text-zinc-300 hover:text-white hover:bg-zinc-700 disabled:opacity-50"
                      >
                        {loadingModels ? <RefreshCw size={14} className="animate-spin" /> : <Search size={14} />}
                      </button>
                    </div>
                    {models.length > 0 && (
                      <select
                        className="w-full mt-2 bg-zinc-900 border border-white/10 rounded px-3 py-2 text-sm text-zinc-300 focus:outline-none"
                        onChange={(e) => updateField(activeTab, activeTab === 'watsonx' ? 'model_id' : 'model', e.target.value)}
                        defaultValue=""
                      >
                        <option value="" disabled>Select a detected model...</option>
                        {models.map(m => <option key={m} value={m}>{m}</option>)}
                      </select>
                    )}
                  </div>

                  <div>
                    <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-1.5">Base URL (Optional)</label>
                    <input
                      type="text"
                      value={settings[activeTab]?.base_url || ''}
                      onChange={(e) => updateField(activeTab, 'base_url', e.target.value)}
                      placeholder={activeTab === 'ollama' ? 'http://localhost:11434' : 'https://api...'}
                      className="w-full bg-black border border-white/10 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                    />
                  </div>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-white/10 bg-zinc-900/50 flex justify-between items-center">
          <div className="text-emerald-400 text-xs font-bold uppercase tracking-wider">{saveStatus}</div>
          <div className="flex gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded text-xs font-bold text-zinc-400 hover:text-white transition-colors"
            >
              CANCEL
            </button>
            <button
              onClick={handleSave}
              className="px-6 py-2 bg-emerald-600 text-white rounded text-xs font-bold uppercase tracking-wider hover:bg-emerald-500 transition-colors shadow-lg shadow-emerald-500/20"
            >
              Save Configuration
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// --- VIEWS ---

const DashboardView = ({ autopilotStatus, threads, setAutopilotStatus, onToggleAutopilot }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full auto-rows-min">
      {/* Autopilot Controller */}
      <Card title="Autopilot Controller" icon={Cpu} className="lg:col-span-2">
        <div className="flex flex-col md:flex-row gap-6 items-center justify-between h-full">
          <div className="flex items-center gap-6">
            <div className={`w-24 h-24 rounded-full border-4 flex items-center justify-center relative ${autopilotStatus.enabled ? 'border-emerald-500/20' : 'border-zinc-800'}`}>
              {autopilotStatus.enabled && (
                <div className="absolute inset-0 rounded-full border-4 border-emerald-500 border-t-transparent animate-spin" />
              )}
              <Bot size={40} className={autopilotStatus.enabled ? 'text-emerald-400' : 'text-zinc-600'} />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white mb-1">
                {autopilotStatus.enabled ? 'Autopilot Engaged' : 'System Standby'}
              </h2>
              <div className="text-sm text-zinc-400 font-mono mb-3">
                Agent Orchestration: {autopilotStatus.enabled ? 'ACTIVE' : 'PAUSED'}
              </div>
              <div className="flex gap-2">
                <button
                  onClick={onToggleAutopilot}
                  className={`px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider flex items-center gap-2 transition-all ${autopilotStatus.enabled ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20 hover:bg-rose-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 hover:bg-emerald-500/20'}`}
                >
                  {autopilotStatus.enabled ? <Square size={14} fill="currentColor" /> : <Play size={14} fill="currentColor" />}
                  {autopilotStatus.enabled ? 'Disengage' : 'Engage'}
                </button>
                <button
                  onClick={() => setAutopilotStatus(prev => ({ ...prev, safe_mode: !prev.safe_mode }))}
                  className={`px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider flex items-center gap-2 border transition-all ${autopilotStatus.safe_mode ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' : 'bg-amber-500/10 text-amber-400 border-amber-500/20'}`}
                >
                  <ShieldCheck size={14} />
                  Safe Mode: {autopilotStatus.safe_mode ? 'ON' : 'OFF'}
                </button>
              </div>
            </div>
          </div>

          {/* Mini Stats */}
          <div className="grid grid-cols-2 gap-4 w-full md:w-auto">
            <div className="bg-zinc-900 p-3 rounded border border-white/5 text-center">
              <div className="text-[10px] text-zinc-500 uppercase font-bold">Active Threads</div>
              <div className="text-xl font-mono text-white">{autopilotStatus.active_threads || 0}</div>
            </div>
            <div className="bg-zinc-900 p-3 rounded border border-white/5 text-center">
              <div className="text-[10px] text-zinc-500 uppercase font-bold">Cycle Time</div>
              <div className="text-xl font-mono text-emerald-400">{autopilotStatus.cycle_duration_ms || 0}ms</div>
            </div>
          </div>
        </div>
      </Card>

      {/* HITL Stats */}
      <Card title="Intervention Queue" icon={AlertTriangle} className="lg:col-span-1">
        <div className="flex flex-col h-full justify-center items-center">
          <div className="text-5xl font-mono font-bold text-amber-500 mb-2">
            {threads.filter(t => t.status === 'PAUSED').length}
          </div>
          <div className="text-xs text-zinc-500 uppercase tracking-widest font-bold">Pending Approvals</div>
          <div className="mt-6 w-full space-y-2">
            <div className="flex justify-between text-xs text-zinc-400">
              <span>Low Risk</span>
              <span className="text-white">{threads.filter(t => t.status === 'PAUSED' && t.risk_score <= 50).length}</span>
            </div>
            <div className="w-full h-1 bg-zinc-800 rounded-full overflow-hidden">
              <div className="h-full bg-emerald-500" style={{width: `${(threads.filter(t => t.status === 'PAUSED' && t.risk_score <= 50).length / Math.max(threads.filter(t => t.status === 'PAUSED').length, 1)) * 100}%`}} />
            </div>
            <div className="flex justify-between text-xs text-zinc-400">
              <span>Medium Risk</span>
              <span className="text-white">{threads.filter(t => t.status === 'PAUSED' && t.risk_score > 50 && t.risk_score <= 80).length}</span>
            </div>
            <div className="w-full h-1 bg-zinc-800 rounded-full overflow-hidden">
              <div className="h-full bg-amber-500" style={{width: `${(threads.filter(t => t.status === 'PAUSED' && t.risk_score > 50 && t.risk_score <= 80).length / Math.max(threads.filter(t => t.status === 'PAUSED').length, 1)) * 100}%`}} />
            </div>
            <div className="flex justify-between text-xs text-zinc-400">
              <span>High Risk</span>
              <span className="text-white">{threads.filter(t => t.status === 'PAUSED' && t.risk_score > 80).length}</span>
            </div>
            <div className="w-full h-1 bg-zinc-800 rounded-full overflow-hidden">
              <div className="h-full bg-rose-500" style={{width: `${(threads.filter(t => t.status === 'PAUSED' && t.risk_score > 80).length / Math.max(threads.filter(t => t.status === 'PAUSED').length, 1)) * 100}%`}} />
            </div>
          </div>
        </div>
      </Card>

      {/* Decision Graph Visualization (LangGraph Mock) */}
      <Card title="Agent Decision Graph" icon={Workflow} className="lg:col-span-3 min-h-[300px]">
        <div className="relative w-full h-full min-h-[250px] bg-[#050505] rounded-lg border border-white/5 flex items-center justify-center overflow-hidden">
          {/* Background Grid */}
          <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(#fff 1px, transparent 1px)', backgroundSize: '20px 20px' }} />

          {/* Graph Nodes */}
          <div className="flex items-center gap-16 relative z-10">
            {[
              { id: 'schedule', label: 'Scheduler', icon: Clock, status: 'active' },
              { id: 'observe', label: 'Observer', icon: Eye, status: 'active' },
              { id: 'plan', label: 'Planner', icon: Cpu, status: 'processing' },
              { id: 'policy', label: 'Policy Gate', icon: ShieldAlert, status: 'waiting' },
              { id: 'act', label: 'Executor', icon: Zap, status: 'idle' }
            ].map((node, i, arr) => {
              const NodeIcon = node.icon;
              return (
              <div key={node.id} className="relative group">
                {/* Connecting Line */}
                {i < arr.length - 1 && (
                  <div className="absolute top-1/2 left-full w-16 h-0.5 bg-zinc-800 -z-10">
                    <div className={`h-full bg-emerald-500/50 transition-all duration-1000 ${node.status === 'processing' ? 'w-full animate-pulse' : 'w-0'}`} />
                  </div>
                )}

                <div className={`
                  w-16 h-16 rounded-xl border-2 flex flex-col items-center justify-center gap-1 transition-all duration-300
                  ${node.status === 'processing' ? 'border-emerald-500 bg-emerald-500/10 shadow-[0_0_20px_rgba(16,185,129,0.3)] scale-110' :
                    node.status === 'waiting' ? 'border-amber-500/50 bg-amber-500/5' :
                    'border-zinc-800 bg-zinc-900'}
                `}>
                  <NodeIcon size={20} className={
                    node.status === 'processing' ? 'text-emerald-400' :
                    node.status === 'waiting' ? 'text-amber-400' : 'text-zinc-500'
                  } />
                </div>
                <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[10px] font-bold uppercase tracking-wider text-zinc-500 whitespace-nowrap">
                  {node.label}
                </div>
              </div>
            )})}
          </div>
        </div>
      </Card>
    </div>
  );
};

const ThreadsView = ({ threads, onApprove, onReject }) => {
  return (
    <Card title="Human-in-the-Loop Interventions" icon={GitBranch} className="h-full">
      <div className="flex flex-col gap-4 overflow-y-auto h-full pr-2">
        {threads.length === 0 && (
          <div className="flex items-center justify-center h-full text-zinc-500">
            <div className="text-center">
              <Bot size={48} className="mx-auto mb-4 opacity-50" />
              <p>No active threads</p>
            </div>
          </div>
        )}
        {threads.map(thread => (
          <div key={thread.id} className={`p-4 rounded-xl border transition-all ${thread.status === 'PAUSED' ? 'bg-amber-950/10 border-amber-500/30' : 'bg-zinc-900/50 border-white/5 opacity-70'}`}>
            <div className="flex justify-between items-start mb-3">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${thread.status === 'PAUSED' ? 'bg-amber-500/20 text-amber-400' : 'bg-zinc-800 text-zinc-500'}`}>
                  {thread.status === 'PAUSED' ? <ShieldAlert size={20} /> : <Activity size={20} />}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold text-white font-mono">{thread.id}</span>
                    <span className={`text-[10px] px-1.5 rounded border ${thread.status === 'PAUSED' ? 'border-amber-500/30 text-amber-400' : 'border-zinc-700 text-zinc-500'}`}>
                      {thread.status}
                    </span>
                  </div>
                  <div className="text-xs text-zinc-400 mt-0.5">
                    Agent: <span className="text-zinc-300">{thread.agent}</span> • Node: <span className="font-mono text-zinc-300">{thread.node}</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs text-zinc-500">{thread.created_at}</span>
                <RiskBadge score={thread.risk_score} />
              </div>
            </div>

            <div className="mb-4">
              <p className="text-sm text-zinc-200 mb-2">{thread.summary}</p>
              {thread.plan && (
                <div className="bg-black/40 rounded-lg p-3 font-mono text-xs text-emerald-400/90 border border-white/5">
                  <div className="text-zinc-500 mb-1">// Proposed Plan</div>
                  {JSON.stringify(thread.plan, null, 2)}
                </div>
              )}
            </div>

            {thread.status === 'PAUSED' && (
              <div className="flex gap-3 justify-end border-t border-white/5 pt-3">
                <button className="px-4 py-2 rounded-lg border border-white/10 hover:bg-white/5 text-xs font-bold text-zinc-300 uppercase tracking-wide transition-colors">
                  Investigate
                </button>
                <button
                  onClick={() => onReject(thread.id)}
                  className="px-4 py-2 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 text-xs font-bold uppercase tracking-wide transition-colors flex items-center gap-2"
                >
                  <XCircle size={14} /> Reject
                </button>
                <button
                  onClick={() => onApprove(thread.id)}
                  className="px-4 py-2 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/20 text-xs font-bold uppercase tracking-wide transition-colors flex items-center gap-2"
                >
                  <CheckCircle size={14} /> Approve & Resume
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </Card>
  );
};

const ProbesView = ({ probes }) => (
  <Card title="Probes & Health Monitors" icon={Radio} className="h-full">
    <div className="overflow-x-auto">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="border-b border-white/10 text-xs text-zinc-500 uppercase tracking-wider">
            <th className="p-4 font-medium">Probe ID</th>
            <th className="p-4 font-medium">Target</th>
            <th className="p-4 font-medium">Type</th>
            <th className="p-4 font-medium">Latency</th>
            <th className="p-4 font-medium">Last Check</th>
            <th className="p-4 font-medium text-right">Status</th>
          </tr>
        </thead>
        <tbody className="text-sm">
          {probes.length === 0 && (
            <tr>
              <td colSpan="6" className="p-8 text-center text-zinc-500">
                No probes configured
              </td>
            </tr>
          )}
          {probes.map(probe => (
            <tr key={probe.id} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
              <td className="p-4 font-mono text-zinc-400">{probe.id}</td>
              <td className="p-4 font-medium text-white">{probe.name}</td>
              <td className="p-4">
                <span className={`text-[10px] px-1.5 py-0.5 rounded border ${
                  probe.type === 'HTTP' ? 'border-blue-500/30 text-blue-400 bg-blue-500/5' : 'border-purple-500/30 text-purple-400 bg-purple-500/5'
                }`}>{probe.type}</span>
              </td>
              <td className="p-4 font-mono text-zinc-300">
                {probe.latency}ms
                {probe.latency > 500 && <span className="ml-2 text-amber-500 text-[10px]">⚠</span>}
              </td>
              <td className="p-4 text-zinc-500 text-xs">{probe.last_check}</td>
              <td className="p-4 text-right">
                <div className="flex justify-end">
                  <StatusIndicator status={probe.status} label="" />
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </Card>
);

const ConfigView = ({ policy, config }) => (
  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
    <Card title="Autopilot Policy (Read-Only)" icon={FileJson} className="lg:col-span-2 h-full">
      <div className="bg-black/50 rounded-lg p-4 font-mono text-xs text-zinc-300 h-full overflow-y-auto border border-white/5 leading-relaxed">
        <pre>{policy}</pre>
      </div>
    </Card>

    <div className="flex flex-col gap-6">
      <Card title="Configuration Flags" icon={Settings}>
        <div className="space-y-4">
          {config.map(flag => (
            <div key={flag.key} className="flex flex-col gap-1 pb-3 border-b border-white/5 last:border-0">
              <span className="text-[10px] text-zinc-500 font-bold uppercase">{flag.key}</span>
              <div className="flex items-center justify-between">
                <span className="text-sm font-mono text-white">{flag.value}</span>
                <span className="text-[10px] text-zinc-600 bg-zinc-900 px-1.5 rounded">{flag.type}</span>
              </div>
            </div>
          ))}
        </div>
      </Card>

      <Card className="bg-gradient-to-br from-emerald-900/10 to-transparent border-emerald-500/10">
        <div className="p-2">
          <h3 className="text-emerald-400 font-bold text-sm mb-1">Worker Status</h3>
          <p className="text-xs text-zinc-400 mb-3">Headless loop runner is healthy.</p>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-ping" />
            <span className="text-xs font-mono text-emerald-300">PID: {Math.floor(Math.random() * 9000) + 1000} (Running)</span>
          </div>
        </div>
      </Card>
    </div>
  </div>
);

// --- NET VIEW (CHAT INTERFACE) ---

const NetView = () => {
  const [messages, setMessages] = useState([
    { id: 1, role: 'ai', text: 'Matrix Guardian Neural Interface initialized. Secure uplink established. I am ready to assist with system diagnostics and remediation planning.' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const handleSendMessage = () => {
    if (!inputValue.trim()) return;

    const userMsg = { id: Date.now(), role: 'user', text: inputValue };
    setMessages(prev => [...prev, userMsg]);
    setInputValue('');
    setIsTyping(true);

    // Mock AI Response
    setTimeout(() => {
      setIsTyping(false);
      const responses = [
        "Analyzing system telemetry... All parameters within nominal ranges.",
        "I've detected a minor latency spike in the auth-gateway. Recommending a pod restart.",
        "Policy constraints prevent autonomous execution of that command. Please submit a HITL intervention request.",
        "Scanning recent logs for anomalies... No critical threats found.",
        "Connection stable. Database shards are synchronized."
      ];
      const randomResponse = responses[Math.floor(Math.random() * responses.length)];

      const aiMsg = {
        id: Date.now() + 1,
        role: 'ai',
        text: randomResponse
      };
      setMessages(prev => [...prev, aiMsg]);
    }, 1500);
  };

  return (
    <Card title="Neural Link // AI Assistant" icon={Network} className="h-full flex flex-col">
      <div className="flex-1 overflow-y-auto p-4 space-y-4" ref={scrollRef}>
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm ${
              msg.role === 'user'
                ? 'bg-emerald-600 text-white rounded-br-sm'
                : 'bg-zinc-800 text-zinc-200 border border-white/10 rounded-bl-sm'
            }`}>
              <div className="flex items-center gap-2 mb-1 opacity-60 text-[10px] font-bold uppercase tracking-wider">
                {msg.role === 'ai' ? <><Bot size={12} /> Guardian AI</> : 'Operator'}
              </div>
              <div className="leading-relaxed">{msg.text}</div>
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex justify-start">
             <div className="bg-zinc-800 px-4 py-3 rounded-2xl rounded-bl-sm border border-white/10 flex items-center gap-2">
                <Bot size={14} className="text-emerald-500 animate-bounce" />
                <span className="text-xs text-zinc-500 font-mono">Processing...</span>
             </div>
          </div>
        )}
      </div>

      <div className="p-4 bg-zinc-900/50 border-t border-white/5">
        <div className="relative">
          <input
            type="text"
            className="w-full bg-black border border-white/10 rounded-xl py-3 pl-4 pr-12 text-sm text-white placeholder-zinc-600 focus:outline-none focus:border-emerald-500/50 transition-colors"
            placeholder="Interrogate system state..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          <button
            onClick={handleSendMessage}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 bg-emerald-500/10 text-emerald-400 rounded-lg hover:bg-emerald-500/20 transition-colors"
          >
            <Zap size={16} />
          </button>
        </div>
        <div className="text-center mt-2 text-[10px] text-zinc-600 font-mono">
           ENCRYPTED UPLINK ESTABLISHED
        </div>
      </div>
    </Card>
  );
};

// --- MAIN APP ---

export default function App() {
  const [activeView, setActiveView] = useState('dashboard');
  const [autopilotStatus, setAutopilotStatus] = useState({
    enabled: false,
    safe_mode: true,
    interval_sec: 60,
    active_threads: 0,
    cycle_duration_ms: 0
  });
  const [systemStatus, setSystemStatus] = useState({
    service: 'matrix-guardian',
    version: 'v2.1.0',
    uptime: '0d 0h 0m',
    db_connection: 'UNKNOWN',
    hub_connection: 'UNKNOWN',
    ai_connection: 'UNKNOWN'
  });
  const [threads, setThreads] = useState([]);
  const [probes, setProbes] = useState([]);
  const [config, setConfig] = useState([]);
  const [policy, setPolicy] = useState('# Loading policy...');
  const [time, setTime] = useState(new Date());
  const [settingsOpen, setSettingsOpen] = useState(false);

  // Real-time clock
  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Fetch initial data
  useEffect(() => {
    fetchSystemStatus();
    fetchAutopilotStatus();
    fetchThreads();
    fetchProbes();
    fetchConfig();

    // Refresh data periodically
    const interval = setInterval(() => {
      fetchSystemStatus();
      fetchAutopilotStatus();
      fetchThreads();
      fetchProbes();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const fetchSystemStatus = async () => {
    try {
      const response = await guardianAPI.readyz();
      setSystemStatus(prev => ({
        ...prev,
        db_connection: response.data.database_connected ? 'CONNECTED' : 'DISCONNECTED'
      }));
    } catch (error) {
      console.error('Failed to fetch system status:', error);
    }
  };

  const fetchAutopilotStatus = async () => {
    try {
      const response = await guardianAPI.getAutopilotStatus();
      setAutopilotStatus(response.data);
    } catch (error) {
      console.error('Failed to fetch autopilot status:', error);
    }
  };

  const fetchThreads = async () => {
    try {
      const response = await guardianAPI.getThreads();
      setThreads(response.data.threads || []);
    } catch (error) {
      // Use mock data if API not available
      console.log('Using mock thread data');
    }
  };

  const fetchProbes = async () => {
    try {
      const response = await guardianAPI.getProbes();
      setProbes(response.data.probes || []);
    } catch (error) {
      // Use mock data if API not available
      console.log('Using mock probe data');
    }
  };

  const fetchConfig = async () => {
    try {
      const response = await guardianAPI.getConfig();
      setConfig(response.data.config || []);
      setPolicy(response.data.policy || '# Policy not available');
    } catch (error) {
      // Use mock data if API not available
      setConfig([
        { key: 'AUTOPILOT_ENABLED', value: 'false', type: 'bool' },
        { key: 'AUTOPILOT_SAFE_MODE', value: 'true', type: 'bool' },
        { key: 'AUTOPILOT_INTERVAL_SEC', value: '60', type: 'int' },
        { key: 'LOG_LEVEL', value: 'INFO', type: 'string' },
      ]);
      setPolicy(`# Guardian Autopilot Policy
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
`);
    }
  };

  const handleToggleAutopilot = async () => {
    // Note: This would need a backend endpoint to actually toggle autopilot
    setAutopilotStatus(prev => ({ ...prev, enabled: !prev.enabled }));
  };

  const handleApproveThread = async (threadId) => {
    try {
      await guardianAPI.resumeThread(threadId, 'approve', 'Approved via UI');
      fetchThreads(); // Refresh threads
    } catch (error) {
      console.error('Failed to approve thread:', error);
    }
  };

  const handleRejectThread = async (threadId) => {
    try {
      await guardianAPI.resumeThread(threadId, 'reject', 'Rejected via UI');
      fetchThreads(); // Refresh threads
    } catch (error) {
      console.error('Failed to reject thread:', error);
    }
  };

  const navItems = [
    { id: 'dashboard', label: 'Guardian Control', icon: ShieldCheck },
    { id: 'net', label: 'Neural Net', icon: Network },
    { id: 'threads', label: 'Interventions (HITL)', icon: GitBranch },
    { id: 'probes', label: 'Probes & Status', icon: Radio },
    { id: 'config', label: 'Policy Config', icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-black text-zinc-100 font-sans selection:bg-emerald-500/30 overflow-hidden flex">

      {/* Background Ambience */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500/0 via-emerald-500/50 to-emerald-500/0 opacity-50" />
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10"></div>
      </div>

      {/* Sidebar */}
      <aside className="w-64 bg-zinc-950/80 backdrop-blur-xl border-r border-white/5 z-20 flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-white/5">
          <ShieldCheck className="text-emerald-500 mr-3" size={24} />
          <div>
            <div className="font-bold text-white tracking-wider text-sm">MATRIX<span className="text-zinc-500">GUARDIAN</span></div>
            <div className="text-[10px] text-zinc-600 font-mono">ADMIN CONSOLE</div>
          </div>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveView(item.id)}
              className={`
                w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 group
                ${activeView === item.id
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                  : 'text-zinc-400 hover:bg-white/5 hover:text-white border border-transparent'}
              `}
            >
              <item.icon size={18} />
              {item.label}
              {activeView === item.id && (
                <div className="ml-auto w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_5px_currentColor]" />
              )}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-white/5">
          <button
            onClick={() => setSettingsOpen(true)}
            className="w-full flex items-center gap-3 px-3 py-2 mb-4 rounded-lg bg-zinc-900 border border-white/5 text-zinc-400 hover:text-white hover:border-white/10 transition-colors text-xs font-bold uppercase tracking-wider"
          >
            <Settings size={14} />
            Global Settings
          </button>

          <div className="text-[10px] font-bold text-zinc-500 uppercase mb-3">System Health</div>
          <div className="space-y-2">
            <StatusIndicator status={systemStatus.db_connection} label="Database" />
            <StatusIndicator status={systemStatus.hub_connection} label="Matrix Hub" />
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col h-screen relative z-10">
        <header className="h-16 flex items-center justify-between px-8 border-b border-white/5 bg-zinc-950/50 backdrop-blur-sm">
          <div className="flex items-center gap-4">
            <div className="text-xs font-mono text-zinc-500">
              <span className="text-emerald-500">●</span> {systemStatus.version}
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 font-mono text-sm text-zinc-400 bg-zinc-900 px-3 py-1 rounded border border-white/5">
              <Clock size={14} className="text-emerald-500" />
              <span>{time.toLocaleTimeString()} UTC</span>
            </div>
            <div className="w-8 h-8 rounded bg-zinc-800 flex items-center justify-center text-xs font-bold text-zinc-400 border border-white/5">
              OP
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-7xl mx-auto h-full">
            {activeView === 'dashboard' && (
              <DashboardView
                autopilotStatus={autopilotStatus}
                setAutopilotStatus={setAutopilotStatus}
                threads={threads}
                onToggleAutopilot={handleToggleAutopilot}
              />
            )}
            {activeView === 'net' && <NetView />}
            {activeView === 'threads' && (
              <ThreadsView
                threads={threads}
                onApprove={handleApproveThread}
                onReject={handleRejectThread}
              />
            )}
            {activeView === 'probes' && <ProbesView probes={probes} />}
            {activeView === 'config' && <ConfigView policy={policy} config={config} />}
          </div>
        </main>
      </div>

      <SettingsModal isOpen={settingsOpen} onClose={() => setSettingsOpen(false)} />
    </div>
  );
}
