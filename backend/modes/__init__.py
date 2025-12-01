"""
Mode definitions
Import all mode files to register them with the registry
"""

# Import modes to trigger registration
from . import research
from . import rfp_sow
from . import itops

# Import strategies to attach them to modes
from strategies import research_strategy
from strategies import rfp_strategy
from strategies import itops_strategy

print("✅ All modes loaded and registered")
