from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from core.database import Base

class SessionFile(Base):
    __tablename__ = "session_files"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False, index=True)

    # File Info
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)  # Actual path on disk
    file_size = Column(Integer, nullable=False)  # Bytes
    mime_type = Column(String(100), nullable=True)

    # Type
    is_input = Column(Boolean, default=True)  # Input or output file

    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    session = relationship("Session", back_populates="files")

    def __repr__(self):
        return f"<SessionFile(id={self.id}, filename={self.filename})>"
