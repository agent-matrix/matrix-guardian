import React, { useState, useEffect } from 'react';
import { Sidebar, Header } from './components/layout';
import { SettingsModal } from './components/modals';
import { DashboardView, ThreadsView, ProbesView, ConfigView } from './views';
import { MOCK_STATUS, MOCK_THREADS, MOCK_PROBES, MOCK_POLICY_YAML } from './data/mockData';

/**
 * MATRIX GUARDIAN // CONTROL PLANE
 * Dedicated Admin Interface for the Matrix-Guardian Microservice
 *
 * Main application component that orchestrates the entire admin interface
 */
export default function App() {
  const [activeView, setActiveView] = useState('dashboard');
  const [autopilotStatus, setAutopilotStatus] = useState(MOCK_STATUS.autopilot);
  const [time, setTime] = useState(new Date());
  const [settingsOpen, setSettingsOpen] = useState(false);

  // Real-time clock
  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen bg-black text-zinc-100 font-sans selection:bg-emerald-500/30 overflow-hidden flex">
      {/* Background Ambience */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500/0 via-emerald-500/50 to-emerald-500/0 opacity-50" />
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10"></div>
      </div>

      {/* Sidebar */}
      <Sidebar
        activeView={activeView}
        setActiveView={setActiveView}
        onSettingsClick={() => setSettingsOpen(true)}
        status={MOCK_STATUS}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col h-screen relative z-10">
        <Header version={MOCK_STATUS.version} time={time} />

        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-7xl mx-auto h-full">
            {activeView === 'dashboard' && (
              <DashboardView
                autopilotStatus={autopilotStatus}
                setAutopilotStatus={setAutopilotStatus}
                threads={MOCK_THREADS}
              />
            )}
            {activeView === 'threads' && <ThreadsView threads={MOCK_THREADS} />}
            {activeView === 'probes' && <ProbesView probes={MOCK_PROBES} />}
            {activeView === 'config' && <ConfigView policy={MOCK_POLICY_YAML} />}
          </div>
        </main>
      </div>

      <SettingsModal isOpen={settingsOpen} onClose={() => setSettingsOpen(false)} />
    </div>
  );
}
