from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from core.enums import EngineType


class InputField(BaseModel):
    """Defines an input field for a mode"""
    name: str
    type: str  # "text", "textarea", "file", "select", "multiselect", "number", "checkbox"
    label: str
    placeholder: str = ""
    required: bool = True
    options: List[str] = Field(default_factory=list)
    default: Any = None
    help_text: str = ""
    accept: Optional[str] = None  # For file inputs


class OutputField(BaseModel):
    """Defines an output field for a mode"""
    name: str
    type: str  # "text", "markdown", "file", "plot", "data"
    label: str
    description: str = ""


class ModeConfig(BaseModel):
    """Configuration for mode execution"""
    engine_config: Dict[str, Any] = Field(default_factory=dict)
    timeout_minutes: int = 60
    max_retries: int = 3
    allow_intervention: bool = False
    intervention_points: List[str] = Field(default_factory=list)


class Mode(BaseModel):
    """
    Definition of a Mode

    A mode represents a specific task type with:
    - Input requirements
    - Output specifications
    - Engine selection
    - Execution configuration
    """
    id: str
    name: str
    description: str
    engine: EngineType  # Which engine to use (CMBAGENT, DENARIO, etc.)
    icon: str = "🤖"

    # Input/Output schema
    inputs: List[InputField] = Field(default_factory=list)
    outputs: List[OutputField] = Field(default_factory=list)

    # Configuration
    config: Optional[ModeConfig] = None

    # Metadata
    category: str = "general"
    tags: List[str] = Field(default_factory=list)
    estimated_time: str = "5-10 minutes"
    cost_estimate: str = "$0.10-1.00"
    examples: List[Dict[str, Any]] = Field(default_factory=list)
    tips: List[str] = Field(default_factory=list)

    class Config:
        use_enum_values = False  # Keep enum objects


# Backward compatibility alias
AgentMode = Mode
OutputType = OutputField
