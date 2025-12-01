# 🤖 TOMAS - Task-Oriented Multi-Agent System

Multi-agent platform with task-specific modes built on **Denario** (CMBAgent + LangGraph).

## ✨ Features

- 🎯 **Multiple Agent Modes**: Research, RFP/SOW Analysis, ITOps Tickets, and more
- 🔄 **Dynamic UI**: Forms auto-generate based on mode configuration
- 🚀 **API-First**: Every mode can be called via REST API
- ⚡ **Powered by Denario**: Leverages CMBAgent and LangGraph
- 📦 **Easy to Extend**: Add new modes with simple configuration

## 🏗️ Architecture

```
Frontend (Next.js) → FastAPI Gateway → Mode Executor → Denario → Results
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- Denario installed in parent directory (`../Denario`)

### Setup Environment

1. **Copy environment template:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Required API keys:
- `OPENAI_API_KEY` - Required for most modes
- `ANTHROPIC_API_KEY` - Optional, for Claude models
- `GOOGLE_API_KEY` - Optional, for Gemini models

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend
python main.py
```

Backend will run on `http://localhost:8000`
- API Docs: http://localhost:8000/api/docs

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:3000`

### Using Docker

```bash
# Start all services
docker-compose up

# Or start backend only
docker-compose up backend
```

## 📚 Available Modes

### 1. 🔬 Research Mode
Generate research ideas, develop methodologies, execute experiments, and write scientific papers.

**Inputs:** Data description, execution mode, LLM model
**Outputs:** Paper (PDF), plots, results, methodology

### 2. 📄 RFP/SOW Intelligence
Analyze proposals and generate cloud architecture solutions with cost estimates.

**Inputs:** RFP document, cloud provider, budget, compliance requirements
**Outputs:** Architecture design, diagrams, cost estimate, implementation plan

### 3. 🎫 ITOps Ticket Analysis
Analyze support tickets to identify patterns and root causes.

**Inputs:** Ticket data (CSV/JSON), analysis focus, time period
**Outputs:** Patterns, root causes, visualizations, recommendations

## 🛠️ Adding New Modes

### Step 1: Define Mode

Create `backend/modes/your_mode.py`:
```python
from core.mode import AgentMode, InputField, OutputType, InputFieldType
from core.mode_registry import registry

your_mode = AgentMode(
    id="your_mode",
    name="Your Mode Name",
    description="What this mode does",
    category="analysis",
    icon="Icon",  # Lucide icon name
    inputs=[...],
    outputs=[...],
    endpoint_path="/api/your-mode"
)

registry.register(your_mode)
```

### Step 2: Create Strategy

Create `backend/strategies/your_strategy.py`:
```python
def execute_your_mode(denario, input_data, mode_config):
    # Use Denario's workflow
    denario.set_data_description(...)
    denario.get_idea(...)
    denario.get_method(...)
    denario.get_results(...)
    denario.get_paper(...)
    
    return results

from core.mode_registry import registry
mode = registry.get("your_mode")
if mode:
    mode.strategy = execute_your_mode
```

### Step 3: Register

Edit `backend/modes/__init__.py`:
```python
from . import your_mode
from strategies import your_strategy
```

### Step 4: Restart
```bash
python main.py  # Mode appears automatically in UI!
```

## 📖 API Documentation

### List Modes
```bash
GET /api/modes
```

### Get Mode Details
```bash
GET /api/modes/{mode_id}
```

### Execute Mode
```bash
POST /api/execute
Content-Type: multipart/form-data

mode_id: research
input_data: {"data_description": "...", "llm": "gpt-4o"}
files: [file1, file2]
```

### Check Task Status
```bash
GET /api/tasks/{task_id}/status
```

### Get Results
```bash
GET /api/tasks/{task_id}/results
```

## 🔧 Development

### Backend Structure
```
backend/
├── core/              # Core abstractions
│   ├── mode.py       # AgentMode base class
│   ├── mode_registry.py
│   └── config.py
├── modes/            # Mode definitions
├── strategies/       # Execution strategies
├── services/         # Service layer
└── routers/          # API routes
```

### Frontend Structure
```
frontend/
├── app/              # Next.js App Router
│   ├── page.tsx     # Main page
│   └── layout.tsx
├── components/       # React components
│   ├── ModeSelector.tsx
│   ├── ModeInterface.tsx
│   ├── DynamicForm.tsx
│   ├── TaskMonitor.tsx
│   └── ResultsViewer.tsx
└── lib/             # Utilities
    ├── types.ts
    └── api.ts
```

## 🐛 Troubleshooting

### Denario Module Not Found
Ensure Denario is in the correct location:
```bash
ls ../Denario
```
Or adjust path in `backend/services/denario_service.py`

### API Keys Not Loading
Check `.env` file format (no spaces, no quotes):
```bash
OPENAI_API_KEY=sk-...
```

### Port Already in Use
```bash
# Change port in .env
PORT=8001

# Or kill process
lsof -ti:8000 | xargs kill -9
```

## 📝 Testing

### Test Backend
```bash
# List modes
curl http://localhost:8000/api/modes

# Execute research mode
curl -X POST "http://localhost:8000/api/execute" \
  -F "mode_id=research" \
  -F 'input_data={"data_description":"Test data","llm":"gpt-4o"}'
```

### Test Frontend
Open browser: http://localhost:3000

## 🚀 Deployment

### Production Build

Backend:
```bash
cd backend
pip install -r requirements.txt
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

Frontend:
```bash
cd frontend
npm run build
npm start
```

### Docker Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📄 License

See LICENSE file.

## 🤝 Contributing

This project uses:
- **Denario** - Multi-agent research system
- **FastAPI** - Modern Python web framework
- **Next.js** - React framework
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS

## 📚 Documentation

- [Implementation Plan](IMPLEMENTATION_PLAN.md) - Detailed implementation guide
- [Next Steps](NEXT_STEPS.md) - What to do next
- [Project Summary](PROJECT_SUMMARY.md) - Overview and architecture

---

**Built with ❤️ using Denario, FastAPI, and Next.js**

1. **Create mode definition** (`backend/modes/your_mode.py`):
```python
from core.mode import AgentMode, InputField, OutputType, InputFieldType
from core.mode_registry import registry

your_mode = AgentMode(
    id="your_mode",
    name="Your Mode Name",
    description="What it does",
    category="analysis",  # or research, generation, automation
    icon="IconName",  # Lucide icon
    inputs=[...],
    outputs=[...],
    endpoint_path="/api/your-mode"
)

registry.register(your_mode)
```

2. **Create execution strategy** (`backend/strategies/your_strategy.py`):
```python
def execute_your_mode(denario, input_data, mode_config):
    # Use Denario's workflow
    denario.set_data_description(...)
    denario.get_idea(...)
    # ... etc
    return results

# Attach to mode
mode = registry.get("your_mode")
mode.strategy = execute_your_mode
```

3. **Import in** `backend/modes/__init__.py`

4. **Restart backend** - UI updates automatically!

## 📁 Project Structure

```
agent-platform/
├── backend/              # FastAPI backend
│   ├── core/            # Core abstractions (Mode, Registry)
│   ├── modes/           # Mode definitions
│   ├── strategies/      # Execution strategies
│   ├── services/        # Services (Denario, Executor)
│   └── routers/         # API routes
├── frontend/            # Next.js frontend
│   ├── components/      # React components
│   └── lib/            # API client, types
├── IMPLEMENTATION_PLAN.md  # Detailed implementation guide
└── README.md           # This file
```

## 🔑 Environment Variables

Required in `.env`:

```bash
# LLM API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
GOOGLE_API_KEY=...

# Backend
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:3000

# Denario
DENARIO_WORKSPACE_DIR=./workspaces
```

## 🐳 Docker Configuration

The `docker-compose.yml` sets up:
- **Backend**: FastAPI on port 8000
- **Frontend**: Next.js on port 3000
- **Volumes**: Workspace persistence, Denario integration

## 📖 Documentation

- **[Implementation Plan](IMPLEMENTATION_PLAN.md)**: Detailed phase-by-phase guide
- **API Docs**: http://localhost:8000/api/docs (when running)
- **Mode Development**: See example modes in `backend/modes/`

## 🏗️ Architecture

The platform follows a clean architecture:

1. **Frontend** sends user inputs to backend
2. **Backend** routes request to appropriate mode
3. **Mode** uses its strategy to configure Denario
4. **Denario** (CMBAgent + LangGraph) executes the workflow
5. **Results** are returned to frontend for display

## 🤝 Contributing

This is an internal project. To contribute:

1. Add new modes following the pattern in `backend/modes/`
2. Test locally with `docker-compose up`
3. Update documentation

## 📄 License

MIT

## 🙏 Acknowledgments

Built with:
- [Denario](https://github.com/AstroPilot-AI/Denario) - Multi-agent research system
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework
- [shadcn/ui](https://ui.shadcn.com/) - UI components

---

**Questions?** See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for detailed setup guide.
