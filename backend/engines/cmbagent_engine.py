"""
CMBAgent Engine Wrapper

Wraps CMBAgent (48+ specialized agents) with the standard IEngine interface.
Used by RFP/SOW mode, ITOps mode, and other CMBAgent-based tasks.
"""

from typing import Dict, Any, AsyncIterator, Optional, List
from pathlib import Path
import asyncio
import sys
import os

from .base import IEngine, EngineOutput

# Import CMBAgent
sys.path.insert(0, str(Path(__file__).parent.parent / "cmbagent"))
from cmbagent import CMBAgent


class CMBAgentEngine(IEngine):
    """Wrapper for CMBAgent with standardized interface"""

    def __init__(self):
        self.agent: Optional[CMBAgent] = None
        self.session_id: Optional[str] = None
        self.workspace_dir: Optional[Path] = None
        self._pause_requested = False
        self._config: Dict[str, Any] = {}

    async def initialize(
        self,
        session_id: str,
        workspace_dir: str,
        config: Dict[str, Any]
    ) -> None:
        """
        Initialize CMBAgent instance

        Args:
            session_id: Unique session identifier
            workspace_dir: Directory for this session's files
            config: Configuration including:
                - api_keys: Dict of API keys
                - platform: 'oai', 'anthropic', etc.
                - model: Model name
                - temperature: Sampling temperature
                - max_round: Maximum conversation rounds
                - default_llm_model: Default LLM model
        """
        self.session_id = session_id
        self.workspace_dir = Path(workspace_dir)
        self._config = config

        # Create output directory
        output_dir = self.workspace_dir / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize CMBAgent with configuration
        self.agent = CMBAgent(
            work_dir=str(output_dir),
            api_keys=config.get("api_keys"),
            platform=config.get("platform", "oai"),
            model=config.get("model", "gpt4o"),
            temperature=config.get("temperature", 0.0),
            max_round=config.get("max_round", 50),
            skip_rag_agents=config.get("skip_rag_agents", True),
            skip_executor=config.get("skip_executor", False),
            clear_work_dir=config.get("clear_work_dir", False),
            verbose=config.get("verbose", False),
            default_llm_model=config.get("default_llm_model", "gpt-4o"),
            default_formatter_model=config.get("default_formatter_model", "gpt-4o-mini"),
        )

    async def execute(
        self,
        task: str,
        input_data: Dict[str, Any],
        mode_config: Dict[str, Any]
    ) -> AsyncIterator[EngineOutput]:
        """
        Execute task with CMBAgent

        Args:
            task: The task description
            input_data: Input data including:
                - uploaded_files: List of file information
                - parameters: Additional parameters
            mode_config: Mode configuration including:
                - mode: "planning_and_control", "one_shot", "chat"
                - initial_agent: Starting agent name
                - max_rounds: Maximum conversation rounds
                - shared_context: Additional context

        Yields:
            EngineOutput objects as execution progresses
        """
        yield EngineOutput(
            status="running",
            content="Initializing CMBAgent...",
            artifacts=[],
            metadata={"step": "initialization"}
        )

        # Extract configuration
        execution_mode = mode_config.get("mode", "planning_and_control")
        initial_agent = mode_config.get("initial_agent", "task_improver")
        max_rounds = mode_config.get("max_rounds", 10)
        shared_context = mode_config.get("shared_context", {})

        # Build file context and augment task
        file_context = self._build_file_context(input_data)
        full_task = f"{task}\n\n{file_context}" if file_context else task

        yield EngineOutput(
            status="running",
            content=f"Starting execution with mode: {execution_mode}, initial agent: {initial_agent}",
            artifacts=[],
            metadata={
                "mode": execution_mode,
                "initial_agent": initial_agent,
                "max_rounds": max_rounds
            }
        )

        # Execute CMBAgent in thread pool (it's synchronous)
        try:
            loop = asyncio.get_event_loop()

            # Run the solve method
            await loop.run_in_executor(
                None,
                self.agent.solve,
                full_task,
                initial_agent,
                shared_context,
                execution_mode,
                None,  # step
                max_rounds
            )

            # Collect artifacts after execution
            artifacts = self._collect_artifacts()

            # Get final context
            final_context = getattr(self.agent, 'final_context', {})

            yield EngineOutput(
                status="completed",
                content=f"CMBAgent execution completed successfully.\n\nTask: {task}\n\nCheck the artifacts for detailed results.",
                artifacts=artifacts,
                metadata={
                    "mode": execution_mode,
                    "initial_agent": initial_agent,
                    "final_context": str(final_context)[:500] if final_context else ""
                },
                cost_info=self._calculate_cost()
            )

        except Exception as e:
            yield EngineOutput(
                status="failed",
                content=f"CMBAgent execution failed: {str(e)}",
                artifacts=[],
                metadata={"error": str(e)},
                cost_info=self._calculate_cost()
            )

    def _build_file_context(self, input_data: Dict[str, Any]) -> str:
        """
        Build file context string for agent

        Args:
            input_data: Input data containing uploaded_files

        Returns:
            Formatted string with file information
        """
        uploaded_files = input_data.get("uploaded_files", [])
        if not uploaded_files:
            return ""

        file_list = []
        for file_info in uploaded_files:
            file_path = file_info.get("path")
            file_name = file_info.get("name", file_info.get("original_filename", "unknown"))
            file_list.append(f"- {file_name}: {file_path}")

        return "Uploaded files:\n" + "\n".join(file_list)

    def _collect_artifacts(self) -> List[Dict[str, Any]]:
        """
        Collect output files from workspace

        Returns:
            List of artifact dictionaries
        """
        artifacts = []
        output_dir = self.workspace_dir / "outputs"

        if output_dir.exists():
            for file_path in output_dir.rglob("*"):
                if file_path.is_file():
                    # Skip hidden files and cache
                    if file_path.name.startswith('.') or '__pycache__' in str(file_path):
                        continue

                    artifacts.append({
                        "type": "file",
                        "name": file_path.name,
                        "path": str(file_path),
                        "relative_path": str(file_path.relative_to(output_dir)),
                        "size": file_path.stat().st_size
                    })

        return artifacts

    def _calculate_cost(self) -> Dict[str, Any]:
        """
        Calculate cost from CMBAgent usage

        Returns:
            Cost information dictionary
        """
        # Try to get cost from CMBAgent's cost reporting
        try:
            if self.agent and hasattr(self.agent, 'final_context'):
                final_context = self.agent.final_context
                cost_report_path = final_context.get('cost_report_path')

                if cost_report_path and os.path.exists(cost_report_path):
                    import json
                    with open(cost_report_path, 'r') as f:
                        cost_data = json.load(f)

                    return {
                        "total_tokens": cost_data.get("total_tokens", 0),
                        "cost_usd": cost_data.get("total_cost", 0.0),
                        "details": cost_data
                    }
        except Exception as e:
            # If cost tracking fails, return default
            pass

        # Default fallback
        return {
            "total_tokens": 0,
            "cost_usd": 0.0,
            "note": "Cost tracking unavailable"
        }

    async def pause(self) -> Dict[str, Any]:
        """
        Pause execution

        Returns:
            Checkpoint data for resuming
        """
        self._pause_requested = True

        # Save current state
        checkpoint = {
            "session_id": self.session_id,
            "workspace_dir": str(self.workspace_dir),
            "state": "paused",
            "config": self._config
        }

        # If agent has final_context, save it
        if self.agent and hasattr(self.agent, 'final_context'):
            checkpoint["final_context"] = self.agent.final_context

        return checkpoint

    async def resume(self, checkpoint: Dict[str, Any]) -> None:
        """
        Resume from checkpoint

        Args:
            checkpoint: Previously saved checkpoint data
        """
        self._pause_requested = False

        # Restore session info
        self.session_id = checkpoint.get("session_id")
        self.workspace_dir = Path(checkpoint.get("workspace_dir", ""))
        self._config = checkpoint.get("config", {})

        # Reinitialize if needed
        if not self.agent:
            await self.initialize(
                self.session_id,
                str(self.workspace_dir),
                self._config
            )

    async def intervene(self, intervention: Dict[str, Any]) -> None:
        """
        Handle human intervention

        Args:
            intervention: Intervention data including:
                - type: Type of intervention
                - data: Intervention-specific data
        """
        intervention_type = intervention.get("type")

        # Different intervention types can be handled here
        # For now, we support basic interventions

        if intervention_type == "modify_task":
            # Store modified task for next execution
            pass
        elif intervention_type == "change_agent":
            # Change the current agent
            pass
        elif intervention_type == "add_context":
            # Add additional context
            if self.agent and hasattr(self.agent, 'shared_context'):
                additional_context = intervention.get("context", {})
                self.agent.shared_context.update(additional_context)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self.agent = None
        self._config = {}

    def get_cost_estimate(self, input_data: Dict[str, Any]) -> float:
        """
        Estimate cost before execution

        Args:
            input_data: Input data to estimate cost for

        Returns:
            Estimated cost in USD
        """
        # Rough estimate based on input size and typical usage
        input_size = len(str(input_data))
        task_complexity = input_data.get("estimated_complexity", "medium")

        # Base estimates
        estimates = {
            "simple": 0.50,
            "medium": 2.00,
            "complex": 5.00
        }

        base_cost = estimates.get(task_complexity, 2.00)

        # Adjust for input size (rough heuristic)
        size_multiplier = max(1.0, input_size / 10000)

        return base_cost * size_multiplier
