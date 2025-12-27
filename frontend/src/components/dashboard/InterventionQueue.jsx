import React from 'react';
import { AlertTriangle } from 'lucide-react';
import Card from '../common/Card';

/**
 * InterventionQueue Component
 * Displays pending human intervention statistics
 *
 * @param {Object} props
 * @param {Array} props.threads - Array of thread objects
 */
const InterventionQueue = ({ threads }) => {
  const pendingCount = threads.filter((t) => t.status === 'PAUSED').length;
  const lowRiskCount = threads.filter((t) => t.status === 'PAUSED' && t.risk_score <= 20).length;
  const mediumRiskCount = threads.filter(
    (t) => t.status === 'PAUSED' && t.risk_score > 20 && t.risk_score <= 80
  ).length;
  const highRiskCount = threads.filter((t) => t.status === 'PAUSED' && t.risk_score > 80).length;

  return (
    <Card title="Intervention Queue" icon={AlertTriangle} className="lg:col-span-1">
      <div className="flex flex-col h-full justify-center items-center">
        <div className="text-5xl font-mono font-bold text-amber-500 mb-2">{pendingCount}</div>
        <div className="text-xs text-zinc-500 uppercase tracking-widest font-bold">
          Pending Approvals
        </div>
        <div className="mt-6 w-full space-y-2">
          <div className="flex justify-between text-xs text-zinc-400">
            <span>Low Risk</span>
            <span className="text-white">{lowRiskCount}</span>
          </div>
          <div className="w-full h-1 bg-zinc-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-emerald-500"
              style={{ width: `${(lowRiskCount / Math.max(pendingCount, 1)) * 100}%` }}
            />
          </div>
          <div className="flex justify-between text-xs text-zinc-400">
            <span>Medium Risk</span>
            <span className="text-white">{mediumRiskCount}</span>
          </div>
          <div className="w-full h-1 bg-zinc-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-amber-500"
              style={{ width: `${(mediumRiskCount / Math.max(pendingCount, 1)) * 100}%` }}
            />
          </div>
          <div className="flex justify-between text-xs text-zinc-400">
            <span>High Risk</span>
            <span className="text-white">{highRiskCount}</span>
          </div>
          <div className="w-full h-1 bg-zinc-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-rose-500"
              style={{ width: `${(highRiskCount / Math.max(pendingCount, 1)) * 100}%` }}
            />
          </div>
        </div>
      </div>
    </Card>
  );
};

export default InterventionQueue;
