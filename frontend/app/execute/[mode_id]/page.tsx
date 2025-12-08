'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Mode, Session, SessionStatus } from '@/lib/types';
import { modesApi, executionApi } from '@/lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Badge } from '@/components/ui/Badge';
import { ThemeToggle } from '@/components/ThemeToggle';
import {
  ArrowLeft,
  Play,
  Loader2,
  Upload,
  Brain,
  Sparkles,
  X,
} from 'lucide-react';
import Link from 'next/link';
import toast from 'react-hot-toast';

export default function ExecutePage() {
  const params = useParams();
  const router = useRouter();
  const modeId = params.mode_id as string;

  const [mode, setMode] = useState<Mode | null>(null);
  const [loading, setLoading] = useState(true);
  const [executing, setExecuting] = useState(false);
  const [task, setTask] = useState('');
  const [inputData, setInputData] = useState<Record<string, any>>({});
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);

  useEffect(() => {
    loadMode();
  }, [modeId]);

  const loadMode = async () => {
    try {
      setLoading(true);
      const response = await modesApi.get(modeId);
      setMode(response.data);
      
      // Initialize input data with defaults
      const defaults: Record<string, any> = {};
      response.data.inputs?.forEach((input) => {
        if (input.default !== undefined) {
          defaults[input.name] = input.default;
        }
      });
      setInputData(defaults);
    } catch (err) {
      toast.error('Failed to load mode details');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setUploadedFiles((prev) => [...prev, ...Array.from(e.target.files!)]);
    }
  };

  const removeFile = (index: number) => {
    setUploadedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleInputChange = (name: string, value: any) => {
    setInputData((prev) => ({ ...prev, [name]: value }));
  };

  const handleExecute = async () => {
    if (!task.trim()) {
      toast.error('Please enter a task description');
      return;
    }

    try {
      setExecuting(true);
      const response = await executionApi.execute({
        mode_id: modeId,
        task: task.trim(),
        input_data: inputData,
      });

      toast.success('Task started successfully!');
      router.push(`/sessions/${response.data.session_id}`);
    } catch (err) {
      toast.error('Failed to start execution');
      console.error(err);
    } finally {
      setExecuting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!mode) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="pt-6">
            <p className="text-center text-muted-foreground">Mode not found</p>
            <Button asChild className="mt-4 mx-auto block">
              <Link href="/">Go Home</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" asChild>
                <Link href="/">
                  <ArrowLeft className="w-4 h-4" />
                </Link>
              </Button>
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary text-primary-foreground">
                  <Brain className="w-6 h-6" />
                </div>
                <div>
                  <h1 className="text-xl font-bold">{mode.name}</h1>
                  <p className="text-xs text-muted-foreground">
                    {mode.category} • {mode.engine}
                  </p>
                </div>
              </div>
            </div>
            <ThemeToggle />
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Mode Info */}
        <Card className="mb-6">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-primary" />
                  About This Mode
                </CardTitle>
                <CardDescription className="mt-2">
                  {mode.description}
                </CardDescription>
              </div>
              <Badge>{mode.engine}</Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              {mode.estimated_time && (
                <div>
                  <span className="font-medium">Estimated Time:</span>{' '}
                  <span className="text-muted-foreground">{mode.estimated_time}</span>
                </div>
              )}
              {mode.cost_estimate && (
                <div>
                  <span className="font-medium">Cost Estimate:</span>{' '}
                  <span className="text-muted-foreground">{mode.cost_estimate}</span>
                </div>
              )}
            </div>
            
            {mode.tags && mode.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-4">
                {mode.tags.map((tag) => (
                  <Badge key={tag} variant="secondary">
                    {tag}
                  </Badge>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Task Input */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Task Description</CardTitle>
            <CardDescription>
              Describe what you want the agent to accomplish
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Textarea
              placeholder="Enter your task description here..."
              value={task}
              onChange={(e) => setTask(e.target.value)}
              rows={6}
              className="resize-none"
            />
          </CardContent>
        </Card>

        {/* Dynamic Inputs */}
        {mode.inputs && mode.inputs.length > 0 && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Configuration</CardTitle>
              <CardDescription>
                Provide additional information for the task
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {mode.inputs.map((input) => (
                <div key={input.name} className="space-y-2">
                  <label className="text-sm font-medium flex items-center gap-2">
                    {input.label}
                    {input.required && <span className="text-destructive">*</span>}
                  </label>
                  {input.help_text && (
                    <p className="text-xs text-muted-foreground">{input.help_text}</p>
                  )}
                  
                  {input.type === 'text' && (
                    <Input
                      placeholder={input.placeholder}
                      value={inputData[input.name] || ''}
                      onChange={(e) => handleInputChange(input.name, e.target.value)}
                      required={input.required}
                    />
                  )}
                  
                  {input.type === 'textarea' && (
                    <Textarea
                      placeholder={input.placeholder}
                      value={inputData[input.name] || ''}
                      onChange={(e) => handleInputChange(input.name, e.target.value)}
                      required={input.required}
                      rows={3}
                    />
                  )}
                  
                  {input.type === 'select' && input.options && (
                    <select
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                      value={inputData[input.name] || ''}
                      onChange={(e) => handleInputChange(input.name, e.target.value)}
                      required={input.required}
                    >
                      <option value="">Select {input.label}</option>
                      {input.options.map((option) => (
                        <option key={option} value={option}>
                          {option}
                        </option>
                      ))}
                    </select>
                  )}
                  
                  {input.type === 'file' && (
                    <div className="space-y-2">
                      <Input
                        type="file"
                        accept={input.accept}
                        onChange={handleFileUpload}
                        className="cursor-pointer"
                      />
                      {uploadedFiles.length > 0 && (
                        <div className="space-y-1">
                          {uploadedFiles.map((file, index) => (
                            <div
                              key={index}
                              className="flex items-center justify-between p-2 bg-muted rounded-md"
                            >
                              <span className="text-sm truncate">{file.name}</span>
                              <Button
                                variant="ghost"
                                size="icon"
                                onClick={() => removeFile(index)}
                              >
                                <X className="w-4 h-4" />
                              </Button>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </CardContent>
          </Card>
        )}

        {/* Execute Button */}
        <Card>
          <CardContent className="pt-6">
            <Button
              onClick={handleExecute}
              disabled={executing || !task.trim()}
              size="lg"
              className="w-full"
              isLoading={executing}
            >
              <Play className="mr-2 w-4 h-4" />
              {executing ? 'Starting Execution...' : 'Start Execution'}
            </Button>
          </CardContent>
        </Card>

        {/* Tips */}
        {mode.tips && mode.tips.length > 0 && (
          <Card className="mt-6 border-info/50 bg-info/5">
            <CardHeader>
              <CardTitle className="text-sm">💡 Tips</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                {mode.tips.map((tip, index) => (
                  <li key={index} className="flex gap-2">
                    <span>•</span>
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
