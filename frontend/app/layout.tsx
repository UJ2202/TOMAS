import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'TOMAS - Task-Oriented Multi-Agent System',
  description: 'Multi-agent platform with task-specific modes built on Denario',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
