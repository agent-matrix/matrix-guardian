import React from 'react';
import { RISK_THRESHOLDS } from '../../constants';

/**
 * RiskBadge Component
 * Displays a risk score badge with color coding based on threshold
 *
 * @param {Object} props
 * @param {number} props.score - Risk score (0-100)
 */
const RiskBadge = ({ score }) => {
  let color = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
  if (score > RISK_THRESHOLDS.MEDIUM) {
    color = 'bg-amber-500/10 text-amber-400 border-amber-500/20';
  }
  if (score > RISK_THRESHOLDS.HIGH) {
    color = 'bg-rose-500/10 text-rose-400 border-rose-500/20';
  }

  return (
    <span
      className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${color}`}
    >
      RISK: {score}/100
    </span>
  );
};

export default RiskBadge;
