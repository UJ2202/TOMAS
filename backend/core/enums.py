from enum import Enum

class SessionStatus(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

class EngineType(str, Enum):
    CMBAGENT = "cmbagent"
    DENARIO = "denario"
    # Future engines
    KOSMOS = "kosmos"

class FileType(str, Enum):
    DOCUMENT = "document"  # PDF, DOCX, TXT
    DATA = "data"          # CSV, JSON, XLSX
    IMAGE = "image"        # PNG, JPG
    CODE = "code"          # PY, JS, etc.
    CONFIG = "config"      # YAML, JSON
