import { AgentMode, TaskStatus, TaskResult } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class APIClient {
  private baseURL: string;

  constructor(baseURL: string = API_URL) {
    this.baseURL = baseURL;
  }

  async listModes(): Promise<{ modes: AgentMode[]; count: number }> {
    const response = await fetch(`${this.baseURL}/api/modes`);
    if (!response.ok) {
      throw new Error('Failed to fetch modes');
    }
    return response.json();
  }

  async getModeDetails(modeId: string): Promise<AgentMode> {
    const response = await fetch(`${this.baseURL}/api/modes/${modeId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch mode ${modeId}`);
    }
    return response.json();
  }

  async executeMode(
    modeId: string,
    inputData: Record<string, any>,
    files?: File[]
  ): Promise<{ task_id: string; session_id: string; status: string }> {
    const formData = new FormData();
    formData.append('mode_id', modeId);
    formData.append('input_data', JSON.stringify(inputData));

    if (files) {
      files.forEach((file) => {
        formData.append('files', file);
      });
    }

    const response = await fetch(`${this.baseURL}/api/execute`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to execute mode');
    }

    return response.json();
  }

  async getTaskStatus(taskId: string): Promise<TaskStatus> {
    const response = await fetch(`${this.baseURL}/api/tasks/${taskId}/status`);
    if (!response.ok) {
      throw new Error('Failed to fetch task status');
    }
    return response.json();
  }

  async getTaskResults(taskId: string): Promise<TaskResult> {
    const response = await fetch(`${this.baseURL}/api/tasks/${taskId}/results`);
    if (!response.ok) {
      throw new Error('Failed to fetch task results');
    }
    return response.json();
  }

  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseURL}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  }
}

export const apiClient = new APIClient();
