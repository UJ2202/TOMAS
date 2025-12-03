"""
Execution Request/Response Schemas
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

from core.enums import SessionStatus


class ExecuteRequest(BaseModel):
    """Request to execute a mode"""
    mode_id: str
    task: str
    input_data: Optional[Dict[str, Any]] = None


class ExecuteResponse(BaseModel):
    """Response from execute endpoint"""
    session_id: str
    status: SessionStatus
    message: str


class TaskStatusResponse(BaseModel):
    """Response with task status"""
    session_id: str
    mode_id: str
    status: SessionStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_tokens: float
    total_cost: float
    error_message: Optional[str] = None


class TaskResultResponse(BaseModel):
    """Response with task results"""
    session_id: str
    mode_id: str
    status: SessionStatus
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    total_tokens: float
    total_cost: float
    created_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
