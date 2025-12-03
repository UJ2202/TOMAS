# TOMAS MVP - Architecture Summary

**Last Updated:** December 2024
**Status:** Priority 1 Components Complete - Ready for Integration & Testing

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Implemented Components](#implemented-components)
4. [Component Details](#component-details)
5. [API Endpoints](#api-endpoints)
6. [Execution Flow](#execution-flow)
7. [Remaining Tasks](#remaining-tasks)
8. [Testing Strategy](#testing-strategy)

---

## 🎯 Executive Summary

TOMAS (Task-Oriented Multi-Agent System) is a backend platform that provides a unified interface for executing complex tasks using multiple AI agent frameworks. The MVP supports two powerful engines:

- **CMBAgent**: 48+ specialized agents for planning, control, and complex task execution
- **Denario**: Automated scientific research pipeline (idea → methodology → results → paper)

### Key Features Implemented

✅ **Dual Engine Architecture** - Equal support for CMBAgent and Denario
✅ **Session Management** - Complete persistence, history, checkpoints
✅ **Streaming Execution** - Real-time Server-Sent Events (SSE)
✅ **Background Tasks** - Async execution with status tracking
✅ **Cost Tracking** - Token usage and cost estimation
✅ **Human Intervention** - Pause/resume/cancel capabilities
✅ **File Management** - Upload/download with automatic path injection
✅ **Mode System** - Pluggable modes with engine routing

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FastAPI Backend                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────┐        ┌────────────────────┐          │
│  │   API Routers      │        │   Services Layer   │          │
│  ├────────────────────┤        ├────────────────────┤          │
│  │ • Execution        │───────▶│ • Mode Executor    │          │
│  │ • Modes            │        │ • Session Manager  │          │
│  │ • Streaming (SSE)  │        └────────────────────┘          │
│  └────────────────────┘                  │                      │
│                                           │                      │
│  ┌────────────────────┐                  ▼                      │
│  │   Mode Registry    │        ┌────────────────────┐          │
│  ├────────────────────┤        │  Engine Registry   │          │
│  │ • Research (🔬)    │        ├────────────────────┤          │
│  │ • RFP/SOW (📄)     │        │ • CMBAgent Engine  │          │
│  │ • ITOps (🎫)       │        │ • Denario Engine   │          │
│  └────────────────────┘        └────────────────────┘          │
│                                           │                      │
└───────────────────────────────────────────┼──────────────────────┘
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    │                                               │
         ┌──────────▼──────────┐                    ┌──────────▼──────────┐
         │   CMBAgent Engine   │                    │   Denario Engine    │
         ├─────────────────────┤                    ├─────────────────────┤
         │ • 48+ Agents        │                    │ • Research Pipeline │
         │ • Planning & Control│                    │ • Fast/CMB Backend  │
         │ • One-Shot/Chat     │                    │ • Idea→Paper        │
         │ • File Injection    │                    │ • Plot Generation   │
         └─────────────────────┘                    └─────────────────────┘
                    │                                               │
                    └───────────────────┬───────────────────────────┘
                                        │
                              ┌─────────▼─────────┐
                              │  SQLite Database  │
                              ├───────────────────┤
                              │ • Sessions        │
                              │ • Messages        │
                              │ • Files           │
                              │ • Costs           │
                              └───────────────────┘
```

---

## ✅ Implemented Components

### Engine Layer (`backend/engines/`)

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| **IEngine Interface** | `base.py` | ✅ Complete | Abstract base for all engines |
| **CMBAgent Wrapper** | `cmbagent_engine.py` | ✅ Complete | Wraps CMBAgent with standard interface |
| **Denario Wrapper** | `denario_engine.py` | ✅ Complete | Wraps Denario research pipeline |
| **Engine Registry** | `__init__.py` | ✅ Complete | Factory pattern for engine creation |

### Services Layer (`backend/services/`)

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| **Session Manager** | `session_manager.py` | ✅ Complete | Session lifecycle, messages, files |
| **Mode Executor** | `mode_executor.py` | ✅ Complete | Routes to engines, background tasks |

### API Routers (`backend/routers/`)

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| **Execution Router** | `execution.py` | ✅ Complete | Execute, stream, status, results |
| **Modes Router** | `modes.py` | ✅ Complete | List modes, get details |

### Mode Implementations (`backend/modes/`)

| Mode | File | Engine | Status | Description |
|------|------|--------|--------|-------------|
| **Research** | `research.py` | Denario | ✅ Complete | Scientific research automation |
| **RFP/SOW** | `rfp_sow.py` | CMBAgent | ✅ Complete | RFP analysis & proposals |
| **ITOps** | `itops.py` | CMBAgent | ✅ Complete | Ticket analysis & insights |

### Database Models (`backend/models/`)

| Model | File | Status | Description |
|-------|------|--------|-------------|
| **Session** | `session.py` | ✅ Complete | Session tracking |
| **Message** | `message.py` | ✅ Complete | Conversation history |
| **File** | `file.py` | ✅ Complete | File uploads/outputs |
| **Config** | `config.py` | ✅ Complete | User configurations |
| **Cost** | `cost.py` | ✅ Complete | Cost tracking |

---

## 🔍 Component Details

### 1. Engine Abstraction Layer

**Purpose**: Provide a unified interface for different agent frameworks.

#### IEngine Interface (`engines/base.py`)

```python
class IEngine(ABC):
    async def initialize(session_id, workspace_dir, config) -> None
    async def execute(task, input_data, mode_config) -> AsyncIterator[EngineOutput]
    async def pause() -> Dict[str, Any]
    async def resume(checkpoint) -> None
    async def intervene(intervention) -> None
    async def cleanup() -> None
    def get_cost_estimate(input_data) -> float
```

#### EngineOutput Dataclass

```python
@dataclass
class EngineOutput:
    status: str              # "running", "completed", "failed"
    content: str             # Human-readable output
    artifacts: List[Dict]    # Files, plots, etc.
    metadata: Dict           # Engine-specific data
    cost_info: Optional[Dict]  # Token usage, cost
```

### 2. CMBAgent Engine (`engines/cmbagent_engine.py`)

**Features:**
- Supports 48+ specialized agents
- Three execution modes: `planning_and_control`, `one_shot`, `chat`
- Automatic file path injection into task prompts
- Output artifact collection
- Cost tracking from CMBAgent reports

**Configuration:**
```python
engine_config = {
    "mode": "planning_and_control",
    "initial_agent": "task_improver",
    "max_rounds": 10,
    "api_keys": {...},
    "skip_rag_agents": True
}
```

### 3. Denario Engine (`engines/denario_engine.py`)

**Features:**
- Research pipeline: idea → methodology → results → paper
- Dual backend: `fast` (LangGraph) or `cmbagent` (detailed)
- Plot generation and collection
- Paper generation in target journal format
- Checkpoint/resume support

**Configuration:**
```python
engine_config = {
    "backend": "fast",  # or "cmbagent"
    "clear_project_dir": False
}
```

### 4. Session Manager (`services/session_manager.py`)

**Responsibilities:**
- Create and manage sessions
- Track execution status (CREATED → RUNNING → COMPLETED/FAILED)
- Store conversation messages with metadata
- Manage file uploads and outputs
- Handle checkpoints for pause/resume
- Calculate total tokens and costs

**Key Methods:**
```python
async def create_session(mode_id, engine_type, input_data) -> Session
async def update_status(session_id, status, error_message) -> Session
async def add_message(session_id, role, content, metadata, tokens, cost) -> Message
async def save_checkpoint(session_id, checkpoint_data) -> None
async def get_session_files(session_id, is_input) -> List[SessionFile]
```

### 5. Mode Executor (`services/mode_executor.py`)

**Responsibilities:**
- Route execution to appropriate engine based on mode
- Manage background task execution
- Stream results via async generators
- Handle pause/resume/cancel operations
- Coordinate with SessionManager for persistence

**Key Methods:**
```python
async def execute_mode(session_id, mode_id, task, input_data) -> AsyncIterator[EngineOutput]
async def execute_mode_background(session_id, mode_id, task, input_data) -> str
async def pause_execution(session_id) -> Dict
async def resume_execution(session_id) -> AsyncIterator[EngineOutput]
async def cancel_execution(session_id) -> None
```

---

## 🌐 API Endpoints

### Execution Endpoints (`/api/*`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/api/execute` | Start background execution |
| **POST** | `/api/execute/stream` | Start streaming execution (SSE) |
| **GET** | `/api/tasks/{session_id}/status` | Get execution status |
| **GET** | `/api/tasks/{session_id}/results` | Get execution results |
| **GET** | `/api/tasks/{session_id}/messages` | Get conversation history |
| **POST** | `/api/tasks/{session_id}/pause` | Pause execution |
| **POST** | `/api/tasks/{session_id}/resume` | Resume execution |
| **POST** | `/api/tasks/{session_id}/cancel` | Cancel execution |

### Mode Endpoints (`/api/modes/*`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/api/modes` | List all modes |
| **GET** | `/api/modes/{mode_id}` | Get mode details |
| **GET** | `/api/modes/category/{category}` | Filter by category |
| **GET** | `/api/modes/engine/{engine_type}` | Filter by engine |

---

## 🔄 Execution Flow

### 1. Background Execution Flow

```
Client Request
    ├─> POST /api/execute
    │     ├─> Validate mode exists
    │     ├─> Create session (SessionManager)
    │     ├─> Queue background task (ModeExecutor)
    │     └─> Return session_id immediately
    │
    └─> Background Task Execution
          ├─> Get mode configuration
          ├─> Get engine from EngineRegistry
          ├─> Initialize engine with session workspace
          ├─> Execute task via engine.execute()
          │     ├─> Stream EngineOutput objects
          │     ├─> Save each output as message
          │     └─> Update session status
          ├─> Collect artifacts
          ├─> Update output_data
          └─> Cleanup engine resources
```

### 2. Streaming Execution Flow

```
Client Request
    ├─> POST /api/execute/stream
    │     ├─> Validate mode exists
    │     ├─> Create session
    │     └─> Return SSE stream
    │
    └─> Server-Sent Events Stream
          ├─> For each EngineOutput:
          │     ├─> Format as JSON
          │     ├─> Send: data: {...}\n\n
          │     └─> Save to database
          └─> Close stream on completion/error
```

### 3. Engine Execution (CMBAgent Example)

```
ModeExecutor.execute_mode()
    ├─> EngineRegistry.get_engine(CMBAGENT)
    ├─> CMBAgentEngine.initialize(session_id, workspace, config)
    │     ├─> Create CMBAgent instance
    │     └─> Setup workspace directories
    │
    └─> CMBAgentEngine.execute(task, input_data, mode_config)
          ├─> Build file context from uploaded files
          ├─> Augment task with file paths
          ├─> Yield: EngineOutput(status="running", ...)
          ├─> Run CMBAgent.solve() in thread pool
          │     ├─> Agent swarm execution
          │     └─> Generate outputs
          ├─> Collect artifacts from workspace
          ├─> Calculate costs
          └─> Yield: EngineOutput(status="completed", ...)
```

---

## 🔧 Remaining Tasks

### Priority 1: Database Initialization

**Task:** Setup Alembic for database migrations

**Files to create:**
- `backend/alembic.ini` - Alembic configuration
- `backend/alembic/env.py` - Migration environment
- `backend/alembic/versions/*.py` - Initial migration

**Commands:**
```bash
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

**Why needed:** Create database tables from SQLAlchemy models

---

### Priority 2: Application Integration

**Task:** Update `backend/main.py` to integrate all components

**Required changes:**

1. **Import new routers:**
```python
from routers.execution import router as execution_router
from routers.modes import router as modes_router
```

2. **Initialize database on startup:**
```python
from core.database import init_db

@app.on_event("startup")
async def startup():
    await init_db()
    print("✅ Database initialized")
```

3. **Load modes on startup:**
```python
import modes  # Trigger mode registration

@app.on_event("startup")
async def load_modes():
    from core.mode_registry import ModeRegistry
    print(f"✅ Loaded {len(ModeRegistry.list_modes())} modes")
```

4. **Include routers:**
```python
app.include_router(execution_router)
app.include_router(modes_router)
```

5. **Remove old dependencies:**
- Remove references to old `DenarioService` if any
- Remove old `mode_executor` app.state references
- Ensure CORS is configured

---

### Priority 3: Environment Setup

**Task:** Ensure `.env` file is configured

**Required variables:**
```bash
# Application
APP_NAME=TOMAS
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Database
DATABASE_URL=sqlite+aiosqlite:///./tomas.db

# Workspace
WORKSPACE_DIR=../workspace
CONFIGS_DIR=../configs

# API Keys (optional, can be provided via UI later)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

---

### Priority 4: Schema Definitions

**Task:** Create Pydantic schemas for API validation

**File:** `backend/schemas/execution.py`

Currently schemas are defined inline in `routers/execution.py`. Should be moved to dedicated schema files for better organization:

```python
# schemas/execution.py
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class ExecuteRequest(BaseModel):
    mode_id: str
    task: str
    input_data: Dict[str, Any] = {}
    stream: bool = False

class ExecuteResponse(BaseModel):
    session_id: str
    status: str
    message: str

# ... other schemas
```

---

## 🧪 Testing Strategy

### Phase 1: Component Testing

**1. Test Mode Registry**
```python
# Test script
from core.mode_registry import ModeRegistry
import modes

print("Available modes:")
for mode in ModeRegistry.list_modes():
    print(f"  - {mode.id}: {mode.name} (Engine: {mode.engine.value})")
```

**2. Test Engine Registry**
```python
from engines import EngineRegistry
from core.enums import EngineType

# Test CMBAgent
engine = EngineRegistry.get_engine(EngineType.CMBAGENT)
print(f"CMBAgent Engine: {engine}")

# Test Denario
engine = EngineRegistry.get_engine(EngineType.DENARIO)
print(f"Denario Engine: {engine}")
```

### Phase 2: Database Testing

**1. Initialize Database**
```bash
cd backend
alembic upgrade head
```

**2. Test Session Creation**
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from core.database import get_db
from services.session_manager import SessionManager

async def test_session():
    async for db in get_db():
        manager = SessionManager(db)
        session = await manager.create_session(
            mode_id="research",
            engine_type="denario",
            input_data={"test": "data"}
        )
        print(f"Created session: {session.id}")
```

### Phase 3: API Testing

**1. Start the server**
```bash
cd backend
uvicorn main:app --reload
```

**2. Test Mode Listing**
```bash
curl http://localhost:8000/api/modes
```

**3. Test Execution**
```bash
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "mode_id": "research",
    "task": "Analyze climate data trends",
    "input_data": {
      "data_description": "Climate data from 1900-2020"
    }
  }'
```

**4. Test Status Checking**
```bash
# Use session_id from previous response
curl http://localhost:8000/api/tasks/{session_id}/status
```

**5. Test Streaming**
```bash
curl -N -X POST http://localhost:8000/api/execute/stream \
  -H "Content-Type: application/json" \
  -d '{
    "mode_id": "research",
    "task": "Analyze climate data",
    "input_data": {"data_description": "Test data"}
  }'
```

### Phase 4: End-to-End Testing

**Test Scenarios:**

1. **Research Mode (Denario)**
   - Upload data description
   - Execute research pipeline
   - Verify idea, methodology, results generated
   - Check artifacts (plots, paper)

2. **RFP/SOW Mode (CMBAgent)**
   - Upload RFP document
   - Specify cloud provider
   - Verify architecture proposal generated
   - Check cost estimates

3. **ITOps Mode (CMBAgent)**
   - Upload tickets CSV
   - Set analysis focus
   - Verify pattern detection
   - Check recommendations

---

## 📊 Current Status Summary

### What's Working
✅ All core architecture components implemented
✅ Both engines (CMBAgent & Denario) wrapped and integrated
✅ Three modes defined (one per engine + one extra for CMBAgent)
✅ Session management with full persistence
✅ API endpoints for execution and modes
✅ Streaming support via SSE
✅ Background task execution

### What's Missing
❌ Database not initialized (needs Alembic)
❌ Main.py not fully integrated with new components
❌ No end-to-end testing performed
❌ Schema files need organization
❌ Environment variables need verification

### Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Database initialization fails | High | Test Alembic setup in isolation first |
| Engine imports fail at runtime | High | Test imports before starting server |
| API keys not configured | Medium | Provide clear .env.example |
| Session workspace creation fails | Medium | Add proper error handling |
| Streaming doesn't work in production | Low | Test with actual frontend client |

---

## 🚀 Next Steps (Recommended Order)

1. **Setup Alembic** ⏱️ 15 mins
   - Initialize Alembic
   - Create initial migration
   - Test database creation

2. **Update main.py** ⏱️ 10 mins
   - Add router imports
   - Add startup events
   - Test server starts

3. **Create .env file** ⏱️ 5 mins
   - Copy from .env.example
   - Add API keys
   - Verify paths

4. **Test API Endpoints** ⏱️ 30 mins
   - Test mode listing
   - Test execution (background)
   - Test status checking
   - Test streaming

5. **End-to-End Test** ⏱️ 60 mins
   - Test research mode
   - Test RFP/SOW mode
   - Verify outputs generated
   - Check cost tracking

**Total estimated time to MVP:** ~2 hours

---

## 📚 Additional Resources

### Documentation to Create
- API documentation (OpenAPI/Swagger - auto-generated by FastAPI)
- Mode development guide
- Engine integration guide
- Deployment guide

### Future Enhancements (Post-MVP)
- Frontend UI (Next.js)
- File upload/download endpoints
- Config management UI
- WebSocket for real-time updates
- Authentication & authorization
- Multi-user support
- More modes (handbook, devops, data analysis)
- More engines (Kosmos, etc.)

---

## 🎯 Success Criteria

The MVP will be considered complete when:

✅ Database initializes without errors
✅ All 3 modes appear in `/api/modes` endpoint
✅ Can execute research mode and get results
✅ Can execute RFP/SOW mode with file upload
✅ Session status updates correctly
✅ Cost tracking works
✅ Streaming execution works
✅ Can pause/resume/cancel executions

---

**Document Version:** 1.0
**Last Updated:** December 2024
**Status:** Ready for Integration Phase
