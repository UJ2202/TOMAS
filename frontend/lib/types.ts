// Core Types for TOMAS Frontend

export enum SessionStatus {
  CREATED = "created",
  QUEUED = "queued",
  RUNNING = "running",
  PAUSED = "paused",
  COMPLETED = "completed",
  FAILED = "failed",
  CANCELLED = "cancelled",
}

export enum EngineType {
  CMBAGENT = "cmbagent",
  DENARIO = "denario",
}

export enum MessageRole {
  SYSTEM = "system",
  USER = "user",
  ASSISTANT = "assistant",
  TOOL = "tool",
}

export interface Mode {
  id: string;
  name: string;
  description: string;
  category: string;
  icon: string;
  engine: EngineType;
  inputs: InputField[];
  outputs: OutputField[];
  tags: string[];
  estimated_time?: string;
  cost_estimate?: string;
  examples?: string[];
  tips?: string[];
}

export interface InputField {
  name: string;
  type: "text" | "textarea" | "file" | "select" | "number" | "boolean";
  label: string;
  required: boolean;
  default?: any;
  placeholder?: string;
  options?: string[];
  accept?: string;
  help_text?: string;
}

export interface OutputField {
  name: string;
  type: "text" | "file" | "plot" | "table" | "json";
  label: string;
  description?: string;
}

export interface Session {
  id: string;
  mode_id: string;
  status: SessionStatus;
  created_at: string;
  updated_at: string;
  input_data: Record<string, any>;
  output_data?: Record<string, any>;
  total_tokens: number;
  total_cost: number;
  error_message?: string;
  input_summary?: string;
}

export interface Message {
  id: string;
  session_id: string;
  role: MessageRole;
  content: string;
  created_at: string;
  metadata?: Record<string, any>;
  tokens?: number;
  cost?: number;
}

export interface SessionFile {
  id: string;
  session_id: string;
  filename: string;
  file_path: string;
  file_size: number;
  mime_type: string;
  is_input: boolean;
  uploaded_at: string;
}

export interface StreamEvent {
  type: "status" | "message" | "progress" | "cost" | "intervention_needed" | "artifact" | "error";
  data: any;
  timestamp: string;
}

export interface CostInfo {
  tokens: number;
  cost: number;
  model?: string;
}

export interface Artifact {
  type: "file" | "plot" | "data";
  name: string;
  path?: string;
  content?: any;
  metadata?: Record<string, any>;
}

// Legacy types for backward compatibility
export interface AgentMode extends Mode {}
export interface OutputType extends OutputField {}

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

