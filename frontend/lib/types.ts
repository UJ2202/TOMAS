// API client types
export interface AgentMode {
  id: string;
  name: string;
  description: string;
  category: string;
  icon: string;
  endpoint_path: string;
  inputs?: InputField[];
  outputs?: OutputType[];
}

export interface InputField {
  name: string;
  type: string;
  label: string;
  placeholder?: string;
  required: boolean;
  options?: string[];
  default?: any;
  help_text?: string;
}

export interface OutputType {
  name: string;
  type: string;
  format: string;
  description: string;
}

export interface TaskStatus {
  task_id: string;
  status: 'queued' | 'executing' | 'completed' | 'failed';
  progress: number;
  error?: string;
}

export interface TaskResult {
  task_id: string;
  result: any;
}

export interface ExecutionRequest {
  mode_id: string;
  input_data: Record<string, any>;
  files?: File[];
}
