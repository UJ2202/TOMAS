"""
Engine Base Interface

Defines the abstract interface that all execution engines must implement.
This allows TOMAS to support multiple backends (CMBAgent, Denario, etc.) with a unified API.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, AsyncIterator, Optional
from dataclasses import dataclass


@dataclass
class EngineOutput:
    """Standardized output format from any engine"""
    status: str  # "running", "completed", "failed"
    content: str
    artifacts: List[Dict[str, Any]]  # Files, plots, etc.
    metadata: Dict[str, Any]  # Engine-specific metadata
    cost_info: Optional[Dict[str, Any]] = None


class IEngine(ABC):
    """Base interface for all execution engines"""

    @abstractmethod
    async def initialize(
        self,
        session_id: str,
        workspace_dir: str,
        config: Dict[str, Any]
    ) -> None:
        """
        Initialize engine for a session

        Args:
            session_id: Unique session identifier
            workspace_dir: Directory for this session's files
            config: Engine-specific configuration
        """
        pass

    @abstractmethod
    async def execute(
        self,
        task: str,
        input_data: Dict[str, Any],
        mode_config: Dict[str, Any]
    ) -> AsyncIterator[EngineOutput]:
        """
        Execute task and yield results

        This is an async generator that yields EngineOutput objects
        as the execution progresses, enabling real-time streaming.

        Args:
            task: The task description/prompt
            input_data: Input data including files, parameters, etc.
            mode_config: Mode-specific execution configuration

        Yields:
            EngineOutput objects as execution progresses
        """
        pass

    @abstractmethod
    async def pause(self) -> Dict[str, Any]:
        """
        Pause execution and return checkpoint

        Returns:
            Checkpoint data that can be used to resume
        """
        pass

    @abstractmethod
    async def resume(self, checkpoint: Dict[str, Any]) -> None:
        """
        Resume from checkpoint

        Args:
            checkpoint: Previously saved checkpoint data
        """
        pass

    @abstractmethod
    async def intervene(self, intervention: Dict[str, Any]) -> None:
        """
        Handle human intervention during execution

        Args:
            intervention: Intervention data (type, parameters, etc.)
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup resources after execution"""
        pass

    @abstractmethod
    def get_cost_estimate(self, input_data: Dict[str, Any]) -> float:
        """
        Estimate cost before execution

        Args:
            input_data: Input data to estimate cost for

        Returns:
            Estimated cost in USD
        """
        pass
