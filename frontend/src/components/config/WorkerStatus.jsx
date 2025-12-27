import React from 'react';
import Card from '../common/Card';

/**
 * WorkerStatus Component
 * Displays the status of the headless worker process
 */
const WorkerStatus = () => {
  return (
    <Card className="bg-gradient-to-br from-emerald-900/10 to-transparent border-emerald-500/10">
      <div className="p-2">
        <h3 className="text-emerald-400 font-bold text-sm mb-1">Worker Status</h3>
        <p className="text-xs text-zinc-400 mb-3">Headless loop runner is healthy.</p>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-emerald-500 rounded-full animate-ping" />
          <span className="text-xs font-mono text-emerald-300">PID: 4829 (Running)</span>
        </div>
      </div>
    </Card>
  );
};

export default WorkerStatus;
