# 🗺️ TOMAS MVP - Comprehensive Implementation Plan

**Version:** 2.0
**Last Updated:** December 2024
**Status:** Ready for Implementation

---

## 🎯 MVP Goals & Success Criteria

### Core Functionality
- ✅ All CMBAgent modes available and working end-to-end
- ✅ All Denario modes available and working end-to-end
- ✅ File upload with automatic path injection into agent context
- ✅ Three priority modes fully functional:
  1. **Research Mode** (Denario)
  2. **RFP/SOW Analysis** (CMBAgent)
  3. **Ticket Analysis** (CMBAgent)

### Advanced Features
- ✅ **Human-in-the-loop**: Real-time streaming with intervention capability
- ✅ **Config Management**: Upload API keys, credentials, YAML configs via UI
- ✅ **Output Normalization**: Unified display despite different engine formats
- ✅ **Cost Tracking**: Token usage and cost estimates per session
- ✅ **Conversation History**: Complete audit trail with replay capability
- ✅ **Session Management**: Robust SQLite-based persistence

### UI/UX Focus
- ✅ Modern, intuitive interface
- ✅ Real-time progress indicators
- ✅ File upload/download with preview
- ✅ Responsive design
- ✅ Error handling with user-friendly messages

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js + TypeScript)               │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ Mode Selector│  │Config Manager│  │  Session Dashboard │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           Task Execution Interface                       │   │
│  │  - File Upload    - Live Streaming  - Human Intervention│   │
│  │  - Cost Display   - Chat History    - Results Viewer    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓ WebSocket + REST API
┌─────────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI + SQLAlchemy)                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  Mode Registry   │  │  Engine Router   │  │Session Manager│ │
│  │  - CMBAgent modes│  │  - Route to      │  │- SQLite DB    │ │
│  │  - Denario modes │  │    correct engine│  │- History      │ │
│  │  - Future modes  │  └──────────────────┘  │- Checkpoints  │ │
│  └──────────────────┘                        └──────────────┘ │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │Config Service    │  │Streaming Service │  │Cost Tracker   │ │
│  │- API keys        │  │- WebSocket       │  │- Token counts │ │
│  │- Credentials     │  │- Event stream    │  │- Cost calc    │ │
│  │- YAML configs    │  │- Intervention    │  └──────────────┘ │
│  └──────────────────┘  └──────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Engine Abstraction Layer                      │
│  ┌───────────────────────┐    ┌───────────────────────┐        │
│  │   CMBAgent Engine     │    │   Denario Engine      │        │
│  │   - All CMBAgent modes│    │   - Research pipeline │        │
│  │   - Planning & control│    │   - CMBAgent backend  │        │
│  │   - 48+ agents        │    │   - LangGraph backend │        │
│  └───────────────────────┘    └───────────────────────┘        │
│                                                                  │
│  ┌───────────────────────┐    ┌───────────────────────┐        │
│  │  Output Normalizer    │    │   File Handler        │        │
│  │  - Unified format     │    │   - Auto path inject  │        │
│  │  - Format conversion  │    │   - Workspace mgmt    │        │
│  └───────────────────────┘    └───────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Key Design Principles

1. **Equal Weightage**: CMBAgent and Denario are equal engines - modes decide which to use
2. **Extensibility**: New engines (Kosmos, etc.) can be added easily
3. **Mode-Centric**: Each mode defines its engine, inputs, outputs, and behavior
4. **File-Aware**: System automatically injects file paths into agent context
5. **Human-in-the-Loop**: Users can intervene during execution
6. **Cost-Conscious**: Track and display all costs in real-time
7. **Session-Based**: Everything is session-scoped with full history
8. **UI-First**: Beautiful, intuitive interface with excellent UX

---

## 🗂️ Project Structure

```
TOMAS/
├── backend/
│   ├── main.py                          # FastAPI app entry point
│   ├── requirements.txt                 # Python dependencies
│   ├── pyproject.toml                   # Project metadata
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                    # Settings (Pydantic)
│   │   ├── database.py                  # SQLAlchemy async setup
│   │   ├── mode.py                      # Mode base class
│   │   ├── mode_registry.py             # Central mode registry
│   │   └── enums.py                     # Status enums, etc.
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── session.py                   # Session SQLAlchemy model
│   │   ├── message.py                   # Message/chat history model
│   │   ├── file.py                      # File upload model
│   │   ├── config.py                    # User config model
│   │   └── cost.py                      # Cost tracking model
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── session_manager.py           # Session lifecycle
│   │   ├── denario_service.py           # Denario engine wrapper
│   │   ├── cmbagent_service.py          # CMBAgent engine wrapper
│   │   ├── file_service.py              # File upload/management
│   │   ├── config_service.py            # Config/credentials management
│   │   ├── streaming_service.py         # WebSocket streaming
│   │   ├── cost_tracker.py              # Token/cost tracking
│   │   └── output_normalizer.py         # Unified output format
│   │
│   ├── engines/
│   │   ├── __init__.py
│   │   ├── base.py                      # IEngine abstract interface
│   │   ├── cmbagent_engine.py           # CMBAgent implementation
│   │   ├── denario_engine.py            # Denario implementation
│   │   └── output_adapter.py            # Format conversion
│   │
│   ├── modes/
│   │   ├── __init__.py                  # Import all modes
│   │   ├── research.py                  # Research mode (Denario)
│   │   ├── rfp_sow.py                   # RFP/SOW mode (CMBAgent)
│   │   ├── itops.py                     # Ticket analysis (CMBAgent)
│   │   ├── handbook.py                  # Handbook generation
│   │   ├── devops.py                    # DevOps mining
│   │   └── data_analysis.py             # Data analysis mode
│   │
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── research_strategy.py         # Research execution strategy
│   │   ├── rfp_strategy.py              # RFP execution strategy
│   │   ├── itops_strategy.py            # ITOps execution strategy
│   │   └── base_strategy.py             # Base strategy interface
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── modes.py                     # Mode listing/info
│   │   ├── execution.py                 # Task execution
│   │   ├── sessions.py                  # Session management
│   │   ├── files.py                     # File upload/download
│   │   ├── config.py                    # Config/credentials
│   │   ├── streaming.py                 # WebSocket endpoint
│   │   └── costs.py                     # Cost tracking endpoints
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── mode.py                      # Mode schemas
│   │   ├── session.py                   # Session schemas
│   │   ├── message.py                   # Message schemas
│   │   ├── file.py                      # File schemas
│   │   └── execution.py                 # Execution request/response
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logging.py                   # Structured logging
│       ├── exceptions.py                # Custom exceptions
│       └── helpers.py                   # Utility functions
│
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   │
│   ├── app/
│   │   ├── layout.tsx                   # Root layout
│   │   ├── page.tsx                     # Landing page
│   │   ├── modes/
│   │   │   └── page.tsx                 # Mode selector
│   │   ├── execute/
│   │   │   └── [mode_id]/page.tsx       # Execution interface
│   │   ├── sessions/
│   │   │   ├── page.tsx                 # Session list
│   │   │   └── [session_id]/page.tsx    # Session detail
│   │   └── settings/
│   │       └── page.tsx                 # Config management
│   │
│   ├── components/
│   │   ├── ModeCard.tsx                 # Mode display card
│   │   ├── ModeSelector.tsx             # Mode grid
│   │   ├── ExecutionInterface.tsx       # Main execution UI
│   │   ├── FileUpload.tsx               # File upload component
│   │   ├── StreamingDisplay.tsx         # Real-time results
│   │   ├── InterventionPanel.tsx        # Human intervention UI
│   │   ├── CostTracker.tsx              # Cost display
│   │   ├── ChatHistory.tsx              # Conversation history
│   │   ├── ConfigManager.tsx            # Config upload UI
│   │   ├── ResultsViewer.tsx            # Output display
│   │   └── SessionDashboard.tsx         # Session overview
│   │
│   ├── lib/
│   │   ├── api.ts                       # API client
│   │   ├── websocket.ts                 # WebSocket client
│   │   ├── types.ts                     # TypeScript types
│   │   └── utils.ts                     # Utility functions
│   │
│   └── public/
│       └── assets/                      # Static assets
│
├── workspace/                            # Execution workspace (gitignored)
│   └── sessions/
│       └── {session_id}/
│           ├── input_files/
│           ├── outputs/
│           ├── logs/
│           └── checkpoints/
│
├── configs/                              # User-uploaded configs (gitignored)
│   ├── api_keys.yaml
│   ├── credentials.yaml
│   └── custom_agents.yaml
│
├── .env.example                          # Environment template
├── .gitignore
├── docker-compose.yml                    # Docker setup
├── README.md                             # Quick start guide
└── IMPLEMENTATION_PLAN.md                # This file
```

---

# 📅 Phase-by-Phase Implementation

---

## Phase 0: Project Setup & Environment (Days 1-2)

### Goals
- ✅ Initialize project structure
- ✅ Setup development environment
- ✅ Configure database
- ✅ Test basic connectivity

### Tasks

#### Day 1: Backend Setup

**1. Initialize Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install --upgrade pip
```

**2. Install Dependencies**

Create `backend/requirements.txt`:
```txt
# Core Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6
websockets==12.0

# Database
sqlalchemy==2.0.25
alembic==1.13.1
aiosqlite==0.19.0

# Validation & Settings
pydantic==2.5.3
pydantic-settings==2.1.0

# Authentication (for future)
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# LLM & AI
openai==1.10.0
anthropic==0.18.0
google-generativeai==0.3.2
langchain==0.1.6
langgraph==0.0.20

# Utilities
python-dotenv==1.0.0
pyyaml==6.0.1
httpx==0.26.0
aiofiles==23.2.1

# Monitoring & Logging
structlog==24.1.0
```

**3. Create Environment Configuration**

`backend/.env.example`:
```bash
# Application
APP_NAME=TOMAS
HOST=0.0.0.0
PORT=8000
DEBUG=True
LOG_LEVEL=INFO

# Database
DATABASE_URL=sqlite+aiosqlite:///./tomas.db

# Workspace
WORKSPACE_DIR=../workspace
CONFIGS_DIR=../configs

# CORS (adjust for production)
CORS_ORIGINS=["http://localhost:3000"]

# API Keys (user can override via UI)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=

# Session Configuration
SESSION_TIMEOUT_HOURS=24
MAX_UPLOAD_SIZE_MB=100
```

**4. Core Configuration**

`backend/core/config.py`:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # Application
    APP_NAME: str = "TOMAS"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./tomas.db"

    # Workspace
    WORKSPACE_DIR: Path = Path("../workspace")
    CONFIGS_DIR: Path = Path("../configs")

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Session
    SESSION_TIMEOUT_HOURS: int = 24
    MAX_UPLOAD_SIZE_MB: int = 100

    # API Keys (can be overridden by user uploads)
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create directories
        self.WORKSPACE_DIR.mkdir(exist_ok=True, parents=True)
        self.CONFIGS_DIR.mkdir(exist_ok=True, parents=True)

settings = Settings()
```

**5. Database Setup**

`backend/core/database.py`:
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from .config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base for models
Base = declarative_base()

# Dependency for FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Initialize database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

**6. Enums**

`backend/core/enums.py`:
```python
from enum import Enum

class SessionStatus(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

class EngineType(str, Enum):
    CMBAGENT = "cmbagent"
    DENARIO = "denario"
    # Future engines
    KOSMOS = "kosmos"

class FileType(str, Enum):
    DOCUMENT = "document"  # PDF, DOCX, TXT
    DATA = "data"          # CSV, JSON, XLSX
    IMAGE = "image"        # PNG, JPG
    CODE = "code"          # PY, JS, etc.
    CONFIG = "config"      # YAML, JSON
```

#### Day 2: Frontend Setup

**1. Initialize Next.js Project**
```bash
npx create-next-app@latest frontend --typescript --tailwind --app --use-npm
cd frontend
```

**2. Install Dependencies**
```bash
npm install
npm install @tanstack/react-query axios socket.io-client
npm install lucide-react class-variance-authority clsx tailwind-merge
npm install recharts date-fns
npm install -D @types/node
```

**3. Configure TypeScript**

`frontend/tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**4. Environment Configuration**

`frontend/.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

**5. API Client**

`frontend/lib/api.ts`:
```typescript
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth (future)
api.interceptors.request.use((config) => {
  // Add auth token if available
  return config;
});

// Response interceptor for errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle errors globally
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);
```

**6. Type Definitions**

`frontend/lib/types.ts`:
```typescript
export enum SessionStatus {
  CREATED = "created",
  QUEUED = "queued",
  RUNNING = "running",
  PAUSED = "paused",
  COMPLETED = "completed",
  FAILED = "failed",
  CANCELLED = "cancelled",
}

export enum EngineType {
  CMBAGENT = "cmbagent",
  DENARIO = "denario",
}

export interface Mode {
  id: string;
  name: string;
  description: string;
  engine: EngineType;
  icon: string;
  inputs: InputField[];
  outputs: OutputField[];
  estimatedTime?: string;
  costEstimate?: string;
}

export interface InputField {
  name: string;
  type: "text" | "textarea" | "file" | "select" | "number";
  label: string;
  placeholder?: string;
  required: boolean;
  options?: string[];
  accept?: string;  // For file inputs
}

export interface OutputField {
  name: string;
  type: "text" | "file" | "plot" | "json" | "markdown";
  label: string;
}

export interface Session {
  id: string;
  mode_id: string;
  status: SessionStatus;
  created_at: string;
  updated_at: string;
  completed_at?: string;
  total_cost?: number;
  input_summary?: string;
}

export interface Message {
  id: string;
  session_id: string;
  role: "system" | "user" | "assistant" | "tool";
  content: string;
  timestamp: string;
  metadata?: Record<string, any>;
}

export interface StreamEvent {
  type: "status" | "message" | "progress" | "cost" | "intervention_needed";
  data: any;
  timestamp: string;
}
```

---

## Phase 1: Database Models & Session Management (Days 3-5)

### Goals
- ✅ Define all SQLAlchemy models
- ✅ Implement session lifecycle management
- ✅ Create session persistence layer
- ✅ Build conversation history storage

### Database Models

#### `backend/models/session.py`
```python
from sqlalchemy import Column, String, DateTime, Enum, Float, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from core.database import Base
from core.enums import SessionStatus, EngineType

class Session(Base):
    __tablename__ = "sessions"

    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Mode & Engine
    mode_id = Column(String(100), nullable=False, index=True)
    engine_type = Column(Enum(EngineType), nullable=False)

    # Status
    status = Column(Enum(SessionStatus), default=SessionStatus.CREATED, nullable=False, index=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Input/Output
    input_data = Column(JSON, nullable=True)  # Original input
    output_data = Column(JSON, nullable=True)  # Final output

    # Execution Metadata
    error_message = Column(Text, nullable=True)
    checkpoint_data = Column(JSON, nullable=True)  # For pause/resume

    # Cost Tracking
    total_cost = Column(Float, default=0.0)
    total_tokens = Column(Float, default=0.0)

    # Workspace
    workspace_path = Column(String(500), nullable=True)

    # Relationships
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    files = relationship("SessionFile", back_populates="session", cascade="all, delete-orphan")
    costs = relationship("CostRecord", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Session(id={self.id}, mode={self.mode_id}, status={self.status})>"
```

#### `backend/models/message.py`
```python
from sqlalchemy import Column, String, DateTime, Enum, Text, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database import Base
from core.enums import MessageRole

class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False, index=True)

    # Message Content
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)

    # Metadata
    metadata = Column(JSON, nullable=True)  # Agent name, tool calls, etc.

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    sequence_number = Column(Integer, nullable=False)  # Order in conversation

    # Cost for this message
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)

    # Relationships
    session = relationship("Session", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, session={self.session_id})>"
```

#### `backend/models/file.py`
```python
from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database import Base

class SessionFile(Base):
    __tablename__ = "session_files"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False, index=True)

    # File Info
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)  # Actual path on disk
    file_size = Column(Integer, nullable=False)  # Bytes
    mime_type = Column(String(100), nullable=True)

    # Type
    is_input = Column(Boolean, default=True)  # Input or output file

    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    session = relationship("Session", back_populates="files")

    def __repr__(self):
        return f"<SessionFile(id={self.id}, filename={self.filename})>"
```

#### `backend/models/config.py`
```python
from sqlalchemy import Column, String, DateTime, Text, Boolean
from datetime import datetime

from core.database import Base

class UserConfig(Base):
    __tablename__ = "user_configs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Config Type
    config_type = Column(String(50), nullable=False)  # "api_keys", "credentials", "yaml"
    config_name = Column(String(100), nullable=False)  # "openai", "anthropic", etc.

    # Content (encrypted in production)
    config_value = Column(Text, nullable=False)

    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserConfig(type={self.config_type}, name={self.config_name})>"
```

#### `backend/models/cost.py`
```python
from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database import Base

class CostRecord(Base):
    __tablename__ = "cost_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False, index=True)

    # Model Info
    model_name = Column(String(100), nullable=False)
    provider = Column(String(50), nullable=False)  # "openai", "anthropic", "google"

    # Token Usage
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)

    # Cost
    cost = Column(Float, default=0.0)

    # Metadata
    metadata = Column(JSON, nullable=True)  # Agent name, operation, etc.

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    session = relationship("Session", back_populates="costs")

    def __repr__(self):
        return f"<CostRecord(session={self.session_id}, cost=${self.cost:.4f})>"
```

### Session Manager Service

#### `backend/services/session_manager.py`
```python
from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pathlib import Path
import shutil

from models.session import Session
from models.message import Message
from models.file import SessionFile
from core.enums import SessionStatus, MessageRole
from core.config import settings

class SessionManager:
    """Manages session lifecycle and persistence"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(
        self,
        mode_id: str,
        engine_type: str,
        input_data: Dict[str, Any]
    ) -> Session:
        """Create a new session"""
        session = Session(
            mode_id=mode_id,
            engine_type=engine_type,
            input_data=input_data,
            status=SessionStatus.CREATED
        )

        # Create workspace directory
        workspace_path = settings.WORKSPACE_DIR / "sessions" / session.id
        workspace_path.mkdir(parents=True, exist_ok=True)
        (workspace_path / "input_files").mkdir(exist_ok=True)
        (workspace_path / "outputs").mkdir(exist_ok=True)
        (workspace_path / "logs").mkdir(exist_ok=True)
        (workspace_path / "checkpoints").mkdir(exist_ok=True)

        session.workspace_path = str(workspace_path)

        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)

        return session

    async def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        result = await self.db.execute(
            select(Session).where(Session.id == session_id)
        )
        return result.scalar_one_or_none()

    async def update_status(
        self,
        session_id: str,
        status: SessionStatus,
        error_message: Optional[str] = None
    ) -> Session:
        """Update session status"""
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        session.status = status
        if error_message:
            session.error_message = error_message

        if status == SessionStatus.RUNNING and not session.started_at:
            from datetime import datetime
            session.started_at = datetime.utcnow()

        if status in [SessionStatus.COMPLETED, SessionStatus.FAILED, SessionStatus.CANCELLED]:
            from datetime import datetime
            session.completed_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def add_message(
        self,
        session_id: str,
        role: MessageRole,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        tokens_used: int = 0,
        cost: float = 0.0
    ) -> Message:
        """Add a message to session history"""
        # Get sequence number
        result = await self.db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.sequence_number.desc())
            .limit(1)
        )
        last_message = result.scalar_one_or_none()
        sequence_number = (last_message.sequence_number + 1) if last_message else 0

        message = Message(
            session_id=session_id,
            role=role,
            content=content,
            metadata=metadata,
            sequence_number=sequence_number,
            tokens_used=tokens_used,
            cost=cost
        )

        self.db.add(message)

        # Update session cost
        session = await self.get_session(session_id)
        session.total_tokens += tokens_used
        session.total_cost += cost

        await self.db.commit()
        await self.db.refresh(message)

        return message

    async def get_messages(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Message]:
        """Get conversation history"""
        query = select(Message).where(
            Message.session_id == session_id
        ).order_by(Message.sequence_number)

        if limit:
            query = query.limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def save_checkpoint(
        self,
        session_id: str,
        checkpoint_data: Dict[str, Any]
    ) -> None:
        """Save checkpoint for pause/resume"""
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        session.checkpoint_data = checkpoint_data
        await self.db.commit()

    async def load_checkpoint(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load checkpoint data"""
        session = await self.get_session(session_id)
        return session.checkpoint_data if session else None

    async def list_sessions(
        self,
        status: Optional[SessionStatus] = None,
        mode_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Session]:
        """List sessions with filters"""
        query = select(Session).order_by(Session.created_at.desc())

        if status:
            query = query.where(Session.status == status)
        if mode_id:
            query = query.where(Session.mode_id == mode_id)

        query = query.limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def delete_session(self, session_id: str) -> None:
        """Delete session and cleanup workspace"""
        session = await self.get_session(session_id)
        if not session:
            return

        # Delete workspace
        if session.workspace_path:
            workspace_path = Path(session.workspace_path)
            if workspace_path.exists():
                shutil.rmtree(workspace_path)

        # Delete from database (cascade deletes messages, files, costs)
        await self.db.delete(session)
        await self.db.commit()

    def get_workspace_dir(self, session_id: str) -> Path:
        """Get workspace directory for session"""
        return settings.WORKSPACE_DIR / "sessions" / session_id
```

### Initialize Database

#### `backend/alembic.ini` (for migrations)
```ini
[alembic]
script_location = alembic
sqlalchemy.url = sqlite+aiosqlite:///./tomas.db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

#### Initialize Alembic
```bash
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial models"
alembic upgrade head
```

---

## Phase 2: Engine Abstraction Layer (Days 6-8)

### Goals
- ✅ Define IEngine interface
- ✅ Implement CMBAgent engine wrapper
- ✅ Implement Denario engine wrapper
- ✅ Create output normalization layer
- ✅ Build engine router

### Engine Interface

#### `backend/engines/base.py`
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List, AsyncIterator, Optional
from dataclasses import dataclass

@dataclass
class EngineOutput:
    """Standardized output format from any engine"""
    status: str  # "running", "completed", "failed"
    content: str
    artifacts: List[Dict[str, Any]]  # Files, plots, etc.
    metadata: Dict[str, Any]  # Engine-specific metadata
    cost_info: Optional[Dict[str, Any]] = None

class IEngine(ABC):
    """Base interface for all execution engines"""

    @abstractmethod
    async def initialize(
        self,
        session_id: str,
        workspace_dir: str,
        config: Dict[str, Any]
    ) -> None:
        """Initialize engine for a session"""
        pass

    @abstractmethod
    async def execute(
        self,
        task: str,
        input_data: Dict[str, Any],
        mode_config: Dict[str, Any]
    ) -> AsyncIterator[EngineOutput]:
        """
        Execute task and yield results

        This is an async generator that yields EngineOutput objects
        as the execution progresses, enabling real-time streaming.
        """
        pass

    @abstractmethod
    async def pause(self) -> Dict[str, Any]:
        """Pause execution and return checkpoint"""
        pass

    @abstractmethod
    async def resume(self, checkpoint: Dict[str, Any]) -> None:
        """Resume from checkpoint"""
        pass

    @abstractmethod
    async def intervene(self, intervention: Dict[str, Any]) -> None:
        """Handle human intervention"""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass

    @abstractmethod
    def get_cost_estimate(self, input_data: Dict[str, Any]) -> float:
        """Estimate cost before execution"""
        pass
```

### CMBAgent Engine

#### `backend/engines/cmbagent_engine.py`
```python
from typing import Dict, Any, AsyncIterator
from pathlib import Path
import asyncio

from .base import IEngine, EngineOutput
from cmbagent import CMBAgent

class CMBAgentEngine(IEngine):
    """Wrapper for CMBAgent with standardized interface"""

    def __init__(self):
        self.agent: Optional[CMBAgent] = None
        self.session_id: Optional[str] = None
        self.workspace_dir: Optional[Path] = None
        self._pause_requested = False

    async def initialize(
        self,
        session_id: str,
        workspace_dir: str,
        config: Dict[str, Any]
    ) -> None:
        """Initialize CMBAgent instance"""
        self.session_id = session_id
        self.workspace_dir = Path(workspace_dir)

        # Initialize CMBAgent with workspace
        self.agent = CMBAgent(
            workspace=str(self.workspace_dir / "outputs"),
            **config
        )

    async def execute(
        self,
        task: str,
        input_data: Dict[str, Any],
        mode_config: Dict[str, Any]
    ) -> AsyncIterator[EngineOutput]:
        """
        Execute task with CMBAgent

        Mode config should include:
        - mode: "planning_and_control", "one_shot", etc.
        - initial_agent: Starting agent
        - max_rounds: Maximum rounds
        """
        yield EngineOutput(
            status="running",
            content="Initializing CMBAgent...",
            artifacts=[],
            metadata={"step": "initialization"}
        )

        # Extract file paths from input_data
        file_context = self._build_file_context(input_data)

        # Augment task with file context
        full_task = f"{task}\n\n{file_context}" if file_context else task

        # Execute CMBAgent
        mode = mode_config.get("mode", "planning_and_control")
        initial_agent = mode_config.get("initial_agent", "task_improver")
        max_rounds = mode_config.get("max_rounds", 10)

        yield EngineOutput(
            status="running",
            content=f"Starting execution with mode: {mode}",
            artifacts=[],
            metadata={"mode": mode, "initial_agent": initial_agent}
        )

        # Run CMBAgent (this is synchronous, so run in thread pool)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self.agent.solve,
            full_task,
            initial_agent,
            None,  # shared_context
            mode,
            None,  # step
            max_rounds
        )

        # Parse result and collect artifacts
        artifacts = self._collect_artifacts()

        yield EngineOutput(
            status="completed",
            content=str(result),
            artifacts=artifacts,
            metadata={"mode": mode, "rounds": "completed"},
            cost_info=self._calculate_cost()
        )

    def _build_file_context(self, input_data: Dict[str, Any]) -> str:
        """Build file context string for agent"""
        uploaded_files = input_data.get("uploaded_files", [])
        if not uploaded_files:
            return ""

        file_list = []
        for file_info in uploaded_files:
            file_path = file_info.get("path")
            file_name = file_info.get("name")
            file_list.append(f"- {file_name}: {file_path}")

        return f"Uploaded files:\n" + "\n".join(file_list)

    def _collect_artifacts(self) -> List[Dict[str, Any]]:
        """Collect output files from workspace"""
        artifacts = []
        output_dir = self.workspace_dir / "outputs"

        if output_dir.exists():
            for file_path in output_dir.rglob("*"):
                if file_path.is_file():
                    artifacts.append({
                        "type": "file",
                        "name": file_path.name,
                        "path": str(file_path),
                        "size": file_path.stat().st_size
                    })

        return artifacts

    def _calculate_cost(self) -> Dict[str, Any]:
        """Calculate cost from CMBAgent usage"""
        # TODO: Implement actual cost tracking from CMBAgent
        return {
            "total_tokens": 0,
            "cost_usd": 0.0
        }

    async def pause(self) -> Dict[str, Any]:
        """Pause execution"""
        self._pause_requested = True
        # TODO: Implement actual pause logic
        return {"state": "paused"}

    async def resume(self, checkpoint: Dict[str, Any]) -> None:
        """Resume from checkpoint"""
        self._pause_requested = False
        # TODO: Implement actual resume logic
        pass

    async def intervene(self, intervention: Dict[str, Any]) -> None:
        """Handle human intervention"""
        # TODO: Implement intervention (e.g., redirect to different agent)
        pass

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self.agent = None

    def get_cost_estimate(self, input_data: Dict[str, Any]) -> float:
        """Estimate cost"""
        # Rough estimate based on input size
        input_size = len(str(input_data))
        estimated_tokens = input_size * 1.5  # Rough estimate
        cost_per_token = 0.00002  # $0.02 per 1K tokens
        return estimated_tokens * cost_per_token
```

### Denario Engine

#### `backend/engines/denario_engine.py`
```python
from typing import Dict, Any, AsyncIterator
from pathlib import Path
import asyncio

from .base import IEngine, EngineOutput
from denario import Denario

class DenarioEngine(IEngine):
    """Wrapper for Denario with standardized interface"""

    def __init__(self):
        self.denario: Optional[Denario] = None
        self.session_id: Optional[str] = None
        self.workspace_dir: Optional[Path] = None

    async def initialize(
        self,
        session_id: str,
        workspace_dir: str,
        config: Dict[str, Any]
    ) -> None:
        """Initialize Denario instance"""
        self.session_id = session_id
        self.workspace_dir = Path(workspace_dir)

        # Initialize Denario
        self.denario = Denario(
            workspace=str(self.workspace_dir / "outputs"),
            backend=config.get("backend", "detailed"),  # "detailed" or "fast"
            **config
        )

    async def execute(
        self,
        task: str,
        input_data: Dict[str, Any],
        mode_config: Dict[str, Any]
    ) -> AsyncIterator[EngineOutput]:
        """
        Execute task with Denario

        For research mode, task is the data description
        """
        yield EngineOutput(
            status="running",
            content="Initializing Denario research pipeline...",
            artifacts=[],
            metadata={"step": "initialization", "backend": self.denario.backend}
        )

        # Set data description
        yield EngineOutput(
            status="running",
            content="Setting up research context...",
            artifacts=[],
            metadata={"step": "data_description"}
        )

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self.denario.set_data_description,
            task
        )

        # Get idea
        yield EngineOutput(
            status="running",
            content="Generating research idea...",
            artifacts=[],
            metadata={"step": "idea_generation"}
        )

        await loop.run_in_executor(None, self.denario.get_idea)

        yield EngineOutput(
            status="running",
            content=f"Research idea: {self.denario.research.idea}",
            artifacts=[],
            metadata={"step": "idea_generated", "idea": self.denario.research.idea}
        )

        # Get methodology
        yield EngineOutput(
            status="running",
            content="Developing methodology...",
            artifacts=[],
            metadata={"step": "methodology"}
        )

        await loop.run_in_executor(None, self.denario.get_method)

        yield EngineOutput(
            status="running",
            content=f"Methodology: {self.denario.research.methodology[:200]}...",
            artifacts=[],
            metadata={"step": "methodology_generated"}
        )

        # Get results
        yield EngineOutput(
            status="running",
            content="Executing research and analyzing results...",
            artifacts=[],
            metadata={"step": "results"}
        )

        await loop.run_in_executor(None, self.denario.get_results)

        # Collect plot artifacts
        plot_artifacts = []
        for plot_path in self.denario.research.plot_paths:
            plot_artifacts.append({
                "type": "plot",
                "name": Path(plot_path).name,
                "path": plot_path
            })

        yield EngineOutput(
            status="running",
            content="Results obtained. Generating paper...",
            artifacts=plot_artifacts,
            metadata={"step": "paper_generation"}
        )

        # Generate paper
        await loop.run_in_executor(None, self.denario.get_paper)

        # Collect all artifacts
        artifacts = self._collect_artifacts()

        yield EngineOutput(
            status="completed",
            content=f"Research completed!\n\nIdea: {self.denario.research.idea}\n\nResults: {self.denario.research.results}",
            artifacts=artifacts,
            metadata={
                "idea": self.denario.research.idea,
                "methodology": self.denario.research.methodology,
                "results": self.denario.research.results,
                "keywords": self.denario.research.keywords
            },
            cost_info=self._calculate_cost()
        )

    def _collect_artifacts(self) -> List[Dict[str, Any]]:
        """Collect all output artifacts"""
        artifacts = []

        # Plots
        for plot_path in self.denario.research.plot_paths:
            artifacts.append({
                "type": "plot",
                "name": Path(plot_path).name,
                "path": plot_path
            })

        # Paper (if generated)
        output_dir = self.workspace_dir / "outputs"
        if output_dir.exists():
            for file_path in output_dir.rglob("*.pdf"):
                artifacts.append({
                    "type": "document",
                    "name": file_path.name,
                    "path": str(file_path)
                })

        return artifacts

    def _calculate_cost(self) -> Dict[str, Any]:
        """Calculate cost from Denario usage"""
        # TODO: Implement actual cost tracking
        return {
            "total_tokens": 0,
            "cost_usd": 0.0
        }

    async def pause(self) -> Dict[str, Any]:
        """Pause execution"""
        # Save current state
        return {
            "research": {
                "data_description": self.denario.research.data_description,
                "idea": self.denario.research.idea,
                "methodology": self.denario.research.methodology,
                "results": self.denario.research.results,
                "plot_paths": self.denario.research.plot_paths,
            }
        }

    async def resume(self, checkpoint: Dict[str, Any]) -> None:
        """Resume from checkpoint"""
        research_data = checkpoint.get("research", {})
        self.denario.research.data_description = research_data.get("data_description", "")
        self.denario.research.idea = research_data.get("idea", "")
        self.denario.research.methodology = research_data.get("methodology", "")
        self.denario.research.results = research_data.get("results", "")
        self.denario.research.plot_paths = research_data.get("plot_paths", [])

    async def intervene(self, intervention: Dict[str, Any]) -> None:
        """Handle human intervention"""
        # Could allow user to modify idea, methodology, etc.
        intervention_type = intervention.get("type")

        if intervention_type == "modify_idea":
            self.denario.research.idea = intervention.get("new_idea")
        elif intervention_type == "modify_methodology":
            self.denario.research.methodology = intervention.get("new_methodology")

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self.denario = None

    def get_cost_estimate(self, input_data: Dict[str, Any]) -> float:
        """Estimate cost for research"""
        # Research typically uses more tokens
        return 5.0  # Rough estimate: $5 per research run
```

### Engine Registry & Router

#### `backend/engines/__init__.py`
```python
from typing import Dict, Type
from .base import IEngine
from .cmbagent_engine import CMBAgentEngine
from .denario_engine import DenarioEngine
from core.enums import EngineType

class EngineRegistry:
    """Registry of available engines"""

    _engines: Dict[EngineType, Type[IEngine]] = {
        EngineType.CMBAGENT: CMBAgentEngine,
        EngineType.DENARIO: DenarioEngine,
    }

    @classmethod
    def get_engine(cls, engine_type: EngineType) -> IEngine:
        """Get engine instance by type"""
        engine_class = cls._engines.get(engine_type)
        if not engine_class:
            raise ValueError(f"Unknown engine type: {engine_type}")
        return engine_class()

    @classmethod
    def register_engine(cls, engine_type: EngineType, engine_class: Type[IEngine]):
        """Register a new engine (for future extensibility)"""
        cls._engines[engine_type] = engine_class

    @classmethod
    def list_engines(cls) -> List[str]:
        """List available engines"""
        return [e.value for e in cls._engines.keys()]
```

---

## Phase 3: Mode System & Registry (Days 9-11)

### Goals
- ✅ Define Mode base class
- ✅ Implement mode registry
- ✅ Create 3 priority modes
- ✅ Build mode discovery system

### Mode Base Class

#### `backend/core/mode.py`
```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from core.enums import EngineType

class InputField(BaseModel):
    """Input field definition"""
    name: str
    type: str  # "text", "textarea", "file", "select", "number"
    label: str
    placeholder: Optional[str] = None
    required: bool = True
    options: Optional[List[str]] = None  # For select
    accept: Optional[str] = None  # For file inputs (e.g., ".csv,.xlsx")
    help_text: Optional[str] = None

class OutputField(BaseModel):
    """Output field definition"""
    name: str
    type: str  # "text", "file", "plot", "json", "markdown"
    label: str
    description: Optional[str] = None

class ModeConfig(BaseModel):
    """Configuration for mode execution"""
    # Engine-specific configuration
    engine_config: Dict[str, Any] = Field(default_factory=dict)

    # Execution parameters
    timeout_minutes: int = 60
    max_retries: int = 3

    # Human-in-the-loop
    allow_intervention: bool = True
    intervention_points: List[str] = Field(default_factory=list)

class Mode(BaseModel):
    """Base mode definition"""
    id: str
    name: str
    description: str
    engine: EngineType
    icon: str = "🤖"

    # Input/Output definitions
    inputs: List[InputField]
    outputs: List[OutputField]

    # Configuration
    config: ModeConfig = Field(default_factory=ModeConfig)

    # Metadata
    category: str = "general"
    tags: List[str] = Field(default_factory=list)
    estimated_time: Optional[str] = None
    cost_estimate: Optional[str] = None

    # Documentation
    examples: List[Dict[str, Any]] = Field(default_factory=list)
    tips: List[str] = Field(default_factory=list)
```

### Mode Registry

#### `backend/core/mode_registry.py`
```python
from typing import Dict, List, Optional
from .mode import Mode

class ModeRegistry:
    """Central registry for all modes"""

    _modes: Dict[str, Mode] = {}

    @classmethod
    def register(cls, mode: Mode) -> None:
        """Register a mode"""
        cls._modes[mode.id] = mode
        print(f"✅ Registered mode: {mode.id} ({mode.name})")

    @classmethod
    def get(cls, mode_id: str) -> Optional[Mode]:
        """Get mode by ID"""
        return cls._modes.get(mode_id)

    @classmethod
    def list_all(cls) -> List[Mode]:
        """List all registered modes"""
        return list(cls._modes.values())

    @classmethod
    def list_by_engine(cls, engine: str) -> List[Mode]:
        """List modes for specific engine"""
        return [m for m in cls._modes.values() if m.engine == engine]

    @classmethod
    def list_by_category(cls, category: str) -> List[Mode]:
        """List modes by category"""
        return [m for m in cls._modes.values() if m.category == category]

# Decorator for easy mode registration
def register_mode(mode: Mode):
    """Decorator to register a mode"""
    ModeRegistry.register(mode)
    return mode
```

### Mode Implementations

#### `backend/modes/research.py`
```python
from core.mode import Mode, InputField, OutputField, ModeConfig
from core.enums import EngineType
from core.mode_registry import register_mode

research_mode = Mode(
    id="research",
    name="Scientific Research",
    description="Automated scientific research pipeline: generate ideas, develop methodology, execute experiments, and write papers",
    engine=EngineType.DENARIO,
    icon="🔬",

    inputs=[
        InputField(
            name="data_description",
            type="textarea",
            label="Data Description",
            placeholder="Describe your dataset and research domain...",
            required=True,
            help_text="Provide details about your data: what it contains, format, size, and research domain"
        ),
        InputField(
            name="data_files",
            type="file",
            label="Data Files (Optional)",
            required=False,
            accept=".csv,.xlsx,.json,.txt",
            help_text="Upload your dataset files (optional)"
        ),
        InputField(
            name="backend",
            type="select",
            label="Execution Backend",
            options=["detailed", "fast"],
            required=True,
            help_text="Detailed: CMBAgent (slower, more thorough). Fast: LangGraph (faster, less detailed)"
        ),
        InputField(
            name="focus_area",
            type="text",
            label="Focus Area (Optional)",
            placeholder="e.g., machine learning, statistical analysis",
            required=False
        )
    ],

    outputs=[
        OutputField(
            name="idea",
            type="markdown",
            label="Research Idea",
            description="Generated research hypothesis and objectives"
        ),
        OutputField(
            name="methodology",
            type="markdown",
            label="Methodology",
            description="Detailed research methodology and approach"
        ),
        OutputField(
            name="results",
            type="markdown",
            label="Results",
            description="Research findings and analysis"
        ),
        OutputField(
            name="plots",
            type="plot",
            label="Visualizations",
            description="Generated plots and figures"
        ),
        OutputField(
            name="paper",
            type="file",
            label="Research Paper",
            description="Complete research paper (PDF)"
        )
    ],

    config=ModeConfig(
        engine_config={
            "backend": "detailed",  # Default backend
        },
        timeout_minutes=120,
        allow_intervention=True,
        intervention_points=["after_idea", "after_methodology"]
    ),

    category="research",
    tags=["science", "research", "automation", "paper"],
    estimated_time="30-60 minutes",
    cost_estimate="$3-5",

    examples=[
        {
            "name": "Climate Data Analysis",
            "data_description": "Historical climate data from 1900-2020 including temperature, precipitation, and CO2 levels",
            "backend": "detailed"
        },
        {
            "name": "Gene Expression Study",
            "data_description": "RNA-seq data from cancer vs normal tissue samples",
            "backend": "fast"
        }
    ],

    tips=[
        "Provide detailed data description for better results",
        "Use 'detailed' backend for novel research",
        "Use 'fast' backend for exploratory analysis",
        "You can intervene after idea generation to refine direction"
    ]
)

# Register the mode
register_mode(research_mode)
```

#### `backend/modes/rfp_sow.py`
```python
from core.mode import Mode, InputField, OutputField, ModeConfig
from core.enums import EngineType
from core.mode_registry import register_mode

rfp_sow_mode = Mode(
    id="rfp_sow",
    name="RFP/SOW Analysis",
    description="Analyze RFP documents and generate technical proposals with architecture diagrams, cost estimates, and SOW",
    engine=EngineType.CMBAGENT,
    icon="📄",

    inputs=[
        InputField(
            name="rfp_document",
            type="file",
            label="RFP Document",
            placeholder="Upload RFP document",
            required=True,
            accept=".pdf,.docx,.txt",
            help_text="Upload the RFP or requirements document"
        ),
        InputField(
            name="cloud_provider",
            type="select",
            label="Preferred Cloud Provider",
            options=["AWS", "Azure", "GCP", "Multi-Cloud", "On-Premise"],
            required=True
        ),
        InputField(
            name="budget_range",
            type="text",
            label="Budget Range (Optional)",
            placeholder="e.g., $50K-$100K",
            required=False
        ),
        InputField(
            name="timeline",
            type="text",
            label="Timeline (Optional)",
            placeholder="e.g., 6 months",
            required=False
        ),
        InputField(
            name="focus_areas",
            type="textarea",
            label="Specific Focus Areas (Optional)",
            placeholder="e.g., Security, Scalability, Cost optimization",
            required=False
        )
    ],

    outputs=[
        OutputField(
            name="requirements_analysis",
            type="markdown",
            label="Requirements Analysis",
            description="Parsed and analyzed requirements from RFP"
        ),
        OutputField(
            name="architecture",
            type="markdown",
            label="Proposed Architecture",
            description="Technical architecture and design"
        ),
        OutputField(
            name="architecture_diagram",
            type="file",
            label="Architecture Diagram",
            description="Visual architecture diagram"
        ),
        OutputField(
            name="cost_estimate",
            type="json",
            label="Cost Breakdown",
            description="Detailed cost estimates by component"
        ),
        OutputField(
            name="sow",
            type="file",
            label="Statement of Work",
            description="Complete SOW document (PDF)"
        ),
        OutputField(
            name="risks",
            type="markdown",
            label="Risk Analysis",
            description="Identified risks and mitigation strategies"
        )
    ],

    config=ModeConfig(
        engine_config={
            "mode": "planning_and_control",
            "initial_agent": "document_parser",
            "max_rounds": 15
        },
        timeout_minutes=90,
        allow_intervention=True,
        intervention_points=["after_requirements", "after_architecture"]
    ),

    category="consulting",
    tags=["rfp", "sow", "architecture", "cloud", "consulting"],
    estimated_time="20-40 minutes",
    cost_estimate="$2-4",

    examples=[
        {
            "name": "Microservices Migration",
            "cloud_provider": "AWS",
            "description": "RFP for migrating monolith to microservices"
        },
        {
            "name": "Data Platform Build",
            "cloud_provider": "GCP",
            "description": "Building enterprise data platform"
        }
    ],

    tips=[
        "Ensure RFP document is clear and well-formatted",
        "Specify budget range for more accurate cost estimates",
        "You can intervene to adjust architecture before cost estimation",
        "Multi-cloud option will provide comparison across providers"
    ]
)

register_mode(rfp_sow_mode)
```

#### `backend/modes/itops.py`
```python
from core.mode import Mode, InputField, OutputField, ModeConfig
from core.enums import EngineType
from core.mode_registry import register_mode

itops_mode = Mode(
    id="itops",
    name="ITOps Ticket Analysis",
    description="Analyze IT operations tickets, identify patterns, root causes, and generate actionable insights",
    engine=EngineType.CMBAGENT,
    icon="🎫",

    inputs=[
        InputField(
            name="tickets_file",
            type="file",
            label="Tickets Data",
            placeholder="Upload tickets CSV/Excel",
            required=True,
            accept=".csv,.xlsx",
            help_text="Upload ticket data with columns: ID, Title, Description, Status, Priority, Category, Created, Resolved"
        ),
        InputField(
            name="time_range",
            type="select",
            label="Time Range",
            options=["Last 7 days", "Last 30 days", "Last 90 days", "Last year", "All time"],
            required=True
        ),
        InputField(
            name="focus_area",
            type="select",
            label="Analysis Focus",
            options=[
                "Root Cause Analysis",
                "Pattern Detection",
                "Predictive Analysis",
                "Team Performance",
                "SLA Compliance",
                "Cost Analysis"
            ],
            required=True
        ),
        InputField(
            name="priority_filter",
            type="select",
            label="Priority Filter (Optional)",
            options=["All", "Critical", "High", "Medium", "Low"],
            required=False
        )
    ],

    outputs=[
        OutputField(
            name="summary",
            type="markdown",
            label="Executive Summary",
            description="High-level insights and key findings"
        ),
        OutputField(
            name="patterns",
            type="markdown",
            label="Identified Patterns",
            description="Recurring issues and trends"
        ),
        OutputField(
            name="root_causes",
            type="markdown",
            label="Root Cause Analysis",
            description="Identified root causes and contributing factors"
        ),
        OutputField(
            name="recommendations",
            type="markdown",
            label="Recommendations",
            description="Actionable recommendations to reduce tickets"
        ),
        OutputField(
            name="dashboard",
            type="plot",
            label="Analytics Dashboard",
            description="Visual analytics and charts"
        ),
        OutputField(
            name="report",
            type="file",
            label="Full Report",
            description="Complete analysis report (PDF)"
        )
    ],

    config=ModeConfig(
        engine_config={
            "mode": "planning_and_control",
            "initial_agent": "data_analyst",
            "max_rounds": 12
        },
        timeout_minutes=60,
        allow_intervention=True,
        intervention_points=["after_pattern_detection"]
    ),

    category="operations",
    tags=["itops", "tickets", "analysis", "patterns", "operations"],
    estimated_time="15-30 minutes",
    cost_estimate="$1-3",

    examples=[
        {
            "name": "Database Performance Issues",
            "time_range": "Last 90 days",
            "focus_area": "Root Cause Analysis"
        },
        {
            "name": "Support Team Efficiency",
            "time_range": "Last 30 days",
            "focus_area": "Team Performance"
        }
    ],

    tips=[
        "Ensure tickets data has consistent format",
        "Include as much metadata as possible (timestamps, categories, etc.)",
        "Use Root Cause Analysis for recurring issues",
        "Use Predictive Analysis to forecast future ticket volume"
    ]
)

register_mode(itops_mode)
```

### Load All Modes

#### `backend/modes/__init__.py`
```python
"""
Mode definitions
Import all mode files to register them with the registry
"""

# Import modes to trigger registration
from . import research
from . import rfp_sow
from . import itops

# Import strategies to attach them to modes
from strategies import research_strategy
from strategies import rfp_strategy
from strategies import itops_strategy

print("✅ All modes loaded and registered")
```

---

## Phase 4: File Handling & Auto-Injection (Days 12-13)

### Goals
- ✅ File upload service
- ✅ Automatic path injection into agent context
- ✅ File download/preview
- ✅ Workspace management

### File Service

#### `backend/services/file_service.py`
```python
from typing import List, Dict, Any, Optional
from pathlib import Path
from fastapi import UploadFile
import aiofiles
import mimetypes
import uuid

from models.file import SessionFile
from core.config import settings

class FileService:
    """Manages file uploads and workspace files"""

    async def save_upload(
        self,
        session_id: str,
        file: UploadFile,
        is_input: bool = True
    ) -> SessionFile:
        """Save uploaded file to session workspace"""

        # Get workspace directory
        workspace_dir = settings.WORKSPACE_DIR / "sessions" / session_id
        target_dir = workspace_dir / ("input_files" if is_input else "outputs")
        target_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique filename
        file_ext = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path = target_dir / unique_filename

        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)

        # Get file info
        file_size = file_path.stat().st_size
        mime_type = mimetypes.guess_type(file.filename)[0]

        # Create database record
        session_file = SessionFile(
            session_id=session_id,
            filename=unique_filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_size=file_size,
            mime_type=mime_type,
            is_input=is_input
        )

        return session_file

    def get_file_context(self, files: List[SessionFile]) -> str:
        """Generate file context string for agent injection"""
        if not files:
            return ""

        context_parts = ["Available files:"]

        for file in files:
            context_parts.append(
                f"- {file.original_filename} (path: {file.file_path})"
            )

        context_parts.append("\nYou can reference these files by their paths in your analysis.")

        return "\n".join(context_parts)

    def get_file_metadata(self, files: List[SessionFile]) -> List[Dict[str, Any]]:
        """Get file metadata for engine input"""
        return [
            {
                "name": f.original_filename,
                "path": f.file_path,
                "size": f.file_size,
                "type": f.mime_type
            }
            for f in files
        ]

    async def list_output_files(self, session_id: str) -> List[Dict[str, Any]]:
        """List all output files from session"""
        output_dir = settings.WORKSPACE_DIR / "sessions" / session_id / "outputs"

        if not output_dir.exists():
            return []

        files = []
        for file_path in output_dir.rglob("*"):
            if file_path.is_file():
                files.append({
                    "name": file_path.name,
                    "path": str(file_path),
                    "size": file_path.stat().st_size,
                    "relative_path": str(file_path.relative_to(output_dir))
                })

        return files

    async def cleanup_session_files(self, session_id: str) -> None:
        """Cleanup all files for a session"""
        workspace_dir = settings.WORKSPACE_DIR / "sessions" / session_id

        if workspace_dir.exists():
            import shutil
            shutil.rmtree(workspace_dir)
```

### File Router

#### `backend/routers/files.py`
```python
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from services.file_service import FileService
from services.session_manager import SessionManager

router = APIRouter(tags=["files"])

@router.post("/sessions/{session_id}/upload")
async def upload_file(
    session_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Upload a file to session"""
    # Verify session exists
    session_manager = SessionManager(db)
    session = await session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Save file
    file_service = FileService()
    session_file = await file_service.save_upload(session_id, file, is_input=True)

    # Add to database
    db.add(session_file)
    await db.commit()
    await db.refresh(session_file)

    return {
        "id": session_file.id,
        "filename": session_file.original_filename,
        "size": session_file.file_size,
        "path": session_file.file_path
    }

@router.get("/sessions/{session_id}/files")
async def list_files(
    session_id: str,
    file_type: str = "all",  # "input", "output", "all"
    db: AsyncSession = Depends(get_db)
):
    """List files for session"""
    from sqlalchemy import select
    from models.file import SessionFile

    query = select(SessionFile).where(SessionFile.session_id == session_id)

    if file_type == "input":
        query = query.where(SessionFile.is_input == True)
    elif file_type == "output":
        query = query.where(SessionFile.is_input == False)

    result = await db.execute(query)
    files = result.scalars().all()

    return [
        {
            "id": f.id,
            "filename": f.original_filename,
            "size": f.file_size,
            "type": "input" if f.is_input else "output",
            "uploaded_at": f.uploaded_at.isoformat()
        }
        for f in files
    ]

@router.get("/sessions/{session_id}/files/{file_id}/download")
async def download_file(
    session_id: str,
    file_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Download a file"""
    from sqlalchemy import select
    from models.file import SessionFile

    result = await db.execute(
        select(SessionFile).where(
            SessionFile.id == file_id,
            SessionFile.session_id == session_id
        )
    )
    file = result.scalar_one_or_none()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file.file_path,
        filename=file.original_filename,
        media_type=file.mime_type
    )
```

---

## Phase 5: Streaming & Human-in-the-Loop (Days 14-16)

### Goals
- ✅ WebSocket streaming
- ✅ Real-time progress updates
- ✅ Human intervention capability
- ✅ Pause/resume functionality

### Streaming Service

#### `backend/services/streaming_service.py`
```python
from typing import Dict, Any, Optional, AsyncIterator
from fastapi import WebSocket
import asyncio
import json
from datetime import datetime

from services.session_manager import SessionManager
from engines import EngineRegistry
from core.enums import MessageRole

class StreamingService:
    """Manages WebSocket streaming and human intervention"""

    def __init__(self, websocket: WebSocket, session_manager: SessionManager):
        self.websocket = websocket
        self.session_manager = session_manager
        self.intervention_queue: asyncio.Queue = asyncio.Queue()
        self._paused = False

    async def send_event(self, event_type: str, data: Any):
        """Send event to client"""
        await self.websocket.send_json({
            "type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        })

    async def receive_intervention(self) -> Optional[Dict[str, Any]]:
        """Receive intervention from client (non-blocking)"""
        try:
            return await asyncio.wait_for(
                self.intervention_queue.get(),
                timeout=0.1
            )
        except asyncio.TimeoutError:
            return None

    async def handle_client_messages(self):
        """Background task to receive client messages"""
        try:
            while True:
                message = await self.websocket.receive_json()
                await self.intervention_queue.put(message)
        except Exception as e:
            print(f"Client disconnected: {e}")

    async def stream_execution(
        self,
        session_id: str,
        mode_id: str,
        input_data: Dict[str, Any],
        engine,
        mode_config: Dict[str, Any]
    ):
        """Stream execution with intervention support"""

        # Start client message handler
        asyncio.create_task(self.handle_client_messages())

        try:
            # Initialize engine
            workspace_dir = self.session_manager.get_workspace_dir(session_id)
            await engine.initialize(
                session_id=session_id,
                workspace_dir=str(workspace_dir),
                config=mode_config
            )

            await self.send_event("status", {
                "status": "running",
                "message": "Execution started"
            })

            # Stream execution
            async for output in engine.execute(
                task=input_data.get("task", ""),
                input_data=input_data,
                mode_config=mode_config
            ):
                # Send output to client
                await self.send_event("output", {
                    "status": output.status,
                    "content": output.content,
                    "artifacts": output.artifacts,
                    "metadata": output.metadata,
                    "cost_info": output.cost_info
                })

                # Save message to history
                await self.session_manager.add_message(
                    session_id=session_id,
                    role=MessageRole.ASSISTANT,
                    content=output.content,
                    metadata=output.metadata
                )

                # Check for interventions
                intervention = await self.receive_intervention()
                if intervention:
                    await self.handle_intervention(
                        intervention,
                        engine,
                        session_id
                    )

            # Execution completed
            await self.send_event("completed", {
                "message": "Execution completed successfully"
            })

        except Exception as e:
            await self.send_event("error", {
                "message": str(e)
            })
            raise

        finally:
            await engine.cleanup()

    async def handle_intervention(
        self,
        intervention: Dict[str, Any],
        engine,
        session_id: str
    ):
        """Handle human intervention"""
        intervention_type = intervention.get("type")

        if intervention_type == "pause":
            # Pause execution
            checkpoint = await engine.pause()
            await self.session_manager.save_checkpoint(session_id, checkpoint)
            await self.session_manager.update_status(session_id, "paused")
            await self.send_event("paused", {"checkpoint_saved": True})
            self._paused = True

            # Wait for resume
            while self._paused:
                msg = await self.receive_intervention()
                if msg and msg.get("type") == "resume":
                    await engine.resume(checkpoint)
                    await self.session_manager.update_status(session_id, "running")
                    await self.send_event("resumed", {})
                    self._paused = False
                await asyncio.sleep(0.5)

        elif intervention_type == "redirect":
            # Redirect to different agent/strategy
            await engine.intervene(intervention)
            await self.send_event("intervention_applied", {
                "type": "redirect",
                "message": "Execution redirected"
            })

        elif intervention_type == "modify":
            # Modify parameters/inputs
            await engine.intervene(intervention)
            await self.send_event("intervention_applied", {
                "type": "modify",
                "message": "Parameters modified"
            })

        elif intervention_type == "cancel":
            # Cancel execution
            await self.session_manager.update_status(session_id, "cancelled")
            await self.send_event("cancelled", {})
            raise Exception("Execution cancelled by user")
```

### Streaming Router

#### `backend/routers/streaming.py`
```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.mode_registry import ModeRegistry
from engines import EngineRegistry
from services.session_manager import SessionManager
from services.streaming_service import StreamingService
from services.file_service import FileService

router = APIRouter(tags=["streaming"])

@router.websocket("/ws/execute/{session_id}")
async def websocket_execute(
    websocket: WebSocket,
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """WebSocket endpoint for streaming execution"""
    await websocket.accept()

    try:
        # Get session
        session_manager = SessionManager(db)
        session = await session_manager.get_session(session_id)

        if not session:
            await websocket.send_json({
                "type": "error",
                "data": {"message": "Session not found"}
            })
            await websocket.close()
            return

        # Get mode
        mode = ModeRegistry.get(session.mode_id)
        if not mode:
            await websocket.send_json({
                "type": "error",
                "data": {"message": "Mode not found"}
            })
            await websocket.close()
            return

        # Get engine
        engine = EngineRegistry.get_engine(mode.engine)

        # Get files and inject context
        from sqlalchemy import select
        from models.file import SessionFile

        result = await db.execute(
            select(SessionFile).where(
                SessionFile.session_id == session_id,
                SessionFile.is_input == True
            )
        )
        files = result.scalars().all()

        file_service = FileService()
        file_context = file_service.get_file_context(files)

        # Augment input data with file context
        input_data = session.input_data or {}
        if file_context:
            input_data["file_context"] = file_context
            input_data["uploaded_files"] = file_service.get_file_metadata(files)

        # Create streaming service
        streaming_service = StreamingService(websocket, session_manager)

        # Update session status
        await session_manager.update_status(session_id, "running")

        # Stream execution
        await streaming_service.stream_execution(
            session_id=session_id,
            mode_id=mode.id,
            input_data=input_data,
            engine=engine,
            mode_config=mode.config.engine_config
        )

        # Mark as completed
        await session_manager.update_status(session_id, "completed")

    except WebSocketDisconnect:
        print(f"Client disconnected from session {session_id}")
    except Exception as e:
        print(f"Error in streaming execution: {e}")
        await session_manager.update_status(session_id, "failed", str(e))
        try:
            await websocket.send_json({
                "type": "error",
                "data": {"message": str(e)}
            })
        except:
            pass
    finally:
        try:
            await websocket.close()
        except:
            pass
```

---

## Phase 6: Config Management (Days 17-18)

### Goals
- ✅ UI for uploading API keys
- ✅ Credentials management
- ✅ YAML config upload
- ✅ Secure storage

### Config Service

#### `backend/services/config_service.py`
```python
from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import yaml
import json
from pathlib import Path

from models.config import UserConfig
from core.config import settings

class ConfigService:
    """Manages user configurations and credentials"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_api_key(
        self,
        provider: str,
        api_key: str
    ) -> UserConfig:
        """Save API key for provider"""
        # Check if exists
        result = await self.db.execute(
            select(UserConfig).where(
                UserConfig.config_type == "api_key",
                UserConfig.config_name == provider
            )
        )
        config = result.scalar_one_or_none()

        if config:
            # Update existing
            config.config_value = api_key
            config.is_active = True
        else:
            # Create new
            config = UserConfig(
                config_type="api_key",
                config_name=provider,
                config_value=api_key,
                is_active=True
            )
            self.db.add(config)

        await self.db.commit()
        await self.db.refresh(config)

        # Save to file for engines to use
        self._save_to_env_file(provider, api_key)

        return config

    async def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key for provider"""
        result = await self.db.execute(
            select(UserConfig).where(
                UserConfig.config_type == "api_key",
                UserConfig.config_name == provider,
                UserConfig.is_active == True
            )
        )
        config = result.scalar_one_or_none()
        return config.config_value if config else None

    async def save_yaml_config(
        self,
        config_name: str,
        yaml_content: str
    ) -> UserConfig:
        """Save YAML configuration"""
        # Validate YAML
        try:
            yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML: {e}")

        # Save to database
        config = UserConfig(
            config_type="yaml",
            config_name=config_name,
            config_value=yaml_content,
            is_active=True
        )
        self.db.add(config)
        await self.db.commit()
        await self.db.refresh(config)

        # Save to file
        config_path = settings.CONFIGS_DIR / f"{config_name}.yaml"
        with open(config_path, 'w') as f:
            f.write(yaml_content)

        return config

    async def list_configs(
        self,
        config_type: Optional[str] = None
    ) -> List[UserConfig]:
        """List all configurations"""
        query = select(UserConfig).where(UserConfig.is_active == True)

        if config_type:
            query = query.where(UserConfig.config_type == config_type)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def delete_config(self, config_id: str) -> None:
        """Delete configuration"""
        result = await self.db.execute(
            select(UserConfig).where(UserConfig.id == config_id)
        )
        config = result.scalar_one_or_none()

        if config:
            config.is_active = False
            await self.db.commit()

    def _save_to_env_file(self, provider: str, api_key: str):
        """Save API key to .env file for engines"""
        env_file = Path(".env")

        # Read existing content
        if env_file.exists():
            with open(env_file, 'r') as f:
                lines = f.readlines()
        else:
            lines = []

        # Update or add key
        key_name = f"{provider.upper()}_API_KEY"
        key_line = f"{key_name}={api_key}\n"

        found = False
        for i, line in enumerate(lines):
            if line.startswith(f"{key_name}="):
                lines[i] = key_line
                found = True
                break

        if not found:
            lines.append(key_line)

        # Write back
        with open(env_file, 'w') as f:
            f.writelines(lines)
```

### Config Router

#### `backend/routers/config.py`
```python
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List

from core.database import get_db
from services.config_service import ConfigService

router = APIRouter(tags=["config"])

class APIKeyRequest(BaseModel):
    provider: str  # "openai", "anthropic", "google"
    api_key: str

class ConfigResponse(BaseModel):
    id: str
    type: str
    name: str
    created_at: str

@router.post("/config/api-keys")
async def save_api_key(
    request: APIKeyRequest,
    db: AsyncSession = Depends(get_db)
):
    """Save API key"""
    config_service = ConfigService(db)
    config = await config_service.save_api_key(
        provider=request.provider,
        api_key=request.api_key
    )

    return {
        "id": config.id,
        "provider": config.config_name,
        "saved": True
    }

@router.get("/config/api-keys")
async def list_api_keys(db: AsyncSession = Depends(get_db)):
    """List configured API keys (without exposing actual keys)"""
    config_service = ConfigService(db)
    configs = await config_service.list_configs(config_type="api_key")

    return [
        {
            "id": c.id,
            "provider": c.config_name,
            "configured": True,
            "created_at": c.created_at.isoformat()
        }
        for c in configs
    ]

@router.post("/config/yaml")
async def upload_yaml_config(
    name: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Upload YAML configuration"""
    content = await file.read()
    yaml_content = content.decode('utf-8')

    config_service = ConfigService(db)
    config = await config_service.save_yaml_config(
        config_name=name,
        yaml_content=yaml_content
    )

    return {
        "id": config.id,
        "name": config.config_name,
        "saved": True
    }

@router.get("/config/yamls")
async def list_yaml_configs(db: AsyncSession = Depends(get_db)):
    """List YAML configurations"""
    config_service = ConfigService(db)
    configs = await config_service.list_configs(config_type="yaml")

    return [
        {
            "id": c.id,
            "name": c.config_name,
            "created_at": c.created_at.isoformat()
        }
        for c in configs
    ]

@router.delete("/config/{config_id}")
async def delete_config(
    config_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete configuration"""
    config_service = ConfigService(db)
    await config_service.delete_config(config_id)

    return {"deleted": True}
```

---

## Phase 7: Frontend Implementation (Days 19-24)

### Goals
- ✅ Mode selector UI
- ✅ Execution interface with streaming
- ✅ File upload/download
- ✅ Config management UI
- ✅ Session dashboard
- ✅ Cost tracker
- ✅ Intervention controls

### Key Components

#### `frontend/components/ModeSelector.tsx`
```typescript
'use client';

import { useEffect, useState } from 'react';
import { Mode } from '@/lib/types';
import { api } from '@/lib/api';
import ModeCard from './ModeCard';

export default function ModeSelector() {
  const [modes, setModes] = useState<Mode[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all');

  useEffect(() => {
    loadModes();
  }, []);

  const loadModes = async () => {
    try {
      const response = await api.get('/modes');
      setModes(response.data);
    } catch (error) {
      console.error('Failed to load modes:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredModes = filter === 'all'
    ? modes
    : modes.filter(m => m.engine === filter);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-4">Select a Mode</h1>
        <p className="text-gray-600 mb-6">
          Choose a task mode to get started with TOMAS
        </p>

        {/* Filter */}
        <div className="flex gap-4">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded ${
              filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-200'
            }`}
          >
            All Modes
          </button>
          <button
            onClick={() => setFilter('cmbagent')}
            className={`px-4 py-2 rounded ${
              filter === 'cmbagent' ? 'bg-blue-600 text-white' : 'bg-gray-200'
            }`}
          >
            CMBAgent
          </button>
          <button
            onClick={() => setFilter('denario')}
            className={`px-4 py-2 rounded ${
              filter === 'denario' ? 'bg-blue-600 text-white' : 'bg-gray-200'
            }`}
          >
            Denario
          </button>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">Loading modes...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredModes.map(mode => (
            <ModeCard key={mode.id} mode={mode} />
          ))}
        </div>
      )}
    </div>
  );
}
```

#### `frontend/components/ExecutionInterface.tsx`
```typescript
'use client';

import { useState, useEffect, useRef } from 'react';
import { Mode, Session, StreamEvent } from '@/lib/types';
import { api } from '@/lib/api';
import FileUpload from './FileUpload';
import StreamingDisplay from './StreamingDisplay';
import InterventionPanel from './InterventionPanel';
import CostTracker from './CostTracker';

interface Props {
  mode: Mode;
  sessionId?: string;
}

export default function ExecutionInterface({ mode, sessionId }: Props) {
  const [session, setSession] = useState<Session | null>(null);
  const [inputs, setInputs] = useState<Record<string, any>>({});
  const [files, setFiles] = useState<File[]>([]);
  const [executing, setExecuting] = useState(false);
  const [events, setEvents] = useState<StreamEvent[]>([]);
  const [totalCost, setTotalCost] = useState(0);

  const wsRef = useRef<WebSocket | null>(null);

  const handleInputChange = (name: string, value: any) => {
    setInputs(prev => ({ ...prev, [name]: value }));
  };

  const handleFileUpload = (uploadedFiles: File[]) => {
    setFiles(prev => [...prev, ...uploadedFiles]);
  };

  const startExecution = async () => {
    try {
      setExecuting(true);
      setEvents([]);

      // Create session
      const sessionResponse = await api.post('/sessions', {
        mode_id: mode.id,
        input_data: inputs
      });

      const newSession = sessionResponse.data;
      setSession(newSession);

      // Upload files
      for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);
        await api.post(`/sessions/${newSession.id}/upload`, formData);
      }

      // Connect WebSocket
      connectWebSocket(newSession.id);

    } catch (error) {
      console.error('Failed to start execution:', error);
      setExecuting(false);
    }
  };

  const connectWebSocket = (sessionId: string) => {
    const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL}/ws/execute/${sessionId}`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      setEvents(prev => [...prev, data]);

      if (data.type === 'output' && data.data.cost_info) {
        setTotalCost(prev => prev + (data.data.cost_info.cost_usd || 0));
      }

      if (data.type === 'completed' || data.type === 'error') {
        setExecuting(false);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setExecuting(false);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setExecuting(false);
    };

    wsRef.current = ws;
  };

  const sendIntervention = (intervention: any) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(intervention));
    }
  };

  const pauseExecution = () => {
    sendIntervention({ type: 'pause' });
  };

  const resumeExecution = () => {
    sendIntervention({ type: 'resume' });
  };

  const cancelExecution = () => {
    sendIntervention({ type: 'cancel' });
    if (wsRef.current) {
      wsRef.current.close();
    }
  };

  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">{mode.icon} {mode.name}</h1>
        <p className="text-gray-600">{mode.description}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left: Inputs */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Inputs</h2>

            {mode.inputs.map(input => (
              <div key={input.name} className="mb-4">
                <label className="block text-sm font-medium mb-2">
                  {input.label}
                  {input.required && <span className="text-red-500">*</span>}
                </label>

                {input.type === 'text' && (
                  <input
                    type="text"
                    className="w-full px-3 py-2 border rounded"
                    placeholder={input.placeholder}
                    value={inputs[input.name] || ''}
                    onChange={(e) => handleInputChange(input.name, e.target.value)}
                  />
                )}

                {input.type === 'textarea' && (
                  <textarea
                    className="w-full px-3 py-2 border rounded"
                    rows={4}
                    placeholder={input.placeholder}
                    value={inputs[input.name] || ''}
                    onChange={(e) => handleInputChange(input.name, e.target.value)}
                  />
                )}

                {input.type === 'select' && (
                  <select
                    className="w-full px-3 py-2 border rounded"
                    value={inputs[input.name] || ''}
                    onChange={(e) => handleInputChange(input.name, e.target.value)}
                  >
                    <option value="">Select...</option>
                    {input.options?.map(opt => (
                      <option key={opt} value={opt}>{opt}</option>
                    ))}
                  </select>
                )}

                {input.type === 'file' && (
                  <FileUpload
                    accept={input.accept}
                    onUpload={handleFileUpload}
                  />
                )}

                {input.help_text && (
                  <p className="text-sm text-gray-500 mt-1">{input.help_text}</p>
                )}
              </div>
            ))}

            <button
              onClick={startExecution}
              disabled={executing}
              className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
            >
              {executing ? 'Executing...' : 'Start Execution'}
            </button>
          </div>

          <CostTracker totalCost={totalCost} estimatedCost={mode.cost_estimate} />
        </div>

        {/* Right: Execution Display */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Execution</h2>

              {executing && (
                <InterventionPanel
                  onPause={pauseExecution}
                  onResume={resumeExecution}
                  onCancel={cancelExecution}
                  onIntervene={sendIntervention}
                />
              )}
            </div>

            <StreamingDisplay events={events} />
          </div>
        </div>
      </div>
    </div>
  );
}
```

*(Additional component implementations for FileUpload, StreamingDisplay, InterventionPanel, CostTracker, ConfigManager, etc. would be similar in structure)*

---

## Phase 8: Testing & Polish (Days 25-28)

### Goals
- ✅ End-to-end testing
- ✅ Fix bugs
- ✅ UI/UX polish
- ✅ Documentation
- ✅ Performance optimization

### Testing Checklist

**Backend Testing:**
- [ ] Database operations (CRUD for all models)
- [ ] Session lifecycle (create, start, pause, resume, complete)
- [ ] File upload/download
- [ ] Cost tracking
- [ ] WebSocket streaming
- [ ] API endpoint responses
- [ ] Error handling

**Engine Testing:**
- [ ] CMBAgent execution
- [ ] Denario execution
- [ ] File path injection
- [ ] Output normalization
- [ ] Pause/resume
- [ ] Intervention handling

**Frontend Testing:**
- [ ] Mode selection
- [ ] Form validation
- [ ] File upload UI
- [ ] Real-time streaming display
- [ ] Intervention controls
- [ ] Cost display
- [ ] Session history
- [ ] Config management UI

**End-to-End Testing:**
- [ ] Research mode (Denario): data → idea → results → paper
- [ ] RFP mode (CMBAgent): document → analysis → architecture → cost
- [ ] ITOps mode (CMBAgent): tickets → patterns → insights → recommendations
- [ ] Human intervention during execution
- [ ] Pause and resume
- [ ] Multiple concurrent sessions

---

## 🚀 Deployment & Production

### Docker Setup

#### `docker-compose.yml`
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///./tomas.db
      - WORKSPACE_DIR=/workspace
      - CONFIGS_DIR=/configs
    volumes:
      - ./workspace:/workspace
      - ./configs:/configs
      - ./backend:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - NEXT_PUBLIC_WS_URL=ws://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
    command: npm run dev
```

#### `backend/Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### `frontend/Dockerfile`
```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "run", "dev"]
```

---

## 📊 Success Metrics

### MVP Completion Criteria

1. ✅ **All 3 Priority Modes Working**
   - Research mode completes end-to-end
   - RFP/SOW mode generates architecture and cost estimates
   - ITOps mode analyzes tickets and provides insights

2. ✅ **File Handling**
   - Upload works for all supported file types
   - Files automatically injected into agent context
   - Download works for all outputs

3. ✅ **Human-in-the-Loop**
   - Real-time streaming works
   - Pause/resume functional
   - Intervention during execution works

4. ✅ **Config Management**
   - API keys can be uploaded via UI
   - YAML configs can be uploaded
   - Configs persist across sessions

5. ✅ **UI/UX**
   - Clean, intuitive interface
   - Real-time updates
   - Cost tracking visible
   - Error messages user-friendly

6. ✅ **Session Management**
   - Sessions saved to SQLite
   - Conversation history complete
   - Sessions can be resumed

7. ✅ **Cost Tracking**
   - Token usage tracked
   - Costs calculated
   - Displayed in real-time

---

## 🔮 Post-MVP Roadmap

### Phase 2 Features (Post-MVP)
- **RAG Integration**: Vector database for client endpoints
- **MCP Integration**: Model Context Protocol support
- **Advanced Guardrails**: Input validation, output verification
- **More Modes**: Handbook, DevOps, Data Analysis, Clinical Trials
- **Multi-tenancy**: User accounts and authentication
- **Advanced Analytics**: Usage patterns, performance metrics
- **Caching Layer**: Redis for better performance
- **Kubernetes**: Container orchestration
- **Monitoring**: Prometheus + Grafana
- **CI/CD Pipeline**: Automated testing and deployment

---

## 📝 Developer Notes

### Key Architectural Decisions

1. **Equal Engine Weightage**: Both CMBAgent and Denario are first-class engines
2. **Mode-Centric Design**: Modes define which engine to use
3. **File Auto-Injection**: System handles file paths transparently
4. **Human-in-the-Loop**: Built-in intervention capability
5. **Cost-First**: Track and display costs throughout
6. **Session-Based**: Everything is session-scoped
7. **Extensible**: Easy to add new engines and modes

### Common Patterns

**Creating a New Mode:**
1. Define mode in `backend/modes/your_mode.py`
2. Create strategy in `backend/strategies/your_strategy.py`
3. Import in `backend/modes/__init__.py`
4. Restart backend - UI updates automatically

**Adding a New Engine:**
1. Implement `IEngine` interface in `backend/engines/your_engine.py`
2. Register in `backend/engines/__init__.py`
3. Update `EngineType` enum
4. Create modes that use the new engine

### Performance Tips

- Use LangGraph backend for Denario when speed > thoroughness
- Implement caching for repeated operations
- Use background tasks for long-running operations
- Optimize database queries with indexes
- Compress large file uploads

---

## 🎉 Getting Started

### Quick Start

1. **Clone and setup:**
```bash
git clone <repo-url>
cd TOMAS
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys
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
alembic upgrade head
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
- WebSocket: ws://localhost:8000

---

## 📚 Additional Resources

- [Backend API Documentation](backend/README.md)
- [Frontend Component Guide](frontend/README.md)
- [Engine Development Guide](docs/engines.md)
- [Mode Development Guide](docs/modes.md)
- [Deployment Guide](docs/deployment.md)

---

**Built with ❤️ for production-ready multi-agent systems**

**Engines:** CMBAgent | Denario | (Kosmos - Coming Soon)
**Framework:** FastAPI + Next.js + SQLAlchemy
**Focus:** Task-Oriented | Human-in-the-Loop | Cost-Conscious
