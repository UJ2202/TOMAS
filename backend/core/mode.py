from pydantic import BaseModel
from typing import List, Dict, Any, Callable, Optional
from enum import Enum

class InputFieldType(str, Enum):
    """Types of input fields"""
    TEXT = "text"
    TEXTAREA = "textarea"
    FILE = "file"
    SELECT = "select"
    MULTISELECT = "multiselect"
    NUMBER = "number"
    CHECKBOX = "checkbox"

class InputField(BaseModel):
    """Defines an input field for a mode"""
    name: str
    type: InputFieldType
    label: str
    placeholder: str = ""
    required: bool = True
    options: List[str] = []
    default: Any = None
    help_text: str = ""

class OutputType(BaseModel):
    """Defines an output type for a mode"""
    name: str
    type: str  # 'document', 'visualization', 'data', 'code'
    format: str  # 'pdf', 'md', 'png', 'json', 'py', etc.
    description: str
    mime_type: str = ""

class AgentMode(BaseModel):
    """
    Definition of an Agent Mode

    A mode represents a specific task type with:
    - Input requirements
    - Output specifications
    - Execution strategy
    """
    id: str
    name: str
    description: str
    category: str  # 'research', 'analysis', 'generation', 'automation'
    icon: str  # Lucide icon name

    # Input/Output schema
    inputs: List[InputField]
    outputs: List[OutputType]

    # Configuration
    denario_config: Dict[str, Any] = {}

    # Future API endpoint
    endpoint_path: str

    # Execution strategy (set programmatically)
    strategy: Optional[Callable] = None

    class Config:
        arbitrary_types_allowed = True
