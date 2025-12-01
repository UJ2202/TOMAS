'use client';

import { useState, useEffect } from 'react';
import { AgentMode } from '@/lib/types';
import { apiClient } from '@/lib/api';
import ModeSelector from '@/components/ModeSelector';
import ModeInterface from '@/components/ModeInterface';

export default function Home() {
  const [modes, setModes] = useState<AgentMode[]>([]);
  const [selectedMode, setSelectedMode] = useState<AgentMode | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadModes();
  }, []);

  const loadModes = async () => {
    try {
      setLoading(true);
      const data = await apiClient.listModes();
      setModes(data.modes);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load modes');
      console.error('Error loading modes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleModeSelect = async (mode: AgentMode) => {
    try {
      const details = await apiClient.getModeDetails(mode.id);
      setSelectedMode(details);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load mode details');
    }
  };

  const handleBack = () => {
    setSelectedMode(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-slate-900 mb-2">
            🤖 TOMAS
          </h1>
          <p className="text-xl text-slate-600">
            Task-Oriented Multi-Agent System
          </p>
        </header>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
            <p className="font-semibold">Error</p>
            <p>{error}</p>
            <button
              onClick={loadModes}
              className="mt-2 text-sm underline hover:no-underline"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Main Content */}
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : selectedMode ? (
          <ModeInterface mode={selectedMode} onBack={handleBack} />
        ) : (
          <ModeSelector modes={modes} onSelect={handleModeSelect} />
        )}

        {/* Footer */}
        <footer className="mt-12 text-center text-slate-500 text-sm">
          <p>
            Built with ❤️ using Denario, FastAPI, and Next.js
          </p>
        </footer>
      </div>
    </div>
  );
}
