"""
RFP/SOW Intelligence Mode

Analyzes RFP (Request for Proposal) and SOW (Statement of Work) documents
to generate cloud architecture proposals, cost estimates, and executive reports.
"""

from core.mode import AgentMode, InputField, OutputType, InputFieldType
from core.mode_registry import registry

rfp_sow_mode = AgentMode(
    id="rfp_sow",
    name="RFP/SOW Intelligence",
    description="Analyze RFP/SOW documents and generate cloud architecture proposals with cost estimates",
    category="analysis",
    icon="FileText",
    inputs=[
        InputField(
            name="rfp_document",
            type=InputFieldType.FILE,
            label="RFP/SOW Document",
            placeholder="Upload your RFP or SOW document (PDF, DOCX, TXT)",
            required=True,
            help_text="The Request for Proposal or Statement of Work document to analyze"
        ),
        InputField(
            name="additional_context",
            type=InputFieldType.TEXTAREA,
            label="Additional Context",
            placeholder="Provide any additional context, constraints, or requirements...",
            required=False,
            help_text="Any additional information to consider during analysis"
        ),
        InputField(
            name="cloud_provider",
            type=InputFieldType.SELECT,
            label="Cloud Provider",
            options=["AWS", "Azure", "GCP", "Multi-Cloud", "On-Premise"],
            default="AWS",
            required=True,
            help_text="Primary cloud platform for architecture design"
        ),
        InputField(
            name="budget_constraint",
            type=InputFieldType.TEXT,
            label="Budget Constraint (USD/month)",
            placeholder="e.g., 10000",
            required=False,
            help_text="Maximum monthly budget in USD"
        ),
        InputField(
            name="compliance_requirements",
            type=InputFieldType.MULTISELECT,
            label="Compliance Requirements",
            options=["SOC2", "HIPAA", "PCI-DSS", "GDPR", "FedRAMP", "ISO27001", "None"],
            default=[],
            required=False,
            help_text="Select applicable compliance frameworks"
        ),
        InputField(
            name="llm",
            type=InputFieldType.SELECT,
            label="LLM Model",
            options=["gpt-4o", "gpt-4.1", "claude-sonnet-4", "gemini-2.0-flash", "gemini-2.5-pro"],
            default="gpt-4o",
            required=True
        )
    ],
    outputs=[
        OutputType(
            name="executive_summary",
            type="document",
            format="md",
            description="Executive summary of the RFP/SOW analysis"
        ),
        OutputType(
            name="architecture_design",
            type="document",
            format="md",
            description="Detailed cloud architecture proposal"
        ),
        OutputType(
            name="architecture_diagram",
            type="visualization",
            format="png",
            description="Visual architecture diagram"
        ),
        OutputType(
            name="cost_estimate",
            type="data",
            format="json",
            description="Detailed cost breakdown and estimates"
        ),
        OutputType(
            name="implementation_plan",
            type="document",
            format="md",
            description="Phased implementation roadmap"
        ),
        OutputType(
            name="risk_assessment",
            type="document",
            format="md",
            description="Risk analysis and mitigation strategies"
        )
    ],
    denario_config={
        "workflow_stages": ["analysis", "architecture", "costing", "planning"],
        "supports_fast_mode": True,
        "supports_cmbagent_mode": True
    },
    endpoint_path="/api/rfp-analysis"
)

# Register mode
registry.register(rfp_sow_mode)
