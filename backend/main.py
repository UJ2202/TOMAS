from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn

from core.config import settings
from routers import modes, execution

# Create FastAPI app
app = FastAPI(
    title="TOMAS - Task-Oriented Multi-Agent System",
    description="Multi-agent system with CMBAgent and Denario engines",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for downloads
workspace_path = Path(settings.WORKSPACE_DIR)
workspace_path.mkdir(exist_ok=True)
# app.mount("/files", StaticFiles(directory=str(workspace_path)), name="files")

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    # Import mode definitions to register them with ModeRegistry
    import modes as mode_definitions

    # Create workspace directories
    (workspace_path / "sessions").mkdir(exist_ok=True)
    (workspace_path / "temp").mkdir(exist_ok=True)

    print(f"✅ TOMAS initialized with workspace: {workspace_path}")

# Include routers
app.include_router(modes.router, prefix="/api")
app.include_router(execution.router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "TOMAS - Task-Oriented Multi-Agent System",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
