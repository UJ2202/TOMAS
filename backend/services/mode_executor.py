from typing import Dict, Any
import asyncio
from pathlib import Path

from services.denario_service import DenarioService
from core.mode import AgentMode

class ModeExecutor:
    """
    Executes agent modes using registered strategies
    """

    def __init__(self, denario_service: DenarioService):
        self.denario_service = denario_service

    async def execute(
        self,
        mode: AgentMode,
        session_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a mode asynchronously

        Args:
            mode: AgentMode definition
            session_id: Session identifier
            input_data: User inputs

        Returns:
            Execution results
        """
        if not mode.strategy:
            raise ValueError(f"Mode '{mode.id}' has no execution strategy")

        # Get Denario instance for this session
        denario = self.denario_service.get_denario_instance(session_id)

        # Execute strategy in thread pool (Denario is synchronous)
        result = await asyncio.to_thread(
            mode.strategy,
            denario,
            input_data,
            mode.denario_config
        )

        return result
