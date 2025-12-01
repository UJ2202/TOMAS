# Agent Platform - Detailed Phase-wise Implementation Plan

## 🎯 Project Vision

Create a multi-agent platform with different **Agent Modes** where:
- Each mode has specific input context requirements
- Each mode produces specific output types
- Denario backend (with CMBAgent + LangGraph) handles execution
- Modes can be exposed as API endpoints for end-to-end task completion
- UI dynamically adapts based on selected mode

---

## 📋 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                        │
│  ┌─────────────────┐         ┌─────────────────────────┐   │
│  │ Mode Selector   │  ────>  │  Mode Interface         │   │
│  │ - Grid of cards │         │  - Dynamic input forms  │   │
│  └─────────────────┘         │  - Real-time results    │   │
│                               │  - Download outputs     │   │
│                               └─────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓ REST API
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI Gateway)                   │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  Mode Registry   │  │  Mode Executor   │                │
│  │  - Research      │  │  - Task Queue    │                │
│  │  - RFP/SOW       │  │  - Status Track  │                │
│  │  - ITOps         │  │  - Results Store │                │
│  │  - Handbook      │  └──────────────────┘                │
│  │  - DevOps        │                                       │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Denario Core Engine                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │
│  │  CMBAgent   │  │  LangGraph  │  │  Multi-Agent    │    │
│  │  Planning & │  │  Fast       │  │  Orchestration  │    │
│  │  Control    │  │  Workflows  │  │  & Handoffs     │    │
│  └─────────────┘  └─────────────┘  └─────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 What is an "Agent Mode"?

An **Agent Mode** is a task-specific configuration that defines:

1. **Input Schema** - What context/data does the user provide?
2. **Output Types** - What results does the mode produce?
3. **Execution Strategy** - How does this mode use Denario's workflow?
4. **API Endpoint** - RESTful endpoint path for future use

---

## 📦 Example Modes

| Mode ID | Name | Inputs | Outputs |
|---------|------|--------|---------|
| `research` | Scientific Research | Data description, tools | Paper (PDF), plots, results |
| `rfp_sow` | RFP/SOW Intelligence | RFP doc, cloud provider | Architecture, diagrams, costs |
| `itops` | ITOps Ticket Analysis | Ticket CSV, focus area | Insights, dashboard, recommendations |
| `handbook` | Technical Handbook | Topic, audience, tech stack | Handbook (PDF/HTML), code examples |
| `devops` | DevOps Mining | Repo URL, analysis type | Security report, docs, CI/CD |

---

## 📊 Implementation Timeline

| Phase | Duration | Focus |
|-------|----------|-------|
| Phase 1 | Day 1 | Project Setup |
| Phase 2 | Days 2-4 | Backend Mode System |
| Phase 3 | Days 5-7 | Frontend Dynamic UI |
| Phase 4 | Days 8-12 | First Three Modes |
| Phase 5 | Days 13-14 | API Endpoints |
| Phase 6 | Days 15-17 | Production Ready |

---

# PHASE 1: Project Setup (Day 1)

## Goals
✅ Create project structure
✅ Setup development environment
✅ Initialize Git repository
✅ Configure environment variables
✅ Test basic connectivity

## Directory Structure Created

```
agent-platform/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── core/
│   │   ├── __init__.py
│   │   ├── mode.py
│   │   ├── mode_registry.py
│   │   └── config.py
│   ├── modes/
│   │   ├── __init__.py
│   │   ├── research.py
│   │   ├── rfp_sow.py
│   │   └── itops.py
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── research_strategy.py
│   │   ├── rfp_strategy.py
│   │   └── itops_strategy.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── denario_service.py
│   │   └── mode_executor.py
│   └── routers/
│       ├── __init__.py
│       ├── modes.py
│       └── execution.py
├── frontend/
│   ├── (Next.js structure)
├── .env.example
├── .gitignore
├── docker-compose.yml
├── IMPLEMENTATION_PLAN.md
└── README.md
```

---

# PHASE 2: Backend Mode System (Days 2-4)

## Key Concepts

### 1. Mode Base Class
Defines structure of every agent mode with inputs, outputs, and execution strategy.

### 2. Mode Registry
Central registry where all modes are registered and can be queried.

### 3. Denario Service
Wrapper around Denario that manages sessions and instances.

### 4. Mode Executor
Executes modes asynchronously using their registered strategies.

## Implementation Files

See individual files in `backend/` directory for complete implementations.

---

# PHASE 3: Frontend Dynamic UI (Days 5-7)

## Components

1. **ModeSelector** - Grid of mode cards
2. **ModeCard** - Individual mode display
3. **ModeInterface** - Main execution interface
4. **DynamicForm** - Auto-generates forms from mode inputs
5. **TaskMonitor** - Real-time status updates
6. **ResultsViewer** - Display outputs

---

# PHASE 4: First Three Modes (Days 8-12)

## Mode 1: Research
Uses Denario exactly as designed for scientific research.

## Mode 2: RFP/SOW Intelligence
Parses RFP documents and generates cloud architectures.

## Mode 3: ITOps Ticket Analysis
Analyzes support tickets and identifies patterns.

---

# PHASE 5: API Endpoints (Days 13-14)

Each mode gets standalone API endpoint:
- `POST /api/v1/research`
- `POST /api/v1/rfp-analysis`
- `POST /api/v1/ticket-analysis`

---

# PHASE 6: Production Ready (Days 15-17)

- Docker containerization
- Environment configuration
- Error handling & logging
- Documentation

---

# 🚀 Getting Started

## Quick Start

1. **Copy environment variables:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

2. **Start with Docker:**
```bash
docker-compose up
```

3. **Or run manually:**

Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

4. **Access:**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/api/docs

---

# 📝 Adding New Modes

To add a new mode:

1. Create mode definition in `backend/modes/your_mode.py`
2. Create execution strategy in `backend/strategies/your_strategy.py`
3. Register mode in `backend/modes/__init__.py`
4. Restart backend - UI updates automatically!

---

# 🔑 Key Design Principles

1. **Denario does the work** - We just configure it differently per mode
2. **Self-contained modes** - Easy to add/remove
3. **API-first** - Every mode can be called independently
4. **Dynamic UI** - No hardcoded forms
5. **Production-ready** - Docker, auth, monitoring built-in

---

# 📚 Documentation

- [README.md](README.md) - Quick start guide
- [Backend Documentation](backend/README.md) - API details
- [Frontend Documentation](frontend/README.md) - Component details

---

# 🤝 Contributing

This is an internal project. For questions, contact the development team.

---

**Built with ❤️ using Denario, FastAPI, and Next.js**
