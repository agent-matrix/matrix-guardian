import React from 'react';
import { ShieldAlert, Activity, CheckCircle, XCircle } from 'lucide-react';
import RiskBadge from '../common/RiskBadge';

/**
 * ThreadCard Component
 * Displays a single thread with its details and action buttons
 *
 * @param {Object} props
 * @param {Object} props.thread - Thread object containing id, status, agent, etc.
 */
const ThreadCard = ({ thread }) => {
  return (
    <div
      className={`p-4 rounded-xl border transition-all ${
        thread.status === 'PAUSED'
          ? 'bg-amber-950/10 border-amber-500/30'
          : 'bg-zinc-900/50 border-white/5 opacity-70'
      }`}
    >
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center gap-3">
          <div
            className={`p-2 rounded-lg ${
              thread.status === 'PAUSED'
                ? 'bg-amber-500/20 text-amber-400'
                : 'bg-zinc-800 text-zinc-500'
            }`}
          >
            {thread.status === 'PAUSED' ? <ShieldAlert size={20} /> : <Activity size={20} />}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold text-white font-mono">{thread.id}</span>
              <span
                className={`text-[10px] px-1.5 rounded border ${
                  thread.status === 'PAUSED'
                    ? 'border-amber-500/30 text-amber-400'
                    : 'border-zinc-700 text-zinc-500'
                }`}
              >
                {thread.status}
              </span>
            </div>
            <div className="text-xs text-zinc-400 mt-0.5">
              Agent: <span className="text-zinc-300">{thread.agent}</span> • Node:{' '}
              <span className="font-mono text-zinc-300">{thread.node}</span>
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
          <button className="px-4 py-2 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 text-xs font-bold uppercase tracking-wide transition-colors flex items-center gap-2">
            <XCircle size={14} /> Reject
          </button>
          <button className="px-4 py-2 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/20 text-xs font-bold uppercase tracking-wide transition-colors flex items-center gap-2">
            <CheckCircle size={14} /> Approve & Resume
          </button>
        </div>
      )}
    </div>
  );
};

export default ThreadCard;
