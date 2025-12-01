"""
ITOps Ticket Analysis Mode

Analyzes IT operations tickets to identify patterns, root causes,
and provide actionable recommendations.
"""

from core.mode import AgentMode, InputField, OutputType, InputFieldType
from core.mode_registry import registry

itops_mode = AgentMode(
    id="itops",
    name="ITOps Ticket Analysis",
    description="Analyze IT support tickets to identify patterns, root causes, and generate insights",
    category="analysis",
    icon="TicketCheck",
    inputs=[
        InputField(
            name="ticket_data",
            type=InputFieldType.FILE,
            label="Ticket Data",
            placeholder="Upload CSV or JSON file with ticket data",
            required=True,
            help_text="CSV or JSON file containing ticket information"
        ),
        InputField(
            name="analysis_focus",
            type=InputFieldType.SELECT,
            label="Analysis Focus",
            options=[
                "Pattern Detection",
                "Root Cause Analysis",
                "Trend Analysis",
                "Performance Metrics",
                "Team Analysis",
                "Comprehensive"
            ],
            default="Comprehensive",
            required=True,
            help_text="Primary focus area for the analysis"
        ),
        InputField(
            name="time_period",
            type=InputFieldType.SELECT,
            label="Time Period",
            options=["Last 7 Days", "Last 30 Days", "Last 90 Days", "Last Year", "All Time"],
            default="Last 30 Days",
            required=False,
            help_text="Time range to analyze"
        ),
        InputField(
            name="priority_filter",
            type=InputFieldType.MULTISELECT,
            label="Priority Filter",
            options=["Critical", "High", "Medium", "Low"],
            default=["Critical", "High", "Medium", "Low"],
            required=False,
            help_text="Filter tickets by priority"
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
            name="summary_report",
            type="document",
            format="md",
            description="Executive summary of ticket analysis"
        ),
        OutputType(
            name="pattern_analysis",
            type="document",
            format="md",
            description="Identified patterns and trends"
        ),
        OutputType(
            name="root_causes",
            type="document",
            format="md",
            description="Root cause analysis findings"
        ),
        OutputType(
            name="visualizations",
            type="visualization",
            format="png",
            description="Charts and graphs showing ticket metrics"
        ),
        OutputType(
            name="recommendations",
            type="document",
            format="md",
            description="Actionable recommendations for improvement"
        ),
        OutputType(
            name="metrics_data",
            type="data",
            format="json",
            description="Structured metrics and KPIs"
        )
    ],
    denario_config={
        "workflow_stages": ["data_analysis", "pattern_detection", "visualization", "recommendations"],
        "supports_fast_mode": True,
        "supports_cmbagent_mode": True
    },
    endpoint_path="/api/ticket-analysis"
)

# Register mode
registry.register(itops_mode)
