"""
ITOps Ticket Analysis Mode

Analyzes IT operations tickets using CMBAgent to identify patterns, root causes,
and provide actionable recommendations for reducing ticket volume.
"""

from core.mode import Mode, InputField, OutputField, ModeConfig
from core.enums import EngineType
from core.mode_registry import ModeRegistry


# Define ITOps Mode
itops_mode = Mode(
    id="itops",
    name="ITOps Ticket Analysis",
    description="Analyze IT operations tickets, identify patterns, root causes, and generate actionable insights",
    engine=EngineType.CMBAGENT,
    icon="🎫",

    inputs=[
        InputField(
            name="tickets_file",
            type="file",
            label="Tickets Data",
            placeholder="Upload tickets CSV/Excel",
            required=True,
            accept=".csv,.xlsx",
            help_text="Upload ticket data with columns: ID, Title, Description, Status, Priority, Category, Created, Resolved"
        ),
        InputField(
            name="time_range",
            type="select",
            label="Time Range",
            options=["Last 7 days", "Last 30 days", "Last 90 days", "Last year", "All time"],
            required=True,
            help_text="Time period to analyze"
        ),
        InputField(
            name="focus_area",
            type="select",
            label="Analysis Focus",
            options=[
                "Root Cause Analysis",
                "Pattern Detection",
                "Predictive Analysis",
                "Team Performance",
                "SLA Compliance",
                "Cost Analysis"
            ],
            required=True,
            help_text="Primary focus of the analysis"
        ),
        InputField(
            name="priority_filter",
            type="select",
            label="Priority Filter (Optional)",
            options=["All", "Critical", "High", "Medium", "Low"],
            required=False,
            help_text="Filter tickets by priority level"
        )
    ],

    outputs=[
        OutputField(
            name="summary",
            type="markdown",
            label="Executive Summary",
            description="High-level insights and key findings"
        ),
        OutputField(
            name="patterns",
            type="markdown",
            label="Identified Patterns",
            description="Recurring issues and trends in ticket data"
        ),
        OutputField(
            name="root_causes",
            type="markdown",
            label="Root Cause Analysis",
            description="Identified root causes and contributing factors"
        ),
        OutputField(
            name="recommendations",
            type="markdown",
            label="Recommendations",
            description="Actionable recommendations to reduce ticket volume"
        ),
        OutputField(
            name="dashboard",
            type="plot",
            label="Analytics Dashboard",
            description="Visual analytics and charts"
        ),
        OutputField(
            name="report",
            type="file",
            label="Full Report",
            description="Complete analysis report (if generated)"
        )
    ],

    config=ModeConfig(
        engine_config={
            "mode": "planning_and_control",
            "initial_agent": "task_improver",  # Start with data analysis agent
            "max_rounds": 12,
            "skip_rag_agents": True,
            "skip_executor": False
        },
        timeout_minutes=60,
        max_retries=2,
        allow_intervention=True,
        intervention_points=["after_pattern_detection"]
    ),

    category="operations",
    tags=["itops", "tickets", "analysis", "patterns", "operations", "cmbagent"],
    estimated_time="15-30 minutes",
    cost_estimate="$1-3",

    examples=[
        {
            "name": "Database Performance Issues",
            "time_range": "Last 90 days",
            "focus_area": "Root Cause Analysis"
        },
        {
            "name": "Support Team Efficiency",
            "time_range": "Last 30 days",
            "focus_area": "Team Performance"
        }
    ],

    tips=[
        "Ensure tickets data has consistent format for best results",
        "Include as much metadata as possible (timestamps, categories, assignees)",
        "Use Root Cause Analysis for recurring issues",
        "Use Predictive Analysis to forecast future ticket volume",
        "Filter by priority to focus on critical issues"
    ]
)

# Register the mode
ModeRegistry.register(itops_mode)
