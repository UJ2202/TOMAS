"""
Engine Registry

Central registry for all execution engines (CMBAgent, Denario, etc.).
Provides factory methods to create engine instances by type.
"""

from typing import Dict, Type, List
from core.enums import EngineType
from .base import IEngine, EngineOutput
from .denario_engine import DenarioEngine

# Try to import CMBAgentEngine, but don't fail if it's not available
try:
    from .cmbagent_engine import CMBAgentEngine
    CMBAGENT_AVAILABLE = True
except Exception as e:
    print(f"⚠️ CMBAgent engine not available: {e}")
    CMBAgentEngine = None
    CMBAGENT_AVAILABLE = False


class EngineRegistry:
    """Registry of available execution engines"""

    _engines: Dict[EngineType, Type[IEngine]] = {}

    # Register available engines
    if CMBAGENT_AVAILABLE:
        _engines[EngineType.CMBAGENT] = CMBAgentEngine
    _engines[EngineType.DENARIO] = DenarioEngine

    @classmethod
    def get_engine(cls, engine_type: EngineType) -> IEngine:
        """
        Get engine instance by type

        Args:
            engine_type: Type of engine to create (CMBAGENT, DENARIO, etc.)

        Returns:
            Instance of the requested engine

        Raises:
            ValueError: If engine type is not registered
        """
        engine_class = cls._engines.get(engine_type)
        if not engine_class:
            raise ValueError(
                f"Unknown engine type: {engine_type}. "
                f"Available engines: {list(cls._engines.keys())}"
            )
        return engine_class()

    @classmethod
    def register_engine(cls, engine_type: EngineType, engine_class: Type[IEngine]) -> None:
        """
        Register a new engine (for future extensibility)

        Args:
            engine_type: Type enum for the engine
            engine_class: Engine class that implements IEngine

        Example:
            # Register a new engine type
            class KosmosEngine(IEngine):
                ...

            EngineRegistry.register_engine(EngineType.KOSMOS, KosmosEngine)
        """
        if not issubclass(engine_class, IEngine):
            raise TypeError(f"{engine_class} must implement IEngine interface")

        cls._engines[engine_type] = engine_class
        print(f" Registered engine: {engine_type.value}")

    @classmethod
    def list_engines(cls) -> List[str]:
        """
        List all available engine types

        Returns:
            List of engine type names
        """
        return [e.value for e in cls._engines.keys()]

    @classmethod
    def is_registered(cls, engine_type: EngineType) -> bool:
        """
        Check if an engine type is registered

        Args:
            engine_type: Engine type to check

        Returns:
            True if registered, False otherwise
        """
        return engine_type in cls._engines


# Export all components
__all__ = [
    'IEngine',
    'EngineOutput',
    'EngineRegistry',
    'CMBAgentEngine',
    'DenarioEngine',
]
