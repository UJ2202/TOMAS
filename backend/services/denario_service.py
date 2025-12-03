import sys
from pathlib import Path
import uuid
from typing import Optional
import os

# Import Denario from local copy
try:
    from denario import Denario
    from denario.key_manager import KeyManager
    DENARIO_AVAILABLE = True
except ImportError:
    DENARIO_AVAILABLE = False
    print("⚠️ Denario not available - running in mock mode")

class DenarioService:
    """Service layer for Denario integration"""

    def __init__(self, workspace_dir: str = "./workspaces"):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)
        self.key_manager = None

        # Initialize API keys from environment
        if DENARIO_AVAILABLE:
            try:
                self.key_manager = KeyManager()
                self.key_manager.get_keys_from_env()

                # Debug: Check which keys are loaded
                keys_status = []
                if self.key_manager.OPENAI:
                    keys_status.append(f"OpenAI: {self.key_manager.OPENAI[:10]}...")
                if self.key_manager.GEMINI:
                    keys_status.append(f"Gemini: {self.key_manager.GEMINI[:10]}...")
                if self.key_manager.ANTHROPIC:
                    keys_status.append(f"Anthropic: {self.key_manager.ANTHROPIC[:10]}...")

                print(f"✅ DenarioService initialized (workspace: {workspace_dir})")
                print(f"🔑 API Keys loaded: {', '.join(keys_status) if keys_status else 'None'}")
            except Exception as e:
                print(f"⚠️  Warning: Could not load API keys: {e}")
        else:
            print(f"✅ DenarioService initialized in mock mode (workspace: {workspace_dir})")

    def create_session(self) -> str:
        """Create a new session with unique ID"""
        session_id = str(uuid.uuid4())
        session_dir = self.workspace_dir / session_id
        session_dir.mkdir(exist_ok=True)
        return session_id

    def get_denario_instance(self, session_id: str):
        """Get Denario instance for a session"""
        project_dir = str(self.workspace_dir / session_id)
        if DENARIO_AVAILABLE:
            return Denario(project_dir=project_dir)
        else:
            return MockDenario(project_dir=project_dir)

    def get_session_dir(self, session_id: str) -> Path:
        """Get session directory path"""
        return self.workspace_dir / session_id

    def get_key_manager(self):
        """Get the key manager instance"""
        return self.key_manager


class MockDenario:
    """Mock Denario for testing without actual Denario installation"""
    
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.research = MockResearch()
        
    def set_data_description(self, desc):
        self.research.data_description = desc
        
    def get_idea(self, **kwargs):
        self.research.idea = "Mock research idea generated"
        
    def get_method(self, **kwargs):
        self.research.methodology = "Mock methodology generated"
        
    def get_results(self, **kwargs):
        self.research.results = "Mock results generated"
        self.research.plot_paths = []
        
    def get_paper(self, **kwargs):
        pass


class MockResearch:
    """Mock research object"""
    def __init__(self):
        self.data_description = ""
        self.idea = ""
        self.methodology = ""
        self.results = ""
        self.plot_paths = []
