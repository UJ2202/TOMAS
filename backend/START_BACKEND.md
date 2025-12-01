# Starting the Backend

## Prerequisites

1. Python 3.12+ installed
2. Denario installed at `../Denario`
3. API keys configured in `.env` file

## Setup

### 1. Copy Environment File

```bash
cd /home/g22yash_tiwari/MAS/agent-platform
cp .env.example .env
```

Edit `.env` and add your API keys:
```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
GOOGLE_API_KEY=...
```

### 2. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run Backend

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload
```

## Verify

- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/health

## Test Research Mode

```bash
curl http://localhost:8000/api/modes
```

Should return the registered research mode.

## Troubleshooting

### Denario Not Found

If you get "ModuleNotFoundError: No module named 'denario'":

1. Check Denario path in `services/denario_service.py`
2. Ensure Denario is at `../Denario` relative to backend folder
3. Or install Denario: `pip install -e ../Denario`

### API Keys Not Loaded

If you get warnings about API keys:

1. Ensure `.env` file exists in project root
2. Check API key format (no spaces, no quotes)
3. Restart backend after updating `.env`

## Docker

Alternatively, use Docker:

```bash
cd /home/g22yash_tiwari/MAS/agent-platform
docker-compose up backend
```
