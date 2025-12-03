from sqlalchemy import Column, String, DateTime, Text, Boolean
from datetime import datetime
import uuid

from core.database import Base

class UserConfig(Base):
    __tablename__ = "user_configs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Config Type
    config_type = Column(String(50), nullable=False)  # "api_keys", "credentials", "yaml"
    config_name = Column(String(100), nullable=False)  # "openai", "anthropic", etc.

    # Content (encrypted in production)
    config_value = Column(Text, nullable=False)

    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserConfig(type={self.config_type}, name={self.config_name})>"
