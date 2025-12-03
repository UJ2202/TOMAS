"""
Alembic Base - Provides Base and metadata for migrations
Imports Base from core.database to ensure models are using the same Base
"""

# Import Base from the actual database module
from core.database import Base

# Import all models to register them with Base's metadata
from models.session import Session
from models.message import Message
from models.file import SessionFile
from models.config import UserConfig
from models.cost import CostRecord

# Export metadata for Alembic
target_metadata = Base.metadata
