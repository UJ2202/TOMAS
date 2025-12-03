from sqlalchemy import Column, String, DateTime, Enum, Text, JSON, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from core.database import Base
from core.enums import MessageRole

class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False, index=True)

    # Message Content
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)

    # Metadata (renamed to avoid SQLAlchemy reserved word)
    message_metadata = Column(JSON, nullable=True)  # Agent name, tool calls, etc.

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    sequence_number = Column(Integer, nullable=False)  # Order in conversation

    # Cost for this message
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)

    # Relationships
    session = relationship("Session", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, session={self.session_id})>"
