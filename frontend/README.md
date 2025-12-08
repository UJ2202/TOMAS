# TOMAS Frontend

Modern, professional frontend for TOMAS (Task-Oriented Multi-Agent System) built with Next.js 14, React 18, and TailwindCSS.

## ✨ Features

- **🎨 Professional Theme System**: Light and dark mode support with beautiful color schemes
  - Very light blue theme for light mode
  - Very dark navy blue theme for dark mode
  - System theme detection
  - Persistent theme selection

- **⚡ Modern Tech Stack**:
  - Next.js 14 with App Router
  - TypeScript for type safety
  - TailwindCSS for styling
  - Framer Motion for animations
  - React Query for data fetching
  - Axios for API communication
  - Zustand for state management

- **🎯 Key Components**:
  - Mode selector with category filtering
  - Dynamic form generation based on mode inputs
  - Real-time execution monitoring
  - Session management and history
  - File upload and management
  - Cost tracking and display
  - Message/conversation history

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ installed
- Backend server running on `http://localhost:8000`

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`

### Build for Production

```bash
# Build the application
npm run build

# Start production server
npm start
```

## 📁 Project Structure

```
frontend/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout with theme provider
│   ├── page.tsx                 # Home page with mode selector
│   ├── globals.css              # Global styles and theme variables
│   ├── execute/
│   │   └── [mode_id]/
│   │       └── page.tsx         # Execution page
│   └── sessions/
│       ├── page.tsx             # Sessions list
│       └── [session_id]/
│           └── page.tsx         # Session detail page
│
├── components/
│   ├── ui/                      # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Badge.tsx
│   │   ├── Input.tsx
│   │   └── Textarea.tsx
│   └── ThemeToggle.tsx          # Theme switcher component
│
├── lib/
│   ├── api.ts                   # API client with axios
│   ├── types.ts                 # TypeScript type definitions
│   ├── utils.ts                 # Utility functions
│   └── theme-provider.tsx       # Theme context provider
│
├── public/                       # Static assets
├── tailwind.config.js           # TailwindCSS configuration
├── tsconfig.json                # TypeScript configuration
└── package.json                 # Dependencies and scripts
```

## 🎨 Theme System

### Color Scheme

**Light Mode** (Very Light Blue):
- Background: `hsl(210, 100%, 98%)` - Very light blue
- Primary: `hsl(210, 100%, 50%)` - Bright blue
- Cards: Pure white with subtle shadows

**Dark Mode** (Very Dark Navy Blue):
- Background: `hsl(222, 47%, 11%)` - Very dark navy
- Primary: `hsl(210, 100%, 56%)` - Bright blue
- Cards: Slightly lighter navy with subtle borders

### Using Theme Colors

```tsx
// In your components
<div className="bg-background text-foreground">
  <button className="bg-primary text-primary-foreground">
    Click me
  </button>
</div>
```

### Custom Theme Classes

```tsx
// Glass morphism
<div className="glass glass-hover">...</div>

// Gradient backgrounds
<div className="gradient-bg-light dark:gradient-bg-dark">...</div>

// Status badges
<Badge className="badge-success">Success</Badge>
<Badge className="badge-warning">Warning</Badge>
<Badge className="badge-error">Error</Badge>
```

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Feature Flags (optional)
NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

## 📦 Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint

# Type checking
npx tsc --noEmit     # Check TypeScript types
```

## 🎯 Key Pages

### Home (`/`)
- Landing page with feature highlights
- Mode grid with category filters
- Quick access to all available modes

### Execute (`/execute/[mode_id]`)
- Mode-specific execution interface
- Dynamic form generation based on mode inputs
- File upload support
- Real-time validation

### Sessions (`/sessions`)
- List of all user sessions
- Status indicators and filtering
- Quick access to session details

### Session Detail (`/sessions/[session_id]`)
- Real-time execution monitoring
- Message/log streaming
- Cost tracking
- Pause/Resume/Cancel controls

## 🎨 Component Library

### Button Component

```tsx
import { Button } from '@/components/ui/Button';

<Button variant="default">Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button isLoading>Loading...</Button>
```

### Card Component

```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>
    Content goes here
  </CardContent>
</Card>
```

### Badge Component

```tsx
import { Badge } from '@/components/ui/Badge';

<Badge variant="default">Default</Badge>
<Badge variant="success">Success</Badge>
<Badge variant="warning">Warning</Badge>
<Badge variant="error">Error</Badge>
```

## 🔌 API Integration

### Using the API Client

```tsx
import { modesApi, executionApi } from '@/lib/api';

// List all modes
const { data } = await modesApi.list();

// Execute a mode
const response = await executionApi.execute({
  mode_id: 'research',
  task: 'Analyze climate data',
  input_data: { dataset: 'climate.csv' }
});

// Get session status
const status = await executionApi.status(sessionId);
```

## 🎯 Best Practices

1. **Use TypeScript**: Leverage type safety for better development experience
2. **Component Composition**: Break down complex UIs into reusable components
3. **Theme Variables**: Use CSS variables for consistent theming
4. **Responsive Design**: Mobile-first approach with TailwindCSS
5. **Error Handling**: Use toast notifications for user feedback
6. **Loading States**: Always show loading indicators for async operations

## 🐛 Troubleshooting

### Theme Not Switching
- Check if `ThemeProvider` wraps the app in `layout.tsx`
- Verify `suppressHydrationWarning` is set on `<html>` tag

### API Errors
- Verify backend is running on correct port
- Check CORS configuration in backend
- Verify API endpoints in `lib/api.ts`

### Build Errors
- Clear `.next` folder: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check TypeScript errors: `npx tsc --noEmit`

## 📝 Contributing

When adding new features:

1. Follow existing component structure
2. Use TypeScript for all new code
3. Add proper type definitions
4. Use theme variables for colors
5. Ensure mobile responsiveness
6. Add loading and error states

## 📄 License

Same as parent TOMAS project.

---

**Built with ❤️ using Next.js and TailwindCSS**
