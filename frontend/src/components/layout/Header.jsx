import React from 'react';
import { Clock } from 'lucide-react';

/**
 * Header Component
 * Top header bar with version info and clock
 *
 * @param {Object} props
 * @param {string} props.version - Application version
 * @param {Date} props.time - Current time
 */
const Header = ({ version, time }) => {
  return (
    <header className="h-16 flex items-center justify-between px-8 border-b border-white/5 bg-zinc-950/50 backdrop-blur-sm">
      <div className="flex items-center gap-4">
        <div className="text-xs font-mono text-zinc-500">
          <span className="text-emerald-500">●</span> {version}
        </div>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 font-mono text-sm text-zinc-400 bg-zinc-900 px-3 py-1 rounded border border-white/5">
          <Clock size={14} className="text-emerald-500" />
          <span>{time.toLocaleTimeString()} UTC</span>
        </div>
        <div className="w-8 h-8 rounded bg-zinc-800 flex items-center justify-center text-xs font-bold text-zinc-400 border border-white/5">
          RM
        </div>
      </div>
    </header>
  );
};

export default Header;
