# TOMAS Backend

FastAPI-based backend for the Task-Oriented Multi-Agent System.

## Architecture

```
FastAPI Gateway
    ↓
Mode Executor
    ↓
Denario (local copy)
    ↓
CMBAgent (local copy)
    ↓
LangGraph + Planning & Control
```

## Local Dependencies

### Why Local Copies?

Instead of installing Denario and CMBAgent as packages, we copied them directly into the backend:

**Benefits:**
- ✅ No external dependency issues
- ✅ Full control over the code
- ✅ Easy to debug and customize
- ✅ No version conflicts
- ✅ Can modify as needed

**Structure:**
```
backend/
├── denario/           # Complete Denario source
├── cmbagent/          # Complete CMBAgent source
├── core/              # TOMAS core
├── modes/             # Mode definitions
├── strategies/        # Execution strategies
├── services/          # Service layer
└── routers/           # API routes
```

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example ../.env
nano ../.env  # Add API keys

# Start server
python main.py
```

## API Endpoints

### Health Check
```bash
GET /health
```

### List Modes
```bash
GET /api/modes

Response:
{
  "modes": [...],
  "count": 3
}
```

### Get Mode Details
```bash
GET /api/modes/{mode_id}

Response:
{
  "id": "research",
  "name": "Scientific Research",
  "inputs": [...],
  "outputs": [...]
}
```

### Execute Mode
```bash
POST /api/execute
Content-Type: multipart/form-data

Fields:
- mode_id: string
- input_data: JSON string
- files: file[] (optional)

Response:
{
  "task_id": "uuid",
  "session_id": "uuid",
  "status": "queued"
}
```

### Get Task Status
```bash
GET /api/tasks/{task_id}/status

Response:
{
  "task_id": "uuid",
  "status": "executing",
  "progress": 45,
  "error": null
}
```

### Get Task Results
```bash
GET /api/tasks/{task_id}/results

Response:
{
  "task_id": "uuid",
  "result": {...}
}
```

## Adding a New Mode

### 1. Create Mode Definition

`modes/my_mode.py`:
```python
from core.mode import AgentMode, InputField, OutputType, InputFieldType
from core.mode_registry import registry

my_mode = AgentMode(
    id="my_mode",
    name="My Mode",
    description="Description",
    category="analysis",
    icon="Icon",
    inputs=[
        InputField(
            name="input1",
            type=InputFieldType.TEXT,
            label="Input 1",
            required=True
        )
    ],
    outputs=[
        OutputType(
            name="output1",
            type="document",
            format="md",
            description="Output description"
        )
    ],
    endpoint_path="/api/my-mode"
)

registry.register(my_mode)
```

### 2. Create Execution Strategy

`strategies/my_strategy.py`:
```python
def execute_my_mode(denario, input_data, mode_config):
    # Extract inputs
    input1 = input_data.get("input1")
    
    # Use Denario workflow
    denario.set_data_description(input1)
    denario.get_idea()
    denario.get_method()
    denario.get_results()
    
    return {
        "status": "success",
        "output1": denario.research.results
    }

from core.mode_registry import registry
mode = registry.get("my_mode")
if mode:
    mode.strategy = execute_my_mode
```

### 3. Register Mode

`modes/__init__.py`:
```python
from . import research
from . import rfp_sow
from . import itops
from . import my_mode  # Add this

from strategies import research_strategy
from strategies import rfp_strategy
from strategies import itops_strategy
from strategies import my_strategy  # Add this
```

### 4. Restart Backend

```bash
python main.py
```

Mode appears automatically in:
- API `/api/modes`
- Frontend UI
- API documentation

## Development

### Running with Auto-Reload

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Run backend test script
../test_backend.sh

# Or manual tests
curl http://localhost:8000/health
curl http://localhost:8000/api/modes
```

### Debugging

Enable debug logging in `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Configuration

Environment variables (`.env`):

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Server
HOST=0.0.0.0
PORT=8000

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Workspace
WORKSPACE_DIR=./workspaces
```

## Directory Structure

```
backend/
├── denario/              # Denario source (local)
│   ├── __init__.py
│   ├── denario.py
│   ├── key_manager.py
│   ├── llm.py
│   ├── research.py
│   └── ...
│
├── cmbagent/             # CMBAgent source (local)
│   ├── __init__.py
│   ├── base_agent.py
│   ├── cmbagent.py
│   └── ...
│
├── core/                 # TOMAS core
│   ├── mode.py          # Mode abstraction
│   ├── mode_registry.py # Registry
│   └── config.py        # Settings
│
├── modes/                # Mode definitions
│   ├── research.py      # Research mode
│   ├── rfp_sow.py       # RFP/SOW mode
│   └── itops.py         # ITOps mode
│
├── strategies/           # Execution strategies
│   ├── research_strategy.py
│   ├── rfp_strategy.py
│   └── itops_strategy.py
│
├── services/             # Service layer
│   ├── denario_service.py    # Denario wrapper
│   └── mode_executor.py      # Mode executor
│
├── routers/              # API routes
│   ├── modes.py         # Mode endpoints
│   └── execution.py     # Execution endpoints
│
├── main.py              # FastAPI app
└── requirements.txt     # Dependencies
```

## Dependencies

See `requirements.txt` for full list. Key dependencies:

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **LangChain** - LLM framework
- **LangGraph** - Graph orchestration
- **CMBAgent Autogen** - Agent framework

All Denario and CMBAgent dependencies are included.

## Troubleshooting

### Import Errors

If you see import errors for `denario` or `cmbagent`:
```bash
# Ensure you're in the backend directory
cd backend
python -c "import denario; print('OK')"
python -c "import cmbagent; print('OK')"
```

### API Key Errors

Check environment:
```bash
source venv/bin/activate
python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
```

### Port Issues

Change port in `.env` or:
```bash
python main.py --port 8001
```

## Production Deployment

### Using Gunicorn

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker

```bash
docker build -t tomas-backend .
docker run -p 8000:8000 --env-file .env tomas-backend
```

### Environment

- Set proper `CORS_ORIGINS`
- Use production-grade database for task storage
- Add authentication
- Enable logging
- Use cloud storage for files

## License

See LICENSE file.
