from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn

from core.config import settings
from services.denario_service import DenarioService
from services.mode_executor import ModeExecutor
from routers import modes, execution

# Import mode definitions to register them
import modes as mode_definitions

# Initialize services
denario_service = DenarioService(workspace_dir=settings.WORKSPACE_DIR)
mode_executor = ModeExecutor(denario_service)

# Create FastAPI app
app = FastAPI(
    title="Agent Platform API",
    description="Multi-agent system with task-specific modes",
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

# Include routers
app.include_router(modes.router, prefix="/api")
app.include_router(execution.router, prefix="/api")

# Make services available to routers
app.state.denario_service = denario_service
app.state.mode_executor = mode_executor

@app.get("/")
def root():
    return {
        "message": "Agent Platform API",
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
