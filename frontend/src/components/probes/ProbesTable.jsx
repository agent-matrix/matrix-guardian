import React from 'react';
import StatusIndicator from '../common/StatusIndicator';

/**
 * ProbesTable Component
 * Displays health probes in a table format
 *
 * @param {Object} props
 * @param {Array} props.probes - Array of probe objects
 */
const ProbesTable = ({ probes }) => {
  return (
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
          {probes.map((probe) => (
            <tr
              key={probe.id}
              className="border-b border-white/5 hover:bg-white/[0.02] transition-colors"
            >
              <td className="p-4 font-mono text-zinc-400">{probe.id}</td>
              <td className="p-4 font-medium text-white">{probe.name}</td>
              <td className="p-4">
                <span
                  className={`text-[10px] px-1.5 py-0.5 rounded border ${
                    probe.type === 'HTTP'
                      ? 'border-blue-500/30 text-blue-400 bg-blue-500/5'
                      : 'border-purple-500/30 text-purple-400 bg-purple-500/5'
                  }`}
                >
                  {probe.type}
                </span>
              </td>
              <td className="p-4 font-mono text-zinc-300">
                {probe.latency}ms
                {probe.latency > 500 && (
                  <span className="ml-2 text-amber-500 text-[10px]">⚠</span>
                )}
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
  );
};

export default ProbesTable;
