import React from 'react';
import { FileJson } from 'lucide-react';
import Card from '../common/Card';

/**
 * PolicyViewer Component
 * Displays the autopilot policy YAML in a read-only format
 *
 * @param {Object} props
 * @param {string} props.policy - Policy YAML string
 */
const PolicyViewer = ({ policy }) => {
  return (
    <Card
      title="Autopilot Policy (Read-Only)"
      icon={FileJson}
      className="lg:col-span-2 h-full"
    >
      <div className="bg-black/50 rounded-lg p-4 font-mono text-xs text-zinc-300 h-full overflow-y-auto border border-white/5 leading-relaxed">
        <pre>{policy}</pre>
      </div>
    </Card>
  );
};

export default PolicyViewer;
