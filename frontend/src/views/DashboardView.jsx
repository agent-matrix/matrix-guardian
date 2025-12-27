import React from 'react';
import {
  AutopilotController,
  InterventionQueue,
  AgentDecisionGraph,
} from '../components/dashboard';

/**
 * DashboardView Component
 * Main dashboard view showing autopilot controls and system overview
 *
 * @param {Object} props
 * @param {Object} props.autopilotStatus - Current autopilot status
 * @param {Function} props.setAutopilotStatus - Function to update autopilot status
 * @param {Array} props.threads - Array of thread objects
 */
const DashboardView = ({ autopilotStatus, threads, setAutopilotStatus }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full auto-rows-min">
      {/* Autopilot Controller */}
      <AutopilotController
        autopilotStatus={autopilotStatus}
        setAutopilotStatus={setAutopilotStatus}
      />

      {/* HITL Stats */}
      <InterventionQueue threads={threads} />

      {/* Decision Graph Visualization (LangGraph Mock) */}
      <AgentDecisionGraph />
    </div>
  );
};

export default DashboardView;
