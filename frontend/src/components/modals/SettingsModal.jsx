import React, { useState, useEffect } from 'react';
import { Settings, RefreshCw, Search, X } from 'lucide-react';
import { MOCK_SETTINGS, MOCK_MODELS } from '../../data/mockData';

/**
 * SettingsModal Component
 * Modal for configuring AI provider settings
 *
 * @param {Object} props
 * @param {boolean} props.isOpen - Whether modal is open
 * @param {Function} props.onClose - Handler to close modal
 */
const SettingsModal = ({ isOpen, onClose }) => {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('openai');
  const [models, setModels] = useState([]);
  const [loadingModels, setLoadingModels] = useState(false);
  const [saveStatus, setSaveStatus] = useState('');

  // Mock initial load
  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      setTimeout(() => {
        setSettings(MOCK_SETTINGS);
        setLoading(false);
      }, 500);
    }
  }, [isOpen]);

  const updateField = (section, field, value) => {
    setSettings((prev) => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value,
      },
    }));
  };

  const handleSave = () => {
    setSaveStatus('Saving...');
    setTimeout(() => {
      setSaveStatus('Settings Saved!');
      setTimeout(() => setSaveStatus(''), 2000);
    }, 800);
  };

  const loadProviderModels = (provider) => {
    setLoadingModels(true);
    setModels([]);
    // Mock API call
    setTimeout(() => {
      setModels(MOCK_MODELS[provider] || []);
      setLoadingModels(false);
    }, 1000);
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-[100] bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-2xl bg-zinc-900 border border-white/10 rounded-xl shadow-2xl overflow-hidden flex flex-col max-h-[80vh]"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between p-4 border-b border-white/10 bg-zinc-900/50">
          <div className="flex items-center gap-2">
            <Settings size={18} className="text-emerald-400" />
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">
              System Configuration
            </h2>
          </div>
          <button
            onClick={onClose}
            className="text-zinc-400 hover:text-white transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        <div className="flex flex-1 overflow-hidden">
          {loading ? (
            <div className="flex-1 flex items-center justify-center p-12 text-zinc-500 gap-2">
              <RefreshCw size={16} className="animate-spin" /> Loading settings...
            </div>
          ) : (
            <>
              <div className="w-48 border-r border-white/5 bg-black/20 p-2 space-y-1">
                {settings.providers.map((p) => (
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
                    {settings.provider === p && (
                      <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_5px_currentColor]" />
                    )}
                  </button>
                ))}
              </div>

              <div className="flex-1 p-6 overflow-y-auto">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-bold text-white capitalize">{activeTab} Settings</h3>
                  <button
                    onClick={() => setSettings((prev) => ({ ...prev, provider: activeTab }))}
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
                  {activeTab !== 'ollama' && (
                    <div>
                      <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-1.5">
                        API Key
                      </label>
                      <input
                        type="password"
                        value={settings[activeTab]?.api_key || ''}
                        onChange={(e) => updateField(activeTab, 'api_key', e.target.value)}
                        placeholder={`Enter ${activeTab} API key...`}
                        className="w-full bg-black border border-white/10 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                      />
                    </div>
                  )}

                  {activeTab === 'ollama' && (
                    <div>
                      <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-1.5">
                        Base URL
                      </label>
                      <input
                        type="text"
                        value={settings[activeTab]?.base_url || ''}
                        onChange={(e) => updateField(activeTab, 'base_url', e.target.value)}
                        placeholder="http://localhost:11434"
                        className="w-full bg-black border border-white/10 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                      />
                    </div>
                  )}

                  {activeTab === 'watsonx' && (
                    <div>
                      <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-1.5">
                        Project ID
                      </label>
                      <input
                        type="text"
                        value={settings[activeTab]?.project_id || ''}
                        onChange={(e) => updateField(activeTab, 'project_id', e.target.value)}
                        placeholder="Enter WatsonX project ID..."
                        className="w-full bg-black border border-white/10 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                      />
                    </div>
                  )}

                  <div>
                    <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-1.5">
                      Model Identifier
                    </label>
                    <div className="flex gap-2">
                      <input
                        type="text"
                        value={settings[activeTab]?.model || settings[activeTab]?.model_id || ''}
                        onChange={(e) =>
                          updateField(
                            activeTab,
                            activeTab === 'watsonx' ? 'model_id' : 'model',
                            e.target.value
                          )
                        }
                        className="flex-1 bg-black border border-white/10 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                      />
                      <button
                        onClick={() => loadProviderModels(activeTab)}
                        disabled={loadingModels}
                        className="px-3 bg-zinc-800 border border-white/10 rounded text-zinc-300 hover:text-white hover:bg-zinc-700 disabled:opacity-50"
                      >
                        {loadingModels ? (
                          <RefreshCw size={14} className="animate-spin" />
                        ) : (
                          <Search size={14} />
                        )}
                      </button>
                    </div>
                    {models.length > 0 && (
                      <select
                        className="w-full mt-2 bg-zinc-900 border border-white/10 rounded px-3 py-2 text-sm text-zinc-300 focus:outline-none"
                        onChange={(e) =>
                          updateField(
                            activeTab,
                            activeTab === 'watsonx' ? 'model_id' : 'model',
                            e.target.value
                          )
                        }
                      >
                        <option value="">Select a detected model...</option>
                        {models.map((m) => (
                          <option key={m} value={m}>
                            {m}
                          </option>
                        ))}
                      </select>
                    )}
                  </div>
                </div>
              </div>
            </>
          )}
        </div>

        <div className="p-4 border-t border-white/10 bg-zinc-900/50 flex justify-between items-center">
          <div className="text-emerald-400 text-xs font-bold uppercase tracking-wider">
            {saveStatus}
          </div>
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

export default SettingsModal;
