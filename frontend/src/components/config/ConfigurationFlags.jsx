import React from 'react';
import { Settings } from 'lucide-react';
import Card from '../common/Card';

/**
 * ConfigurationFlags Component
 * Displays system configuration flags
 *
 * @param {Object} props
 * @param {Array} props.flags - Array of configuration flag objects
 */
const ConfigurationFlags = ({ flags }) => {
  return (
    <Card title="Configuration Flags" icon={Settings}>
      <div className="space-y-4">
        {flags.map((flag) => (
          <div
            key={flag.key}
            className="flex flex-col gap-1 pb-3 border-b border-white/5 last:border-0"
          >
            <span className="text-[10px] text-zinc-500 font-bold uppercase">{flag.key}</span>
            <div className="flex items-center justify-between">
              <span className="text-sm font-mono text-white">{flag.value}</span>
              <span className="text-[10px] text-zinc-600 bg-zinc-900 px-1.5 rounded">
                {flag.type}
              </span>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};

export default ConfigurationFlags;
