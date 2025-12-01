# 🤖 Agent Platform

Multi-agent system with task-specific modes built on Denario.

## ✨ Features

- 🎯 **Multiple Agent Modes**: Research, RFP/SOW Analysis, ITOps Tickets, and more
- 🔄 **Dynamic UI**: Forms auto-generate based on mode configuration
- 🚀 **API-First**: Every mode can be called via REST API
- ⚡ **Powered by Denario**: Leverages CMBAgent and LangGraph
- 📦 **Easy to Extend**: Add new modes with simple configuration

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Copy environment template:**
```bash
cp .env.example .env
# Edit .env and add your API keys (OPENAI_API_KEY, etc.)
```

2. **Start services:**
```bash
docker-compose up
```

3. **Open browser:**
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/api/docs

### Manual Setup

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📚 Available Modes

### 1. 🔬 Research Mode
Generate research ideas, develop methodologies, execute experiments, and write scientific papers.

**Inputs:** Data description, tools
**Outputs:** Paper (PDF), plots, results, methodology

**API Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/research" \
  -H "X-API-Key: apk_your_key" \
  -F "data_description=Analyze gravitational wave data using Python" \
  -F "llm=gpt-4o"
```

### 2. 📄 RFP/SOW Intelligence
Analyze proposals and generate cloud architecture solutions with cost estimates.

**Inputs:** RFP document, cloud provider, budget
**Outputs:** Architecture design, diagrams, cost estimate, executive report

**API Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/rfp-analysis" \
  -H "X-API-Key: apk_your_key" \
  -F "rfp_document=@proposal.pdf" \
  -F "cloud_provider=AWS" \
  -F "budget_constraint=10000"
```

### 3. 🎫 ITOps Ticket Analysis
Analyze support tickets to identify patterns and root causes.

**Inputs:** Ticket data (CSV/JSON), analysis focus
**Outputs:** Patterns, root causes, visualizations, recommendations

**API Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/ticket-analysis" \
  -H "X-API-Key: apk_your_key" \
  -F "ticket_data=@tickets.csv" \
  -F "analysis_focus=Root Cause Analysis"
```

## 🛠️ Adding New Modes

Adding a new mode is simple:

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
