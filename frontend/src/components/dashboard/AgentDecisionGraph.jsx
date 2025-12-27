import React from 'react';
import { Workflow, Clock, Eye, Cpu, ShieldAlert, Zap } from 'lucide-react';
import Card from '../common/Card';
import { GRAPH_NODES } from '../../constants';

/**
 * AgentDecisionGraph Component
 * Visualizes the agent decision-making workflow as a graph
 */
const AgentDecisionGraph = () => {
  const iconMap = {
    Clock,
    Eye,
    Cpu,
    ShieldAlert,
    Zap,
  };

  return (
    <Card
      title="Agent Decision Graph"
      icon={Workflow}
      className="lg:col-span-3 min-h-[300px]"
    >
      <div className="relative w-full h-full min-h-[250px] bg-[#050505] rounded-lg border border-white/5 flex items-center justify-center overflow-hidden">
        {/* Background Grid */}
        <div
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: 'radial-gradient(#fff 1px, transparent 1px)',
            backgroundSize: '20px 20px',
          }}
        />

        {/* Graph Nodes */}
        <div className="flex items-center gap-16 relative z-10">
          {GRAPH_NODES.map((node, i, arr) => {
            const NodeIcon = iconMap[node.icon];
            return (
              <div key={node.id} className="relative group">
                {/* Connecting Line */}
                {i < arr.length - 1 && (
                  <div className="absolute top-1/2 left-full w-16 h-0.5 bg-zinc-800 -z-10">
                    <div
                      className={`h-full bg-emerald-500/50 transition-all duration-1000 ${
                        node.status === 'processing' ? 'w-full animate-pulse' : 'w-0'
                      }`}
                    />
                  </div>
                )}

                <div
                  className={`
                  w-16 h-16 rounded-xl border-2 flex flex-col items-center justify-center gap-1 transition-all duration-300
                  ${
                    node.status === 'processing'
                      ? 'border-emerald-500 bg-emerald-500/10 shadow-[0_0_20px_rgba(16,185,129,0.3)] scale-110'
                      : node.status === 'waiting'
                      ? 'border-amber-500/50 bg-amber-500/5'
                      : 'border-zinc-800 bg-zinc-900'
                  }
                `}
                >
                  <NodeIcon
                    size={20}
                    className={
                      node.status === 'processing'
                        ? 'text-emerald-400'
                        : node.status === 'waiting'
                        ? 'text-amber-400'
                        : 'text-zinc-500'
                    }
                  />
                </div>
                <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[10px] font-bold uppercase tracking-wider text-zinc-500 whitespace-nowrap">
                  {node.label}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </Card>
  );
};

export default AgentDecisionGraph;
