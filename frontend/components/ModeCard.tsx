'use client';

import { AgentMode } from '@/lib/types';
import { FlaskConical, FileText, Ticket } from 'lucide-react';

interface ModeCardProps {
  mode: AgentMode;
  onClick: () => void;
}

const iconMap: Record<string, any> = {
  FlaskConical,
  FileText,
  Ticket,
};

export default function ModeCard({ mode, onClick }: ModeCardProps) {
  const Icon = iconMap[mode.icon] || FlaskConical;

  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6 border border-slate-200 hover:border-blue-400"
    >
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0">
          <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <Icon className="w-6 h-6 text-blue-600" />
          </div>
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="text-lg font-semibold text-slate-900 mb-1">
            {mode.name}
          </h4>
          <p className="text-sm text-slate-600 line-clamp-2">
            {mode.description}
          </p>
        </div>
      </div>
    </button>
  );
}
