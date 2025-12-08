from typing import Dict, List, Optional
from .mode import Mode


class ModeRegistry:
    """Central registry for all modes"""
    _modes: Dict[str, Mode] = {}

    @classmethod
    def register(cls, mode: Mode):
        """Register a new mode"""
        if mode.id in cls._modes:
            raise ValueError(f"Mode '{mode.id}' already registered")
        cls._modes[mode.id] = mode
        print(f"✅ Registered mode: {mode.id} - {mode.name}")

    @classmethod
    def get_mode(cls, mode_id: str) -> Optional[Mode]:
        """Get mode by ID"""
        return cls._modes.get(mode_id)

    @classmethod
    def list_modes(cls) -> List[Mode]:
        """List all registered modes"""
        return list(cls._modes.values())

    @classmethod
    def list_by_category(cls, category: str) -> List[Mode]:
        """List modes by category"""
        return [m for m in cls._modes.values() if m.category == category]

    @classmethod
    def list_by_engine(cls, engine: str) -> List[Mode]:
        """List modes by engine type"""
        return [m for m in cls._modes.values() if m.engine.value == engine]

    # Backward compatibility aliases
    @classmethod
    def get(cls, mode_id: str) -> Optional[Mode]:
        """Alias for get_mode"""
        return cls.get_mode(mode_id)

    @classmethod
    def list_all(cls) -> List[Mode]:
        """Alias for list_modes"""
        return cls.list_modes()

