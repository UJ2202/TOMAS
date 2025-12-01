from typing import Dict, List, Optional
from .mode import AgentMode

class ModeRegistry:
    """Central registry for all agent modes"""

    def __init__(self):
        self._modes: Dict[str, AgentMode] = {}

    def register(self, mode: AgentMode):
        """Register a new mode"""
        if mode.id in self._modes:
            raise ValueError(f"Mode '{mode.id}' already registered")
        self._modes[mode.id] = mode
        print(f"✅ Registered mode: {mode.id} - {mode.name}")

    def get(self, mode_id: str) -> Optional[AgentMode]:
        """Get mode by ID"""
        return self._modes.get(mode_id)

    def list_all(self) -> List[AgentMode]:
        """List all registered modes"""
        return list(self._modes.values())

    def list_by_category(self, category: str) -> List[AgentMode]:
        """List modes by category"""
        return [m for m in self._modes.values() if m.category == category]

# Global registry instance
registry = ModeRegistry()
