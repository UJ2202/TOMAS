'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { Session, Message, SessionStatus } from '@/lib/types';
import { executionApi } from '@/lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { ThemeToggle } from '@/components/ThemeToggle';
import { getStatusBadgeClass, formatDate, formatCost } from '@/lib/utils';
import {
  Brain,
  ArrowLeft,
  Loader2,
  Play,
  Pause,
  X,
  Download,
  MessageSquare,
  DollarSign,
  Clock,
} from 'lucide-react';
import toast from 'react-hot-toast';

export default function SessionDetailPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params.session_id as string;

  const [session, setSession] = useState<Session | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);
  const [polling, setPolling] = useState(false);

  useEffect(() => {
    loadSession();
    loadMessages();
  }, [sessionId]);

  useEffect(() => {
    // Poll for updates if session is running
    if (session?.status === SessionStatus.RUNNING || session?.status === SessionStatus.QUEUED) {
      const interval = setInterval(() => {
        loadSession();
        loadMessages();
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [session?.status]);

  const loadSession = async () => {
    try {
      const response = await executionApi.status(sessionId);
      setSession(response.data as any);
      setLoading(false);
    } catch (err) {
      toast.error('Failed to load session');
      console.error(err);
      setLoading(false);
    }
  };

  const loadMessages = async () => {
    try {
      const response = await executionApi.messages(sessionId);
      setMessages(response.data);
    } catch (err) {
      console.error('Failed to load messages:', err);
    }
  };

  const handlePause = async () => {
    try {
      await executionApi.pause(sessionId);
      toast.success('Execution paused');
      loadSession();
    } catch (err) {
      toast.error('Failed to pause execution');
    }
  };

  const handleResume = async () => {
    try {
      await executionApi.resume(sessionId);
      toast.success('Execution resumed');
      loadSession();
    } catch (err) {
      toast.error('Failed to resume execution');
    }
  };

  const handleCancel = async () => {
    if (!confirm('Are you sure you want to cancel this execution?')) return;
    
    try {
      await executionApi.cancel(sessionId);
      toast.success('Execution cancelled');
      loadSession();
    } catch (err) {
      toast.error('Failed to cancel execution');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!session) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="pt-6">
            <p className="text-center text-muted-foreground">Session not found</p>
            <Button asChild className="mt-4 mx-auto block">
              <Link href="/sessions">Back to Sessions</Link>
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
                <Link href="/sessions">
                  <ArrowLeft className="w-4 h-4" />
                </Link>
              </Button>
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary text-primary-foreground">
                  <Brain className="w-6 h-6" />
                </div>
                <div>
                  <h1 className="text-xl font-bold">Session Details</h1>
                  <p className="text-xs text-muted-foreground">{session.id}</p>
                </div>
              </div>
            </div>
            <ThemeToggle />
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Status and Controls */}
        <Card className="mb-6">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <CardTitle>Execution Status</CardTitle>
                  <Badge className={getStatusBadgeClass(session.status)}>
                    {session.status}
                  </Badge>
                </div>
                <CardDescription>Mode: {session.mode_id}</CardDescription>
              </div>
              <div className="flex gap-2">
                {session.status === SessionStatus.RUNNING && (
                  <>
                    <Button variant="outline" size="sm" onClick={handlePause}>
                      <Pause className="w-4 h-4 mr-2" />
                      Pause
                    </Button>
                    <Button variant="destructive" size="sm" onClick={handleCancel}>
                      <X className="w-4 h-4 mr-2" />
                      Cancel
                    </Button>
                  </>
                )}
                {session.status === SessionStatus.PAUSED && (
                  <>
                    <Button variant="outline" size="sm" onClick={handleResume}>
                      <Play className="w-4 h-4 mr-2" />
                      Resume
                    </Button>
                    <Button variant="destructive" size="sm" onClick={handleCancel}>
                      <X className="w-4 h-4 mr-2" />
                      Cancel
                    </Button>
                  </>
                )}
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4 text-sm">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Clock className="w-4 h-4" />
                <div>
                  <p className="font-medium text-foreground">Created</p>
                  <p>{formatDate(session.created_at)}</p>
                </div>
              </div>
              <div className="flex items-center gap-2 text-muted-foreground">
                <DollarSign className="w-4 h-4" />
                <div>
                  <p className="font-medium text-foreground">Total Cost</p>
                  <p>{formatCost(session.total_cost)}</p>
                </div>
              </div>
              <div className="flex items-center gap-2 text-muted-foreground">
                <MessageSquare className="w-4 h-4" />
                <div>
                  <p className="font-medium text-foreground">Tokens</p>
                  <p>{session.total_tokens.toLocaleString()}</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Messages */}
        <Card>
          <CardHeader>
            <CardTitle>Execution Log</CardTitle>
            <CardDescription>Real-time updates from the agent</CardDescription>
          </CardHeader>
          <CardContent>
            {messages.length === 0 ? (
              <p className="text-center text-muted-foreground py-8">
                No messages yet
              </p>
            ) : (
              <div className="space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className="p-4 rounded-lg border bg-card"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <Badge variant="outline">{message.role}</Badge>
                      <span className="text-xs text-muted-foreground">
                        {formatDate(message.created_at)}
                      </span>
                    </div>
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    {message.cost && (
                      <p className="text-xs text-muted-foreground mt-2">
                        Cost: {formatCost(message.cost)} • Tokens: {message.tokens}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
