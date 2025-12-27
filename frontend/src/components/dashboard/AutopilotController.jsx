import React from 'react';
import { Bot, Play, Square } from 'lucide-react';
import { ShieldCheck } from 'lucide-react';
import Card from '../common/Card';

/**
 * AutopilotController Component
 * Main autopilot engagement control panel
 *
 * @param {Object} props
 * @param {Object} props.autopilotStatus - Current autopilot status
 * @param {Function} props.setAutopilotStatus - Function to update autopilot status
 */
const AutopilotController = ({ autopilotStatus, setAutopilotStatus }) => {
  return (
    <Card title="Autopilot Controller" icon={require('lucide-react').Cpu} className="lg:col-span-2">
      <div className="flex flex-col md:flex-row gap-6 items-center justify-between h-full">
        <div className="flex items-center gap-6">
          <div
            className={`w-24 h-24 rounded-full border-4 flex items-center justify-center relative ${
              autopilotStatus.enabled ? 'border-emerald-500/20' : 'border-zinc-800'
            }`}
          >
            {autopilotStatus.enabled && (
              <div className="absolute inset-0 rounded-full border-4 border-emerald-500 border-t-transparent animate-spin" />
            )}
            <Bot
              size={40}
              className={autopilotStatus.enabled ? 'text-emerald-400' : 'text-zinc-600'}
            />
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
                onClick={() =>
                  setAutopilotStatus((prev) => ({ ...prev, enabled: !prev.enabled }))
                }
                className={`px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider flex items-center gap-2 transition-all ${
                  autopilotStatus.enabled
                    ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20 hover:bg-rose-500/20'
                    : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 hover:bg-emerald-500/20'
                }`}
              >
                {autopilotStatus.enabled ? (
                  <Square size={14} fill="currentColor" />
                ) : (
                  <Play size={14} fill="currentColor" />
                )}
                {autopilotStatus.enabled ? 'Disengage' : 'Engage'}
              </button>
              <button
                onClick={() =>
                  setAutopilotStatus((prev) => ({ ...prev, safe_mode: !prev.safe_mode }))
                }
                className={`px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider flex items-center gap-2 border transition-all ${
                  autopilotStatus.safe_mode
                    ? 'bg-blue-500/10 text-blue-400 border-blue-500/20'
                    : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                }`}
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
            <div className="text-xl font-mono text-white">{autopilotStatus.active_threads}</div>
          </div>
          <div className="bg-zinc-900 p-3 rounded border border-white/5 text-center">
            <div className="text-[10px] text-zinc-500 uppercase font-bold">Cycle Time</div>
            <div className="text-xl font-mono text-emerald-400">
              {autopilotStatus.cycle_duration_ms}ms
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default AutopilotController;
