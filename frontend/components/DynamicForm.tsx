'use client';

import { useState } from 'react';
import { AgentMode, InputField } from '@/lib/types';
import { apiClient } from '@/lib/api';

interface DynamicFormProps {
  mode: AgentMode;
  onSubmit: (taskId: string) => void;
}

export default function DynamicForm({ mode, onSubmit }: DynamicFormProps) {
  const [formData, setFormData] = useState<Record<string, any>>({});
  const [files, setFiles] = useState<File[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (name: string, value: any) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);

    try {
      const response = await apiClient.executeMode(mode.id, formData, files);
      onSubmit(response.task_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit');
    } finally {
      setSubmitting(false);
    }
  };

  const renderField = (field: InputField) => {
    const commonClasses = 'w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500';

    switch (field.type) {
      case 'text':
      case 'number':
        return (
          <input
            type={field.type}
            name={field.name}
            placeholder={field.placeholder}
            required={field.required}
            defaultValue={field.default}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            className={commonClasses}
          />
        );

      case 'textarea':
        return (
          <textarea
            name={field.name}
            placeholder={field.placeholder}
            required={field.required}
            defaultValue={field.default}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            rows={6}
            className={commonClasses}
          />
        );

      case 'select':
        return (
          <select
            name={field.name}
            required={field.required}
            defaultValue={field.default}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            className={commonClasses}
          >
            {field.options?.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        );

      case 'file':
        return (
          <input
            type="file"
            name={field.name}
            required={field.required}
            onChange={handleFileChange}
            className={commonClasses}
          />
        );

      case 'checkbox':
        return (
          <input
            type="checkbox"
            name={field.name}
            required={field.required}
            defaultChecked={field.default}
            onChange={(e) => handleInputChange(field.name, e.target.checked)}
            className="w-5 h-5 text-blue-600"
          />
        );

      case 'multiselect':
        return (
          <select
            name={field.name}
            required={field.required}
            multiple
            onChange={(e) => {
              const values = Array.from(e.target.selectedOptions, (option) => option.value);
              handleInputChange(field.name, values);
            }}
            className={`${commonClasses} h-32`}
          >
            {field.options?.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        );

      default:
        return null;
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
        <p className="text-blue-900">{mode.description}</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          <p className="font-semibold">Error</p>
          <p>{error}</p>
        </div>
      )}

      {mode.inputs?.map((field) => (
        <div key={field.name} className="space-y-2">
          <label className="block text-sm font-medium text-slate-700">
            {field.label}
            {field.required && <span className="text-red-500 ml-1">*</span>}
          </label>
          {renderField(field)}
          {field.help_text && (
            <p className="text-sm text-slate-500">{field.help_text}</p>
          )}
        </div>
      ))}

      <button
        type="submit"
        disabled={submitting}
        className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold transition-colors"
      >
        {submitting ? 'Submitting...' : 'Execute Mode'}
      </button>
    </form>
  );
}
