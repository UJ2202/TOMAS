from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from core.database import Base

class CostRecord(Base):
    __tablename__ = "cost_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False, index=True)

    # Model Info
    model_name = Column(String(100), nullable=False)
    provider = Column(String(50), nullable=False)  # "openai", "anthropic", "google"

    # Token Usage
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)

    # Cost
    cost = Column(Float, default=0.0)

    # Metadata (renamed to avoid SQLAlchemy reserved word)
    cost_metadata = Column(JSON, nullable=True)  # Agent name, operation, etc.

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    session = relationship("Session", back_populates="costs")

    def __repr__(self):
        return f"<CostRecord(session={self.session_id}, cost=${self.cost:.4f})>"
