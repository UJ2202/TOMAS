"""
RFP/SOW Intelligence Mode

Analyzes RFP (Request for Proposal) and SOW (Statement of Work) documents using CMBAgent
to generate cloud architecture proposals, cost estimates, and implementation plans.
"""

from core.mode import Mode, InputField, OutputField, ModeConfig
from core.enums import EngineType
from core.mode_registry import ModeRegistry


# Define RFP/SOW Mode
rfp_sow_mode = Mode(
    id="rfp_sow",
    name="RFP/SOW Analysis",
    description="Analyze RFP documents and generate technical proposals with architecture diagrams, cost estimates, and SOW",
    engine=EngineType.CMBAGENT,
    icon="📄",

    inputs=[
        InputField(
            name="rfp_document",
            type="file",
            label="RFP Document",
            placeholder="Upload RFP document",
            required=True,
            accept=".pdf,.docx,.txt",
            help_text="Upload the RFP or requirements document to analyze"
        ),
        InputField(
            name="cloud_provider",
            type="select",
            label="Preferred Cloud Provider",
            options=["AWS", "Azure", "GCP", "Multi-Cloud", "On-Premise"],
            required=True,
            help_text="Select the primary cloud platform for architecture design"
        ),
        InputField(
            name="budget_range",
            type="text",
            label="Budget Range (Optional)",
            placeholder="e.g., $50K-$100K",
            required=False,
            help_text="Specify budget constraints for cost optimization"
        ),
        InputField(
            name="timeline",
            type="text",
            label="Timeline (Optional)",
            placeholder="e.g., 6 months",
            required=False,
            help_text="Expected project timeline"
        ),
        InputField(
            name="focus_areas",
            type="textarea",
            label="Specific Focus Areas (Optional)",
            placeholder="e.g., Security, Scalability, Cost optimization",
            required=False,
            help_text="Highlight specific areas to focus on in the analysis"
        )
    ],

    outputs=[
        OutputField(
            name="requirements_analysis",
            type="markdown",
            label="Requirements Analysis",
            description="Parsed and analyzed requirements from RFP"
        ),
        OutputField(
            name="architecture",
            type="markdown",
            label="Proposed Architecture",
            description="Technical architecture and design recommendations"
        ),
        OutputField(
            name="architecture_diagram",
            type="file",
            label="Architecture Diagram",
            description="Visual architecture diagram (if generated)"
        ),
        OutputField(
            name="cost_estimate",
            type="json",
            label="Cost Breakdown",
            description="Detailed cost estimates by component"
        ),
        OutputField(
            name="sow",
            type="file",
            label="Statement of Work",
            description="Complete SOW document"
        ),
        OutputField(
            name="risks",
            type="markdown",
            label="Risk Analysis",
            description="Identified risks and mitigation strategies"
        )
    ],

    config=ModeConfig(
        engine_config={
            "mode": "planning_and_control",
            "initial_agent": "task_improver",  # CMBAgent will improve the task first
            "max_rounds": 15,
            "skip_rag_agents": True,
            "skip_executor": False
        },
        timeout_minutes=90,
        max_retries=2,
        allow_intervention=True,
        intervention_points=["after_requirements", "after_architecture"]
    ),

    category="consulting",
    tags=["rfp", "sow", "architecture", "cloud", "consulting", "cmbagent"],
    estimated_time="20-40 minutes",
    cost_estimate="$2-4",

    examples=[
        {
            "name": "Microservices Migration",
            "cloud_provider": "AWS",
            "description": "RFP for migrating monolithic application to microservices architecture"
        },
        {
            "name": "Data Platform Build",
            "cloud_provider": "GCP",
            "description": "Building enterprise data platform with real-time analytics"
        }
    ],

    tips=[
        "Ensure RFP document is clear and well-formatted for best results",
        "Specify budget range for more accurate cost estimates",
        "You can intervene to adjust architecture before cost estimation",
        "Multi-cloud option will provide comparison across providers",
        "Include specific compliance requirements in focus areas if needed"
    ]
)

# Register the mode
ModeRegistry.register(rfp_sow_mode)
