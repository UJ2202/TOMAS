'use client';

import { useState } from 'react';
import { AgentMode } from '@/lib/types';
import { ArrowLeft } from 'lucide-react';
import DynamicForm from './DynamicForm';
import TaskMonitor from './TaskMonitor';
import ResultsViewer from './ResultsViewer';

interface ModeInterfaceProps {
  mode: AgentMode;
  onBack: () => void;
}

type ViewState = 'form' | 'executing' | 'results';

export default function ModeInterface({ mode, onBack }: ModeInterfaceProps) {
  const [view, setView] = useState<ViewState>('form');
  const [taskId, setTaskId] = useState<string | null>(null);
  const [results, setResults] = useState<any>(null);

  const handleSubmit = (taskId: string) => {
    setTaskId(taskId);
    setView('executing');
  };

  const handleComplete = (results: any) => {
    setResults(results);
    setView('results');
  };

  const handleNewExecution = () => {
    setTaskId(null);
    setResults(null);
    setView('form');
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={onBack}
          className="flex items-center text-slate-600 hover:text-slate-900 transition-colors"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Modes
        </button>
        <h2 className="text-2xl font-bold text-slate-900">{mode.name}</h2>
        <div className="w-24"></div> {/* Spacer for alignment */}
      </div>

      {/* Content */}
      {view === 'form' && (
        <DynamicForm mode={mode} onSubmit={handleSubmit} />
      )}

      {view === 'executing' && taskId && (
        <TaskMonitor
          taskId={taskId}
          onComplete={handleComplete}
          onCancel={handleNewExecution}
        />
      )}

      {view === 'results' && results && (
        <ResultsViewer
          results={results}
          onNewExecution={handleNewExecution}
        />
      )}
    </div>
  );
}
