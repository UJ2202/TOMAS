'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api';
import { TaskStatus } from '@/lib/types';
import { Loader2, XCircle } from 'lucide-react';

interface TaskMonitorProps {
  taskId: string;
  onComplete: (results: any) => void;
  onCancel: () => void;
}

export default function TaskMonitor({ taskId, onComplete, onCancel }: TaskMonitorProps) {
  const [status, setStatus] = useState<TaskStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const pollStatus = setInterval(async () => {
      try {
        const taskStatus = await apiClient.getTaskStatus(taskId);
        setStatus(taskStatus);

        if (taskStatus.status === 'completed') {
          clearInterval(pollStatus);
          const results = await apiClient.getTaskResults(taskId);
          onComplete(results.result);
        } else if (taskStatus.status === 'failed') {
          clearInterval(pollStatus);
          setError(taskStatus.error || 'Task failed');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch status');
        clearInterval(pollStatus);
      }
    }, 2000); // Poll every 2 seconds

    return () => clearInterval(pollStatus);
  }, [taskId, onComplete]);

  if (error) {
    return (
      <div className="text-center py-12">
        <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-slate-900 mb-2">Task Failed</h3>
        <p className="text-slate-600 mb-4">{error}</p>
        <button
          onClick={onCancel}
          className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="text-center py-12">
      <Loader2 className="w-16 h-16 text-blue-600 mx-auto mb-4 animate-spin" />
      <h3 className="text-xl font-semibold text-slate-900 mb-2">
        {status?.status === 'queued' ? 'Queued' : 'Executing'}
      </h3>
      <p className="text-slate-600 mb-4">
        Your task is being processed. This may take a few minutes...
      </p>
      <div className="max-w-md mx-auto">
        <div className="bg-slate-200 rounded-full h-2 mb-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${status?.progress || 0}%` }}
          />
        </div>
        <p className="text-sm text-slate-500">{status?.progress || 0}% complete</p>
      </div>
      <button
        onClick={onCancel}
        className="mt-6 text-slate-600 hover:text-slate-900 underline"
      >
        Cancel
      </button>
    </div>
  );
}
