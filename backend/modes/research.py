from core.mode import AgentMode, InputField, OutputType, InputFieldType
from core.mode_registry import registry

research_mode = AgentMode(
    id="research",
    name="Scientific Research",
    description="Generate research ideas, develop methodologies, execute experiments, and write scientific papers",
    category="research",
    icon="FlaskConical",
    inputs=[
        InputField(
            name="data_description",
            type=InputFieldType.TEXTAREA,
            label="Data & Tools Description",
            placeholder="Describe your research data, available tools, and computational environment...\n\nExample:\nAnalyze gravitational wave data using Python (numpy, scipy, sklearn).\nData location: /path/to/data.csv",
            required=True,
            help_text="Provide details about your research data and the tools you'll use"
        ),
        InputField(
            name="mode",
            type=InputFieldType.SELECT,
            label="Execution Mode",
            options=["fast", "cmbagent"],
            default="fast",
            required=True,
            help_text="Fast: LangGraph (quicker), CMBAgent: Detailed planning"
        ),
        InputField(
            name="llm",
            type=InputFieldType.SELECT,
            label="LLM Model",
            options=["gpt-4o", "gpt-4.1", "claude-sonnet-4", "gemini-2.0-flash", "gemini-2.5-pro"],
            default="gpt-4o",
            required=True
        ),
        InputField(
            name="journal",
            type=InputFieldType.SELECT,
            label="Journal Format",
            options=["NONE", "AAS", "APS", "ICML", "NeurIPS", "JHEP", "PASJ"],
            default="NONE",
            required=False,
            help_text="Select target journal for paper formatting"
        ),
        InputField(
            name="iterations",
            type=InputFieldType.NUMBER,
            label="Idea Iterations",
            default="4",
            required=False,
            help_text="Number of idea generation iterations"
        )
    ],
    outputs=[
        OutputType(
            name="idea",
            type="document",
            format="md",
            description="Generated research idea"
        ),
        OutputType(
            name="methodology",
            type="document",
            format="md",
            description="Detailed research methodology"
        ),
        OutputType(
            name="results",
            type="document",
            format="md",
            description="Experimental results and analysis"
        ),
        OutputType(
            name="paper",
            type="document",
            format="pdf",
            description="Research paper in LaTeX/PDF format"
        ),
        OutputType(
            name="plots",
            type="visualization",
            format="png",
            description="Generated plots and figures"
        )
    ],
    denario_config={
        "workflow_stages": ["idea", "method", "results", "paper"],
        "supports_fast_mode": True,
        "supports_cmbagent_mode": True
    },
    endpoint_path="/api/research"
)

# Register mode
registry.register(research_mode)
