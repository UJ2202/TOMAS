"""
Mode Executor Service

Routes execution to the appropriate engine (CMBAgent, Denario, etc.) based on mode configuration.
Manages background task execution and handles streaming of results.
"""

from typing import Dict, Any, AsyncIterator, Optional
from pathlib import Path
import asyncio
from datetime import datetime

from engines import EngineRegistry, EngineOutput
from core.enums import EngineType, SessionStatus, MessageRole
from core.mode_registry import ModeRegistry
from services.session_manager import SessionManager
from core.config import settings


class ModeExecutor:
    """Executes modes by routing to appropriate engines"""

    def __init__(self, session_manager: SessionManager):
        """
        Initialize ModeExecutor

        Args:
            session_manager: SessionManager instance for session operations
        """
        self.session_manager = session_manager
        self._background_tasks: Dict[str, asyncio.Task] = {}

    async def execute_mode(
        self,
        session_id: str,
        mode_id: str,
        task: str,
        input_data: Dict[str, Any],
        stream: bool = True
    ) -> AsyncIterator[EngineOutput]:
        """
        Execute a mode by routing to the appropriate engine

        Args:
            session_id: Session ID for this execution
            mode_id: Mode to execute
            task: Task description/prompt
            input_data: Input data including files and parameters
            stream: Whether to stream results (True) or wait for completion (False)

        Yields:
            EngineOutput objects as execution progresses

        Raises:
            ValueError: If mode not found or engine not available
        """
        # Get mode configuration
        mode = ModeRegistry.get_mode(mode_id)
        if not mode:
            raise ValueError(f"Mode '{mode_id}' not found")

        # Get session
        session = await self.session_manager.get_session(session_id)
        if not session:
            raise ValueError(f"Session '{session_id}' not found")

        # Update session status to RUNNING
        await self.session_manager.update_status(session_id, SessionStatus.RUNNING)

        # Log start message
        await self.session_manager.add_message(
            session_id=session_id,
            role=MessageRole.SYSTEM,
            content=f"Starting execution of mode: {mode.name}",
            metadata={"mode_id": mode_id, "engine": mode.engine.value}
        )

        try:
            # Get the appropriate engine
            engine = EngineRegistry.get_engine(mode.engine)

            # Get workspace directory
            workspace_dir = session.workspace_path

            # Prepare engine configuration
            engine_config = self._prepare_engine_config(mode, input_data)

            # Initialize engine
            await engine.initialize(
                session_id=session_id,
                workspace_dir=workspace_dir,
                config=engine_config
            )

            # Get mode-specific execution configuration
            mode_config = mode.config.engine_config if mode.config else {}

            # Execute and stream results
            async for output in engine.execute(
                task=task,
                input_data=input_data,
                mode_config=mode_config
            ):
                # Save output as message
                await self.session_manager.add_message(
                    session_id=session_id,
                    role=MessageRole.ASSISTANT,
                    content=output.content,
                    metadata={
                        "status": output.status,
                        "artifacts_count": len(output.artifacts),
                        **output.metadata
                    },
                    tokens_used=output.cost_info.get("total_tokens", 0) if output.cost_info else 0,
                    cost=output.cost_info.get("cost_usd", 0.0) if output.cost_info else 0.0
                )

                # Yield output for streaming
                yield output

                # If execution completed or failed, update session status
                if output.status == "completed":
                    await self.session_manager.update_status(
                        session_id,
                        SessionStatus.COMPLETED
                    )
                    # Save output data
                    await self.session_manager.update_output_data(
                        session_id,
                        {
                            "content": output.content,
                            "artifacts": output.artifacts,
                            "metadata": output.metadata
                        }
                    )
                elif output.status == "failed":
                    await self.session_manager.update_status(
                        session_id,
                        SessionStatus.FAILED,
                        error_message=output.content
                    )

            # Cleanup engine resources
            await engine.cleanup()

        except Exception as e:
            # Log error
            await self.session_manager.add_message(
                session_id=session_id,
                role=MessageRole.SYSTEM,
                content=f"Execution failed: {str(e)}",
                metadata={"error": str(e)}
            )

            # Update session status to FAILED
            await self.session_manager.update_status(
                session_id,
                SessionStatus.FAILED,
                error_message=str(e)
            )

            # Yield error output
            yield EngineOutput(
                status="failed",
                content=f"Execution failed: {str(e)}",
                artifacts=[],
                metadata={"error": str(e), "mode_id": mode_id}
            )

    def _prepare_engine_config(
        self,
        mode: Any,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prepare engine configuration from mode and input data

        Args:
            mode: Mode object
            input_data: Input data

        Returns:
            Engine configuration dictionary
        """
        # Start with mode's engine config
        config = dict(mode.config.engine_config) if mode.config else {}

        # Add any API keys from settings
        api_keys = {}
        if settings.OPENAI_API_KEY:
            api_keys["openai"] = settings.OPENAI_API_KEY
        if settings.ANTHROPIC_API_KEY:
            api_keys["anthropic"] = settings.ANTHROPIC_API_KEY
        if settings.GOOGLE_API_KEY:
            api_keys["google"] = settings.GOOGLE_API_KEY

        config["api_keys"] = api_keys

        # Add any user-provided configuration from input_data
        user_config = input_data.get("config", {})
        config.update(user_config)

        return config

    async def execute_mode_background(
        self,
        session_id: str,
        mode_id: str,
        task: str,
        input_data: Dict[str, Any]
    ) -> str:
        """
        Execute mode in background task

        Args:
            session_id: Session ID
            mode_id: Mode to execute
            task: Task description
            input_data: Input data

        Returns:
            Task ID for tracking
        """
        # Create background task
        task_obj = asyncio.create_task(
            self._run_background_execution(session_id, mode_id, task, input_data)
        )

        # Store task reference
        self._background_tasks[session_id] = task_obj

        return session_id

    async def _run_background_execution(
        self,
        session_id: str,
        mode_id: str,
        task: str,
        input_data: Dict[str, Any]
    ) -> None:
        """
        Internal method to run execution in background

        Args:
            session_id: Session ID
            mode_id: Mode to execute
            task: Task description
            input_data: Input data
        """
        try:
            # Execute and consume all outputs
            async for output in self.execute_mode(
                session_id=session_id,
                mode_id=mode_id,
                task=task,
                input_data=input_data,
                stream=False
            ):
                # Outputs are already saved to database by execute_mode
                pass
        except Exception as e:
            # Errors are already handled by execute_mode
            pass
        finally:
            # Remove from background tasks when done
            self._background_tasks.pop(session_id, None)

    async def pause_execution(self, session_id: str) -> Dict[str, Any]:
        """
        Pause an ongoing execution

        Args:
            session_id: Session ID to pause

        Returns:
            Checkpoint data

        Raises:
            ValueError: If session not found or not running
        """
        session = await self.session_manager.get_session(session_id)
        if not session:
            raise ValueError(f"Session '{session_id}' not found")

        if session.status != SessionStatus.RUNNING:
            raise ValueError(f"Session '{session_id}' is not running")

        # TODO: Implement actual pause logic with engine
        # For now, just update status
        await self.session_manager.update_status(session_id, SessionStatus.PAUSED)

        checkpoint = {
            "session_id": session_id,
            "paused_at": datetime.utcnow().isoformat()
        }

        await self.session_manager.save_checkpoint(session_id, checkpoint)

        return checkpoint

    async def resume_execution(self, session_id: str) -> AsyncIterator[EngineOutput]:
        """
        Resume a paused execution

        Args:
            session_id: Session ID to resume

        Yields:
            EngineOutput objects as execution continues

        Raises:
            ValueError: If session not found or not paused
        """
        session = await self.session_manager.get_session(session_id)
        if not session:
            raise ValueError(f"Session '{session_id}' not found")

        if session.status != SessionStatus.PAUSED:
            raise ValueError(f"Session '{session_id}' is not paused")

        # Load checkpoint
        checkpoint = await self.session_manager.load_checkpoint(session_id)
        if not checkpoint:
            raise ValueError(f"No checkpoint found for session '{session_id}'")

        # TODO: Implement actual resume logic with engine
        # For now, just update status
        await self.session_manager.update_status(session_id, SessionStatus.RUNNING)

        yield EngineOutput(
            status="running",
            content="Execution resumed",
            artifacts=[],
            metadata={"resumed_from": checkpoint.get("paused_at")}
        )

    async def cancel_execution(self, session_id: str) -> None:
        """
        Cancel an ongoing execution

        Args:
            session_id: Session ID to cancel
        """
        # Cancel background task if exists
        task = self._background_tasks.get(session_id)
        if task and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        # Update session status
        await self.session_manager.update_status(session_id, SessionStatus.CANCELLED)

    def get_task_status(self, session_id: str) -> Optional[str]:
        """
        Get status of a background task

        Args:
            session_id: Session ID

        Returns:
            Task status or None if not found
        """
        task = self._background_tasks.get(session_id)
        if not task:
            return None

        if task.done():
            if task.cancelled():
                return "cancelled"
            elif task.exception():
                return "failed"
            else:
                return "completed"
        else:
            return "running"
