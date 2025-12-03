from sqlalchemy import Column, String, DateTime, Enum, Float, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from core.database import Base
from core.enums import SessionStatus, EngineType

class Session(Base):
    __tablename__ = "sessions"

    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Mode & Engine
    mode_id = Column(String(100), nullable=False, index=True)
    engine_type = Column(Enum(EngineType), nullable=False)

    # Status
    status = Column(Enum(SessionStatus), default=SessionStatus.CREATED, nullable=False, index=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Input/Output
    input_data = Column(JSON, nullable=True)  # Original input
    output_data = Column(JSON, nullable=True)  # Final output

    # Execution Metadata
    error_message = Column(Text, nullable=True)
    checkpoint_data = Column(JSON, nullable=True)  # For pause/resume

    # Cost Tracking
    total_cost = Column(Float, default=0.0)
    total_tokens = Column(Float, default=0.0)

    # Workspace
    workspace_path = Column(String(500), nullable=True)

    # Relationships
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    files = relationship("SessionFile", back_populates="session", cascade="all, delete-orphan")
    costs = relationship("CostRecord", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Session(id={self.id}, mode={self.mode_id}, status={self.status})>"
