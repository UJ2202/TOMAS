import axios from 'axios';
import { AgentMode, Mode } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth (future)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('tomas-auth-token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('tomas-auth-token');
    }
    return Promise.reject(error);
  }
);

// API Methods
export const modesApi = {
  list: () => api.get('/modes'),
  get: (modeId: string) => api.get(`/modes/${modeId}`),
  byCategory: (category: string) => api.get(`/modes/category/${category}`),
  byEngine: (engine: string) => api.get(`/modes/engine/${engine}`),
};

export const executionApi = {
  execute: (data: {
    mode_id: string;
    task: string;
    input_data: Record<string, any>;
  }) => api.post('/execute', data),
  
  stream: (data: {
    mode_id: string;
    task: string;
    input_data: Record<string, any>;
  }) => api.post('/execute/stream', data),
  
  status: (sessionId: string) => api.get(`/tasks/${sessionId}/status`),
  results: (sessionId: string) => api.get(`/tasks/${sessionId}/results`),
  messages: (sessionId: string) => api.get(`/tasks/${sessionId}/messages`),
  pause: (sessionId: string) => api.post(`/tasks/${sessionId}/pause`),
  resume: (sessionId: string) => api.post(`/tasks/${sessionId}/resume`),
  cancel: (sessionId: string) => api.post(`/tasks/${sessionId}/cancel`),
};

export const filesApi = {
  upload: (sessionId: string, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/files/${sessionId}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  list: (sessionId: string) => api.get(`/files/${sessionId}`),
  download: (sessionId: string, fileId: string) => 
    api.get(`/files/${sessionId}/${fileId}`, {
      responseType: 'blob',
    }),
  delete: (sessionId: string, fileId: string) =>
    api.delete(`/files/${sessionId}/${fileId}`),
};

// Legacy APIClient class for backward compatibility
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
