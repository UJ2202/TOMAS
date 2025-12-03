"""
Research Mode

Automated scientific research using Denario engine.
Generates ideas, develops methodologies, executes experiments, and writes papers.
"""

from core.mode import Mode, InputField, OutputField, ModeConfig
from core.enums import EngineType
from core.mode_registry import ModeRegistry


# Define Research Mode
research_mode = Mode(
    id="research",
    name="Scientific Research",
    description="Generate research ideas, develop methodologies, execute experiments, and write scientific papers using AI",
    engine=EngineType.DENARIO,
    icon="🔬",

    inputs=[
        InputField(
            name="data_description",
            type="textarea",
            label="Data & Tools Description",
            placeholder="Describe your research data, available tools, and computational environment...\n\nExample:\nAnalyze gravitational wave data using Python (numpy, scipy, sklearn).\nData location: /path/to/data.csv",
            required=True,
            help_text="Provide details about your research data and the tools you'll use for analysis"
        ),
        InputField(
            name="backend",
            type="select",
            label="Execution Backend",
            options=["fast", "cmbagent"],
            required=False,
            help_text="Fast: LangGraph backend (quicker), CMBAgent: Detailed planning and control (slower but more thorough)"
        ),
        InputField(
            name="journal",
            type="select",
            label="Journal Format (Optional)",
            options=["NONE", "AAS", "APS", "ICML", "NeurIPS", "JHEP", "PASJ"],
            required=False,
            help_text="Select target journal for paper formatting"
        )
    ],

    outputs=[
        OutputField(
            name="idea",
            type="markdown",
            label="Research Idea",
            description="Generated research idea and hypothesis"
        ),
        OutputField(
            name="methodology",
            type="markdown",
            label="Methodology",
            description="Detailed research methodology and experimental design"
        ),
        OutputField(
            name="results",
            type="markdown",
            label="Results",
            description="Experimental results and analysis"
        ),
        OutputField(
            name="paper",
            type="file",
            label="Research Paper",
            description="Complete research paper in PDF format"
        ),
        OutputField(
            name="plots",
            type="plot",
            label="Visualizations",
            description="Generated plots and figures"
        )
    ],

    config=ModeConfig(
        engine_config={
            "backend": "fast",  # Default backend
            "clear_project_dir": False
        },
        timeout_minutes=120,  # Research can take longer
        max_retries=2,
        allow_intervention=True,
        intervention_points=["after_idea", "after_methodology"]
    ),

    category="research",
    tags=["science", "research", "automation", "paper", "denario"],
    estimated_time="30-60 minutes",
    cost_estimate="$3-8 (depending on backend)",

    examples=[
        {
            "name": "Climate Data Analysis",
            "data_description": "Historical climate data from 1900-2020 including temperature, precipitation, and CO2 levels stored in climate_data.csv",
            "backend": "fast"
        },
        {
            "name": "Gene Expression Study",
            "data_description": "RNA-seq data from cancer vs normal tissue samples. Data files in /data/rna_seq/. Tools: Python, pandas, scikit-learn",
            "backend": "cmbagent"
        }
    ],

    tips=[
        "Provide detailed data description for better research quality",
        "Use 'cmbagent' backend for novel research requiring deep analysis",
        "Use 'fast' backend for exploratory analysis and quick iterations",
        "You can intervene after idea generation to refine the research direction",
        "Include file paths in your data description for automatic file handling"
    ]
)

# Register the mode
ModeRegistry.register(research_mode)
