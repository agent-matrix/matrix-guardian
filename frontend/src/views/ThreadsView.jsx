import React from 'react';
import { GitBranch } from 'lucide-react';
import Card from '../components/common/Card';
import { ThreadsList } from '../components/threads';

/**
 * ThreadsView Component
 * View for displaying and managing intervention threads
 *
 * @param {Object} props
 * @param {Array} props.threads - Array of thread objects
 */
const ThreadsView = ({ threads }) => {
  return (
    <Card title="Human-in-the-Loop Interventions" icon={GitBranch} className="h-full">
      <ThreadsList threads={threads} />
    </Card>
  );
};

export default ThreadsView;
