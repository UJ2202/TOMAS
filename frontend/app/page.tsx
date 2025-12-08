'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Mode } from '@/lib/types';
import { modesApi } from '@/lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { ThemeToggle } from '@/components/ThemeToggle';
import {
  Sparkles,
  Zap,
  Shield,
  ArrowRight,
  Loader2,
  FileText,
  FlaskConical,
  Ticket,
  Brain,
  Network,
  Rocket,
} from 'lucide-react';

const iconMap: Record<string, any> = {
  '🔬': FlaskConical,
  '📄': FileText,
  '🎫': Ticket,
  '📚': FileText,
  '⚙️': Network,
  '📊': Network,
};

export default function Home() {
  const [modes, setModes] = useState<Mode[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadModes();
  }, []);

  const loadModes = async () => {
    try {
      setLoading(true);
      const response = await modesApi.list();
      setModes(response.data.modes);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load modes');
      console.error('Error loading modes:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary text-primary-foreground">
                <Brain className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">TOMAS</h1>
                <p className="text-xs text-muted-foreground">Task-Oriented Multi-Agent System</p>
              </div>
            </div>
            <ThemeToggle />
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-6xl text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary mb-6 animate-fade-in">
            <Sparkles className="w-4 h-4" />
            <span className="text-sm font-medium">Powered by CMBAgent & Denario</span>
          </div>
          
          <h2 className="text-5xl md:text-6xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-primary via-primary-600 to-accent">
            Intelligent Multi-Agent Platform
          </h2>
          
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Execute complex tasks with specialized AI agents. From scientific research to document analysis,
            TOMAS delivers professional results with cutting-edge AI technology.
          </p>

          <div className="flex flex-wrap gap-4 justify-center">
            <Button size="lg" asChild>
              <Link href="#modes">
                Get Started
                <ArrowRight className="ml-2 w-4 h-4" />
              </Link>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <Link href="/sessions">
                View Sessions
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 px-4 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="glass glass-hover">
              <CardHeader>
                <Zap className="w-10 h-10 text-primary mb-2" />
                <CardTitle>Dual Engine Power</CardTitle>
                <CardDescription>
                  CMBAgent for complex planning and Denario for scientific research
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="glass glass-hover">
              <CardHeader>
                <Shield className="w-10 h-10 text-primary mb-2" />
                <CardTitle>Production Ready</CardTitle>
                <CardDescription>
                  Robust session management, cost tracking, and error handling
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="glass glass-hover">
              <CardHeader>
                <Rocket className="w-10 h-10 text-primary mb-2" />
                <CardTitle>Real-time Streaming</CardTitle>
                <CardDescription>
                  Watch your agents work in real-time with live progress updates
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Modes Section */}
      <section id="modes" className="py-20 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold mb-4">Available Modes</h3>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Choose from specialized agent modes designed for specific tasks and industries
            </p>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-20">
              <Loader2 className="w-8 h-8 animate-spin text-primary" />
            </div>
          ) : error ? (
            <Card className="border-destructive">
              <CardContent className="pt-6">
                <p className="text-destructive text-center">{error}</p>
                <Button onClick={loadModes} className="mt-4 mx-auto block">
                  Retry
                </Button>
              </CardContent>
            </Card>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {modes.map((mode) => {
                const IconComponent = iconMap[mode.icon] || FileText;
                return (
                  <Card key={mode.id} className="card-hover group">
                    <CardHeader>
                      <div className="flex items-start justify-between mb-3">
                        <div className="p-3 rounded-lg bg-primary/10 text-primary group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                          <IconComponent className="w-6 h-6" />
                        </div>
                        <Badge variant="outline">{mode.engine}</Badge>
                      </div>
                      <CardTitle className="text-xl">{mode.name}</CardTitle>
                      <CardDescription className="line-clamp-2">
                        {mode.description}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex flex-wrap gap-2 mb-4">
                        {mode.tags?.slice(0, 3).map((tag) => (
                          <Badge key={tag} variant="secondary" className="text-xs">
                            {tag}
                          </Badge>
                        ))}
                      </div>
                      <Button asChild className="w-full">
                        <Link href={`/execute/${mode.id}`}>
                          Start Task
                          <ArrowRight className="ml-2 w-4 h-4" />
                        </Link>
                      </Button>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8 px-4 bg-card/50">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm text-muted-foreground">
              © 2024 TOMAS. Advanced Multi-Agent System.
            </p>
            <div className="flex gap-4">
              <Link href="/docs" className="text-sm text-muted-foreground hover:text-foreground">
                Documentation
              </Link>
              <Link href="/api" className="text-sm text-muted-foreground hover:text-foreground">
                API
              </Link>
              <Link href="/about" className="text-sm text-muted-foreground hover:text-foreground">
                About
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
