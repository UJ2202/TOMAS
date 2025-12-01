'use client';

import { AgentMode } from '@/lib/types';
import ModeCard from './ModeCard';

interface ModeSelectorProps {
  modes: AgentMode[];
  onSelect: (mode: AgentMode) => void;
}

export default function ModeSelector({ modes, onSelect }: ModeSelectorProps) {
  const categories = Array.from(new Set(modes.map((m) => m.category)));

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-2xl font-semibold text-slate-800 mb-2">
          Select an Agent Mode
        </h2>
        <p className="text-slate-600">
          Choose a task-specific mode to get started
        </p>
      </div>

      {categories.map((category) => {
        const categoryModes = modes.filter((m) => m.category === category);
        
        return (
          <div key={category}>
            <h3 className="text-lg font-semibold text-slate-700 mb-4 capitalize">
              {category}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {categoryModes.map((mode) => (
                <ModeCard
                  key={mode.id}
                  mode={mode}
                  onClick={() => onSelect(mode)}
                />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
