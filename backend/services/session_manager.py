"""
Session Manager Service

Manages session lifecycle, persistence, messages, and checkpoints.
Works with ANY engine (CMBAgent, Denario, or future engines).
"""

from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pathlib import Path
import shutil
from datetime import datetime
import uuid

from models.session import Session
from models.message import Message
from models.file import SessionFile
from core.enums import SessionStatus, MessageRole
from core.config import settings


class SessionManager:
    """Manages session lifecycle and persistence"""

    def __init__(self, db: AsyncSession):
        """
        Initialize SessionManager

        Args:
            db: AsyncSession for database operations
        """
        self.db = db

    async def create_session(
        self,
        mode_id: str,
        engine_type: str,
        input_data: Dict[str, Any]
    ) -> Session:
        """
        Create a new session

        Args:
            mode_id: ID of the mode being executed
            engine_type: Type of engine (CMBAGENT, DENARIO, etc.)
            input_data: Input parameters for the session

        Returns:
            Created Session object
        """
        # Generate unique session ID
        session_id = str(uuid.uuid4())

        session = Session(
            id=session_id,
            mode_id=mode_id,
            engine_type=engine_type,
            input_data=input_data,
            status=SessionStatus.CREATED,
            total_tokens=0,
            total_cost=0.0,
            created_at=datetime.utcnow()
        )

        # Create workspace directory structure
        workspace_path = settings.WORKSPACE_DIR / "sessions" / session.id
        workspace_path.mkdir(parents=True, exist_ok=True)
        (workspace_path / "input_files").mkdir(exist_ok=True)
        (workspace_path / "outputs").mkdir(exist_ok=True)
        (workspace_path / "logs").mkdir(exist_ok=True)
        (workspace_path / "checkpoints").mkdir(exist_ok=True)

        session.workspace_path = str(workspace_path)

        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)

        return session

    async def get_session(self, session_id: str) -> Optional[Session]:
        """
        Get session by ID

        Args:
            session_id: Session ID to retrieve

        Returns:
            Session object or None if not found
        """
        result = await self.db.execute(
            select(Session).where(Session.id == session_id)
        )
        return result.scalar_one_or_none()

    async def update_status(
        self,
        session_id: str,
        status: SessionStatus,
        error_message: Optional[str] = None
    ) -> Session:
        """
        Update session status

        Args:
            session_id: Session ID to update
            status: New status
            error_message: Optional error message if status is FAILED

        Returns:
            Updated Session object

        Raises:
            ValueError: If session not found
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        session.status = status

        if error_message:
            session.error_message = error_message

        # Set timestamps based on status
        if status == SessionStatus.RUNNING and not session.started_at:
            session.started_at = datetime.utcnow()

        if status in [SessionStatus.COMPLETED, SessionStatus.FAILED, SessionStatus.CANCELLED]:
            session.completed_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def add_message(
        self,
        session_id: str,
        role: MessageRole,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        tokens_used: int = 0,
        cost: float = 0.0
    ) -> Message:
        """
        Add a message to session history

        Args:
            session_id: Session ID
            role: Message role (SYSTEM, USER, ASSISTANT, TOOL)
            content: Message content
            metadata: Optional metadata dictionary
            tokens_used: Number of tokens used
            cost: Cost in USD

        Returns:
            Created Message object
        """
        # Get next sequence number
        result = await self.db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.sequence_number.desc())
            .limit(1)
        )
        last_message = result.scalar_one_or_none()
        sequence_number = (last_message.sequence_number + 1) if last_message else 0

        message = Message(
            session_id=session_id,
            role=role,
            content=content,
            message_metadata=metadata or {},
            sequence_number=sequence_number,
            tokens_used=tokens_used,
            cost=cost,
            timestamp=datetime.utcnow()
        )

        self.db.add(message)

        # Update session cost and token tracking
        session = await self.get_session(session_id)
        if session:
            session.total_tokens += tokens_used
            session.total_cost += cost

        await self.db.commit()
        await self.db.refresh(message)

        return message

    async def get_messages(
        self,
        session_id: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Message]:
        """
        Get conversation history for a session

        Args:
            session_id: Session ID
            limit: Maximum number of messages to return
            offset: Number of messages to skip

        Returns:
            List of Message objects ordered by sequence number
        """
        query = select(Message).where(
            Message.session_id == session_id
        ).order_by(Message.sequence_number).offset(offset)

        if limit:
            query = query.limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def save_checkpoint(
        self,
        session_id: str,
        checkpoint_data: Dict[str, Any]
    ) -> None:
        """
        Save checkpoint for pause/resume functionality

        Args:
            session_id: Session ID
            checkpoint_data: Checkpoint data to save

        Raises:
            ValueError: If session not found
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        session.checkpoint_data = checkpoint_data
        await self.db.commit()

    async def load_checkpoint(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load checkpoint data for resuming

        Args:
            session_id: Session ID

        Returns:
            Checkpoint data or None if no checkpoint exists
        """
        session = await self.get_session(session_id)
        return session.checkpoint_data if session else None

    async def list_sessions(
        self,
        status: Optional[SessionStatus] = None,
        mode_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Session]:
        """
        List sessions with optional filters

        Args:
            status: Filter by status
            mode_id: Filter by mode ID
            limit: Maximum number of sessions to return
            offset: Number of sessions to skip

        Returns:
            List of Session objects ordered by creation date (newest first)
        """
        query = select(Session).order_by(Session.created_at.desc()).offset(offset)

        if status:
            query = query.where(Session.status == status)
        if mode_id:
            query = query.where(Session.mode_id == mode_id)

        query = query.limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete_session(self, session_id: str) -> None:
        """
        Delete session and cleanup workspace

        Args:
            session_id: Session ID to delete
        """
        session = await self.get_session(session_id)
        if not session:
            return

        # Delete workspace directory and all contents
        if session.workspace_path:
            workspace_path = Path(session.workspace_path)
            if workspace_path.exists():
                shutil.rmtree(workspace_path)

        # Delete from database (cascade should delete related messages, files, costs)
        await self.db.delete(session)
        await self.db.commit()

    def get_workspace_dir(self, session_id: str) -> Path:
        """
        Get workspace directory path for a session

        Args:
            session_id: Session ID

        Returns:
            Path to the session's workspace directory
        """
        return settings.WORKSPACE_DIR / "sessions" / session_id

    async def add_file(
        self,
        session_id: str,
        filename: str,
        original_filename: str,
        file_path: str,
        file_size: int,
        mime_type: Optional[str] = None,
        is_input: bool = True
    ) -> SessionFile:
        """
        Add file record to session

        Args:
            session_id: Session ID
            filename: Stored filename
            original_filename: Original uploaded filename
            file_path: Full path to the file
            file_size: File size in bytes
            mime_type: MIME type of the file
            is_input: True if input file, False if output

        Returns:
            Created SessionFile object
        """
        session_file = SessionFile(
            session_id=session_id,
            filename=filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
            is_input=is_input,
            uploaded_at=datetime.utcnow()
        )

        self.db.add(session_file)
        await self.db.commit()
        await self.db.refresh(session_file)

        return session_file

    async def get_session_files(
        self,
        session_id: str,
        is_input: Optional[bool] = None
    ) -> List[SessionFile]:
        """
        Get files associated with a session

        Args:
            session_id: Session ID
            is_input: Filter by input/output files (None for all)

        Returns:
            List of SessionFile objects
        """
        query = select(SessionFile).where(SessionFile.session_id == session_id)

        if is_input is not None:
            query = query.where(SessionFile.is_input == is_input)

        query = query.order_by(SessionFile.uploaded_at)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_output_data(
        self,
        session_id: str,
        output_data: Dict[str, Any]
    ) -> Session:
        """
        Update session's output data

        Args:
            session_id: Session ID
            output_data: Output data to save

        Returns:
            Updated Session object

        Raises:
            ValueError: If session not found
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        session.output_data = output_data
        await self.db.commit()
        await self.db.refresh(session)

        return session
