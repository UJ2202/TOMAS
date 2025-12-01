# 🚀 TOMAS Quick Start Guide

Get TOMAS up and running in 5 minutes!

## Prerequisites

- Python 3.12+
- Node.js 18+ (optional, for frontend)
- API Keys (at least OpenAI)

## Step 1: Clone and Setup

```bash
cd /Users/ujjwal.tiwari/uj/MAS/TOMAS

# Run setup script
./setup.sh
```

This will:
- Create Python virtual environment
- Install all backend dependencies (including local Denario & CMBAgent)
- Install frontend dependencies (if Node.js available)
- Create .env file from template

## Step 2: Configure API Keys

Edit the `.env` file with your API keys:

```bash
nano .env
```

**Minimum required:**
```bash
OPENAI_API_KEY=sk-your-key-here
```

**Optional (for other models):**
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_API_KEY=your-google-key
```

## Step 3: Start Backend

```bash
cd backend
source venv/bin/activate
python main.py
```

You should see:
```
✅ DenarioService initialized
✅ Registered mode: research - Scientific Research
✅ Registered mode: rfp_sow - RFP/SOW Intelligence
✅ Registered mode: itops - ITOps Ticket Analysis
✅ All modes loaded and registered
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test it:**
```bash
# In a new terminal
curl http://localhost:8000/health
curl http://localhost:8000/api/modes
```

Or open: http://localhost:8000/api/docs

## Step 4: Start Frontend (Optional)

In a new terminal:

```bash
cd frontend
npm run dev
```

Open: http://localhost:3000

## Step 5: Test Execution

### Option A: Using the UI

1. Go to http://localhost:3000
2. Select a mode (e.g., Research)
3. Fill in the form
4. Click "Execute Mode"
5. Monitor progress
6. View results

### Option B: Using API

```bash
# Test research mode
curl -X POST "http://localhost:8000/api/execute" \
  -F "mode_id=research" \
  -F 'input_data={"data_description":"Analyze time series data using Python pandas and matplotlib. Data is in CSV format with timestamp and value columns.","mode":"fast","llm":"gpt-4o","iterations":"2"}'

# Get the task_id from response, then check status:
curl http://localhost:8000/api/tasks/{task_id}/status

# When complete, get results:
curl http://localhost:8000/api/tasks/{task_id}/results
```

## Testing

Run the test script to verify everything works:

```bash
./test_backend.sh
```

## Common Issues

### Issue: "Denario module not found"
**Solution:** Denario is now copied locally in `backend/denario/`. Just install requirements:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "API keys not loading"
**Solution:** Check `.env` file format:
```bash
cat .env
# Should show: OPENAI_API_KEY=sk-...
# No quotes, no spaces around =
```

### Issue: "Port 8000 already in use"
**Solution:** Kill existing process:
```bash
lsof -ti:8000 | xargs kill -9
```

Or change port in `.env`:
```bash
PORT=8001
```

### Issue: Frontend won't start
**Solution:** 
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## What's Next?

### Add Your Own Mode

1. Create mode definition: `backend/modes/my_mode.py`
2. Create strategy: `backend/strategies/my_strategy.py`
3. Import in `backend/modes/__init__.py`
4. Restart backend - mode appears automatically!

See [README.md](README.md) for detailed instructions.

### Customize Existing Modes

Edit mode files in `backend/modes/`:
- `research.py` - Research mode configuration
- `rfp_sow.py` - RFP/SOW mode configuration
- `itops.py` - ITOps mode configuration

Edit strategies in `backend/strategies/`:
- `research_strategy.py` - How research mode uses Denario
- `rfp_strategy.py` - How RFP mode uses Denario
- `itops_strategy.py` - How ITOps mode uses Denario

### Deploy to Production

See [README.md](README.md) deployment section.

## Architecture

```
User → Next.js UI → FastAPI Gateway → Mode Executor → Denario → CMBAgent → Results
                                          ↓
                                    Local Denario
                                    Local CMBAgent
```

## Available Modes

1. **🔬 Research** - Scientific research workflow
2. **📄 RFP/SOW** - Cloud architecture proposals
3. **🎫 ITOps** - Ticket analysis and insights

## Quick Reference

### Backend Commands
```bash
cd backend
source venv/bin/activate
python main.py                    # Start backend
python main.py --reload           # Start with auto-reload
```

### Frontend Commands
```bash
cd frontend
npm run dev                       # Development mode
npm run build                     # Production build
npm start                         # Run production build
```

### API Endpoints
- `GET /health` - Health check
- `GET /api/modes` - List all modes
- `GET /api/modes/{id}` - Mode details
- `POST /api/execute` - Execute mode
- `GET /api/tasks/{id}/status` - Task status
- `GET /api/tasks/{id}/results` - Task results

## Need Help?

1. Check [README.md](README.md) for detailed documentation
2. Check [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for architecture details
3. Check backend logs for error messages
4. Run `./test_backend.sh` to diagnose issues

## Success Checklist

- [ ] Setup script completed without errors
- [ ] .env file configured with API keys
- [ ] Backend starts and shows all 3 modes registered
- [ ] Health check returns success
- [ ] `/api/modes` returns 3 modes
- [ ] Frontend loads (if using UI)
- [ ] Can execute a test task
- [ ] Task completes and returns results

🎉 **You're all set! Start building amazing multi-agent workflows!**
