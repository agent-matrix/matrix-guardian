import React from 'react';
import {
  ShieldCheck,
  GitBranch,
  Radio,
  Settings as SettingsIcon,
} from 'lucide-react';
import { NAV_ITEMS } from '../../constants';
import StatusIndicator from '../common/StatusIndicator';

/**
 * Sidebar Component
 * Main navigation sidebar with status indicators
 *
 * @param {Object} props
 * @param {string} props.activeView - Currently active view
 * @param {Function} props.setActiveView - Function to change active view
 * @param {Function} props.onSettingsClick - Handler for settings button click
 * @param {Object} props.status - System status object
 */
const Sidebar = ({ activeView, setActiveView, onSettingsClick, status }) => {
  const iconMap = {
    ShieldCheck,
    GitBranch,
    Radio,
    Settings: SettingsIcon,
  };

  return (
    <aside className="w-64 bg-zinc-950/80 backdrop-blur-xl border-r border-white/5 z-20 flex flex-col">
      <div className="h-16 flex items-center px-6 border-b border-white/5">
        <ShieldCheck className="text-emerald-500 mr-3" size={24} />
        <div>
          <div className="font-bold text-white tracking-wider text-sm">
            MATRIX<span className="text-zinc-500">GUARDIAN</span>
          </div>
          <div className="text-[10px] text-zinc-600 font-mono">ADMIN CONSOLE</div>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-1">
        {NAV_ITEMS.map((item) => {
          const Icon = iconMap[item.icon];
          return (
            <button
              key={item.id}
              onClick={() => setActiveView(item.id)}
              className={`
                w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 group
                ${
                  activeView === item.id
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    : 'text-zinc-400 hover:bg-white/5 hover:text-white border border-transparent'
                }
              `}
            >
              <Icon size={18} />
              {item.label}
              {activeView === item.id && (
                <div className="ml-auto w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_5px_currentColor]" />
              )}
            </button>
          );
        })}
      </nav>

      <div className="p-4 border-t border-white/5">
        <button
          onClick={onSettingsClick}
          className="w-full flex items-center gap-3 px-3 py-2 mb-4 rounded-lg bg-zinc-900 border border-white/5 text-zinc-400 hover:text-white hover:border-white/10 transition-colors text-xs font-bold uppercase tracking-wider"
        >
          <SettingsIcon size={14} />
          Global Settings
        </button>

        <div className="text-[10px] font-bold text-zinc-500 uppercase mb-3">System Health</div>
        <div className="space-y-2">
          <StatusIndicator status={status.db_connection} label="Database" />
          <StatusIndicator status={status.hub_connection} label="Matrix Hub" />
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
