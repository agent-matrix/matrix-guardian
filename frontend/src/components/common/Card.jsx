import React from 'react';

/**
 * Card Component
 * Reusable card container with optional title, icon, and action
 *
 * @param {Object} props
 * @param {string} props.title - Card title
 * @param {React.Component} props.icon - Icon component (from lucide-react)
 * @param {React.ReactNode} props.children - Card content
 * @param {string} props.className - Additional CSS classes
 * @param {React.ReactNode} props.action - Action element (e.g., button) for the header
 */
const Card = ({ title, icon: Icon, children, className = '', action }) => (
  <div
    className={`bg-[#09090b] border border-white/10 rounded-xl overflow-hidden flex flex-col shadow-xl ${className}`}
  >
    {(title || Icon) && (
      <div className="px-4 py-3 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
        <div className="flex items-center gap-2">
          {Icon && <Icon size={16} className="text-emerald-500" />}
          <span className="text-xs font-bold text-zinc-300 uppercase tracking-widest">
            {title}
          </span>
        </div>
        {action}
      </div>
    )}
    <div className="p-4 flex-1 relative">{children}</div>
  </div>
);

export default Card;
