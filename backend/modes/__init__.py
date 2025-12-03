"""
Mode Definitions

Import all mode files to register them with the ModeRegistry.
Modes are automatically registered when imported.
"""

# Import modes to trigger registration
from . import research
from . import rfp_sow
from . import itops

print("✅ All modes loaded and registered with ModeRegistry")

__all__ = ['research', 'rfp_sow', 'itops']
