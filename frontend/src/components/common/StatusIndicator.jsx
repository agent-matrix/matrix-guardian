import React from 'react';

/**
 * StatusIndicator Component
 * Displays a status indicator with a colored dot and label
 *
 * @param {Object} props
 * @param {string} props.status - Status value (CONNECTED, OK, DEGRADED, ERROR, etc.)
 * @param {string} props.label - Label text to display
 */
const StatusIndicator = ({ status, label }) => (
  <div className="flex items-center gap-2 bg-zinc-900/50 border border-white/5 px-3 py-1.5 rounded-lg">
    <div
      className={`w-2 h-2 rounded-full ${
        status === 'CONNECTED' || status === 'OK'
          ? 'bg-emerald-500 animate-pulse'
          : 'bg-rose-500'
      }`}
    />
    <div className="flex flex-col">
      <span className="text-[10px] text-zinc-500 uppercase font-bold tracking-wider">
        {label}
      </span>
      <span className="text-xs text-zinc-300 font-mono">{status}</span>
    </div>
  </div>
);

export default StatusIndicator;
