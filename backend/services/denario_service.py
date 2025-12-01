import sys
from pathlib import Path
import uuid
from typing import Optional

# Add Denario to path
DENARIO_PATH = Path(__file__).parent.parent.parent.parent / "Denario"
sys.path.insert(0, str(DENARIO_PATH))

from denario import Denario, KeyManager

class DenarioService:
    """Service layer for Denario integration"""

    def __init__(self, workspace_dir: str = "./workspaces"):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)

        # Initialize API keys from environment
        try:
            KeyManager.get_keys_from_env()
            print(f"✅ DenarioService initialized (workspace: {workspace_dir})")
        except Exception as e:
            print(f"⚠️  Warning: Could not load API keys: {e}")

    def create_session(self) -> str:
        """Create a new session with unique ID"""
        session_id = str(uuid.uuid4())
        session_dir = self.workspace_dir / session_id
        session_dir.mkdir(exist_ok=True)
        return session_id

    def get_denario_instance(self, session_id: str) -> Denario:
        """Get Denario instance for a session"""
        project_dir = str(self.workspace_dir / session_id)
        return Denario(project_dir=project_dir)

    def get_session_dir(self, session_id: str) -> Path:
        """Get session directory path"""
        return self.workspace_dir / session_id
