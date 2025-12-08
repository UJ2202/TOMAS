"""
Execution Router

API endpoints for executing modes, managing sessions, and retrieving results.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
import json

from core.database import get_db
from core.mode_registry import ModeRegistry
from services.session_manager import SessionManager
from services.mode_executor import ModeExecutor
from core.enums import SessionStatus
from schemas.execution import ExecuteRequest, ExecuteResponse, TaskStatusResponse, TaskResultResponse


router = APIRouter(tags=["execution"])


class ExecuteRequest(BaseModel):
    """Request to execute a mode"""
    mode_id: str
    task: str
    input_data: Dict[str, Any] = {}
    stream: bool = False


class ExecuteResponse(BaseModel):
    """Response for execution request"""
    session_id: str
    status: str
    message: str


class TaskStatusResponse(BaseModel):
    """Task status response"""
    session_id: str
    status: str
    progress: Optional[float] = None
    error_message: Optional[str] = None
    total_tokens: int = 0
    total_cost: float = 0.0


class TaskResultResponse(BaseModel):
    """Task result response"""
    session_id: str
    status: str
    output_data: Optional[Dict[str, Any]] = None
    artifacts: List[Dict[str, Any]] = []
    messages_count: int = 0


# Dependency to get SessionManager
async def get_session_manager(db: AsyncSession = Depends(get_db)) -> SessionManager:
    """Get SessionManager instance"""
    return SessionManager(db)


# Dependency to get ModeExecutor
async def get_mode_executor(
    session_manager: SessionManager = Depends(get_session_manager)
) -> ModeExecutor:
    """Get ModeExecutor instance"""
    return ModeExecutor(session_manager)


@router.post("/execute", response_model=ExecuteResponse)
async def execute_mode(
    request: ExecuteRequest,
    background_tasks: BackgroundTasks,
    mode_executor: ModeExecutor = Depends(get_mode_executor),
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Execute a mode

    Creates a session and starts execution in the background.
    Returns immediately with session_id for tracking.

    Args:
        request: Execution request with mode_id, task, and input_data

    Returns:
        ExecuteResponse with session_id and status
    """
    # Validate mode exists
    mode = ModeRegistry.get_mode(request.mode_id)
    if not mode:
        raise HTTPException(
            status_code=404,
            detail=f"Mode '{request.mode_id}' not found"
        )

    # Create session
    try:
        session = await session_manager.create_session(
            mode_id=request.mode_id,
            engine_type=mode.engine.value,
            input_data=request.input_data
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create session: {str(e)}"
        )

    # Execute in background if not streaming
    if not request.stream:
        background_tasks.add_task(
            mode_executor.execute_mode_background,
            session.id,
            request.mode_id,
            request.task,
            request.input_data
        )

        return ExecuteResponse(
            session_id=session.id,
            status="queued",
            message=f"Execution started for mode '{mode.name}'"
        )
    else:
        # For streaming, client should use /execute/stream endpoint
        raise HTTPException(
            status_code=400,
            detail="Use /execute/stream endpoint for streaming execution"
        )


@router.post("/execute/stream")
async def execute_mode_stream(
    request: ExecuteRequest,
    mode_executor: ModeExecutor = Depends(get_mode_executor),
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Execute a mode with streaming results

    Returns a Server-Sent Events (SSE) stream of execution progress.

    Args:
        request: Execution request with mode_id, task, and input_data

    Returns:
        StreamingResponse with SSE events
    """
    # Validate mode exists
    mode = ModeRegistry.get_mode(request.mode_id)
    if not mode:
        raise HTTPException(
            status_code=404,
            detail=f"Mode '{request.mode_id}' not found"
        )

    # Create session
    try:
        session = await session_manager.create_session(
            mode_id=request.mode_id,
            engine_type=mode.engine.value,
            input_data=request.input_data
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create session: {str(e)}"
        )

    # Stream execution
    async def event_generator():
        """Generate SSE events from execution"""
        try:
            async for output in mode_executor.execute_mode(
                session_id=session.id,
                mode_id=request.mode_id,
                task=request.task,
                input_data=request.input_data,
                stream=True
            ):
                # Format as SSE event
                event_data = {
                    "session_id": session.id,
                    "status": output.status,
                    "content": output.content,
                    "artifacts": output.artifacts,
                    "metadata": output.metadata
                }

                yield f"data: {json.dumps(event_data)}\n\n"

        except Exception as e:
            error_data = {
                "session_id": session.id,
                "status": "error",
                "error": str(e)
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@router.get("/tasks/{session_id}/status", response_model=TaskStatusResponse)
async def get_task_status(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Get execution status for a session

    Args:
        session_id: Session ID to check

    Returns:
        TaskStatusResponse with current status and progress
    """
    session = await session_manager.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' not found"
        )

    return TaskStatusResponse(
        session_id=session.id,
        status=session.status.value,
        error_message=session.error_message,
        total_tokens=session.total_tokens,
        total_cost=session.total_cost
    )


@router.get("/tasks/{session_id}/results", response_model=TaskResultResponse)
async def get_task_results(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Get execution results for a completed session

    Args:
        session_id: Session ID to get results for

    Returns:
        TaskResultResponse with output data and artifacts
    """
    session = await session_manager.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' not found"
        )

    # Get messages count
    messages = await session_manager.get_messages(session_id)

    # Get artifacts (files)
    files = await session_manager.get_session_files(session_id, is_input=False)
    artifacts = [
        {
            "name": f.filename,
            "original_name": f.original_filename,
            "path": f.file_path,
            "size": f.file_size,
            "mime_type": f.mime_type
        }
        for f in files
    ]

    return TaskResultResponse(
        session_id=session.id,
        status=session.status.value,
        output_data=session.output_data,
        artifacts=artifacts,
        messages_count=len(messages)
    )


@router.post("/tasks/{session_id}/pause")
async def pause_task(
    session_id: str,
    mode_executor: ModeExecutor = Depends(get_mode_executor)
):
    """
    Pause an ongoing execution

    Args:
        session_id: Session ID to pause

    Returns:
        Checkpoint data
    """
    try:
        checkpoint = await mode_executor.pause_execution(session_id)
        return {
            "session_id": session_id,
            "status": "paused",
            "checkpoint": checkpoint
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to pause: {str(e)}")


@router.post("/tasks/{session_id}/resume")
async def resume_task(
    session_id: str,
    mode_executor: ModeExecutor = Depends(get_mode_executor)
):
    """
    Resume a paused execution

    Args:
        session_id: Session ID to resume

    Returns:
        Resume confirmation
    """
    try:
        # Start resume in background
        async def resume_generator():
            async for output in mode_executor.resume_execution(session_id):
                yield f"data: {json.dumps({'content': output.content})}\n\n"

        return StreamingResponse(
            resume_generator(),
            media_type="text/event-stream"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resume: {str(e)}")


@router.post("/tasks/{session_id}/cancel")
async def cancel_task(
    session_id: str,
    mode_executor: ModeExecutor = Depends(get_mode_executor)
):
    """
    Cancel an ongoing execution

    Args:
        session_id: Session ID to cancel

    Returns:
        Cancellation confirmation
    """
    try:
        await mode_executor.cancel_execution(session_id)
        return {
            "session_id": session_id,
            "status": "cancelled",
            "message": "Execution cancelled"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel: {str(e)}")


@router.get("/tasks/{session_id}/messages")
async def get_task_messages(
    session_id: str,
    limit: Optional[int] = 100,
    offset: int = 0,
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Get conversation history for a session

    Args:
        session_id: Session ID
        limit: Maximum number of messages to return
        offset: Number of messages to skip

    Returns:
        List of messages
    """
    session = await session_manager.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' not found"
        )

    messages = await session_manager.get_messages(session_id, limit, offset)

    return {
        "session_id": session_id,
        "messages": [
            {
                "role": msg.role.value,
                "content": msg.content,
                "metadata": msg.message_metadata,
                "timestamp": msg.timestamp.isoformat(),
                "tokens_used": msg.tokens_used,
                "cost": msg.cost
            }
            for msg in messages
        ],
        "total": len(messages)
    }
