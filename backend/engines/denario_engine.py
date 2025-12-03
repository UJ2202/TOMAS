"""
Denario Engine Wrapper

Wraps Denario (scientific research automation framework) with the standard IEngine interface.
Used by Research mode and scientific analysis tasks.

Denario supports two backends:
- 'fast': LangGraph backend for faster but less detailed research
- 'cmbagent': CMBAgent backend for detailed and thorough research
"""

from typing import Dict, Any, AsyncIterator, Optional, List
from pathlib import Path
import asyncio
import sys
import os

from .base import IEngine, EngineOutput

# Import Denario
sys.path.insert(0, str(Path(__file__).parent.parent / "denario"))
from denario import Denario, Research


class DenarioEngine(IEngine):
    """Wrapper for Denario with standardized interface"""

    def __init__(self):
        self.denario: Optional[Denario] = None
        self.session_id: Optional[str] = None
        self.workspace_dir: Optional[Path] = None
        self._config: Dict[str, Any] = {}
        self._pause_requested = False

    async def initialize(
        self,
        session_id: str,
        workspace_dir: str,
        config: Dict[str, Any]
    ) -> None:
        """
        Initialize Denario instance

        Args:
            session_id: Unique session identifier
            workspace_dir: Directory for this session's files
            config: Configuration including:
                - backend: 'fast' or 'cmbagent' (default: 'fast')
                - clear_project_dir: Whether to clear project directory (default: False)
        """
        self.session_id = session_id
        self.workspace_dir = Path(workspace_dir)
        self._config = config

        # Create project directory within workspace
        project_dir = self.workspace_dir / "research_project"
        project_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Research object
        research = Research()

        # Initialize Denario with the project directory
        self.denario = Denario(
            research=research,
            project_dir=str(project_dir),
            clear_project_dir=config.get("clear_project_dir", False)
        )

    async def execute(
        self,
        task: str,
        input_data: Dict[str, Any],
        mode_config: Dict[str, Any]
    ) -> AsyncIterator[EngineOutput]:
        """
        Execute research task with Denario

        The task is the data description for the research.

        Args:
            task: The data description (what data/tools are available)
            input_data: Input data including:
                - uploaded_files: Optional data files
                - parameters: Additional parameters
            mode_config: Mode configuration including:
                - backend: 'fast' or 'cmbagent'
                - llm_models: Dict of LLM models for different agents

        Yields:
            EngineOutput objects as execution progresses through research pipeline
        """
        backend = mode_config.get("backend", "fast")

        yield EngineOutput(
            status="running",
            content=f"Initializing Denario research pipeline with {backend} backend...",
            artifacts=[],
            metadata={"step": "initialization", "backend": backend}
        )

        # Set data description
        yield EngineOutput(
            status="running",
            content="Setting up research context...",
            artifacts=[],
            metadata={"step": "data_description"}
        )

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self.denario.set_data_description,
            task
        )

        # Step 1: Generate idea
        yield EngineOutput(
            status="running",
            content="Generating research idea...",
            artifacts=[],
            metadata={"step": "idea_generation", "backend": backend}
        )

        try:
            await loop.run_in_executor(
                None,
                self.denario.get_idea,
                backend  # mode parameter
            )

            idea = self.denario.research.idea
            yield EngineOutput(
                status="running",
                content=f"Research idea generated:\n\n{idea}",
                artifacts=[],
                metadata={"step": "idea_generated", "idea": idea}
            )

        except Exception as e:
            yield EngineOutput(
                status="failed",
                content=f"Failed to generate idea: {str(e)}",
                artifacts=[],
                metadata={"error": str(e), "step": "idea_generation"}
            )
            return

        # Step 2: Generate methodology
        yield EngineOutput(
            status="running",
            content="Developing research methodology...",
            artifacts=[],
            metadata={"step": "methodology", "backend": backend}
        )

        try:
            await loop.run_in_executor(
                None,
                self.denario.get_method,
                backend  # mode parameter
            )

            methodology = self.denario.research.methodology
            yield EngineOutput(
                status="running",
                content=f"Methodology developed:\n\n{methodology[:500]}..." if len(methodology) > 500 else methodology,
                artifacts=[],
                metadata={"step": "methodology_generated"}
            )

        except Exception as e:
            yield EngineOutput(
                status="failed",
                content=f"Failed to generate methodology: {str(e)}",
                artifacts=[],
                metadata={"error": str(e), "step": "methodology"}
            )
            return

        # Step 3: Execute experiments and get results
        yield EngineOutput(
            status="running",
            content="Executing research and analyzing results...",
            artifacts=[],
            metadata={"step": "results", "backend": backend}
        )

        try:
            await loop.run_in_executor(
                None,
                self.denario.get_results
            )

            results = self.denario.research.results

            # Collect plot artifacts
            plot_artifacts = []
            if hasattr(self.denario.research, 'plot_paths'):
                for plot_path in self.denario.research.plot_paths:
                    if os.path.exists(plot_path):
                        plot_artifacts.append({
                            "type": "plot",
                            "name": Path(plot_path).name,
                            "path": plot_path
                        })

            yield EngineOutput(
                status="running",
                content=f"Results obtained:\n\n{results[:500]}..." if len(results) > 500 else results,
                artifacts=plot_artifacts,
                metadata={"step": "results_generated"}
            )

        except Exception as e:
            yield EngineOutput(
                status="failed",
                content=f"Failed to get results: {str(e)}",
                artifacts=[],
                metadata={"error": str(e), "step": "results"}
            )
            return

        # Step 4: Generate paper (optional, but let's include it)
        yield EngineOutput(
            status="running",
            content="Generating research paper...",
            artifacts=[],
            metadata={"step": "paper_generation"}
        )

        try:
            await loop.run_in_executor(
                None,
                self.denario.get_paper
            )

            # Collect all artifacts
            artifacts = self._collect_artifacts()

            # Prepare final summary
            summary = f"""Research completed successfully!

**Idea:** {self.denario.research.idea}

**Methodology:** {self.denario.research.methodology[:300]}...

**Results:** {self.denario.research.results[:300]}...

Check artifacts for plots and the full research paper.
"""

            yield EngineOutput(
                status="completed",
                content=summary,
                artifacts=artifacts,
                metadata={
                    "idea": self.denario.research.idea,
                    "methodology": self.denario.research.methodology,
                    "results": self.denario.research.results,
                    "keywords": getattr(self.denario.research, 'keywords', [])
                },
                cost_info=self._calculate_cost()
            )

        except Exception as e:
            # Even if paper generation fails, we still have the research
            artifacts = self._collect_artifacts()

            yield EngineOutput(
                status="completed",
                content=f"""Research completed (paper generation encountered issues):

**Idea:** {self.denario.research.idea}

**Results:** {self.denario.research.results[:500]}...

Note: {str(e)}
""",
                artifacts=artifacts,
                metadata={
                    "idea": self.denario.research.idea,
                    "methodology": self.denario.research.methodology,
                    "results": self.denario.research.results,
                    "paper_generation_error": str(e)
                },
                cost_info=self._calculate_cost()
            )

    def _collect_artifacts(self) -> List[Dict[str, Any]]:
        """
        Collect all output artifacts (plots, papers, etc.)

        Returns:
            List of artifact dictionaries
        """
        artifacts = []

        # Collect plots
        if hasattr(self.denario.research, 'plot_paths'):
            for plot_path in self.denario.research.plot_paths:
                if os.path.exists(plot_path):
                    artifacts.append({
                        "type": "plot",
                        "name": Path(plot_path).name,
                        "path": plot_path,
                        "size": os.path.getsize(plot_path)
                    })

        # Collect generated papers and other files
        project_dir = Path(self.denario.project_dir)
        if project_dir.exists():
            # Look for PDF files (generated papers)
            for pdf_file in project_dir.rglob("*.pdf"):
                artifacts.append({
                    "type": "document",
                    "name": pdf_file.name,
                    "path": str(pdf_file),
                    "size": pdf_file.stat().st_size
                })

            # Look for markdown files (idea, method, results)
            for md_file in project_dir.rglob("*.md"):
                artifacts.append({
                    "type": "markdown",
                    "name": md_file.name,
                    "path": str(md_file),
                    "size": md_file.stat().st_size
                })

        return artifacts

    def _calculate_cost(self) -> Dict[str, Any]:
        """
        Calculate cost from Denario usage

        Returns:
            Cost information dictionary
        """
        # Denario typically uses multiple LLM calls for idea, method, results, and paper
        # This is a rough estimate
        return {
            "total_tokens": 0,  # Would need to track from LLM calls
            "cost_usd": 0.0,   # Would need actual token counts
            "note": "Cost tracking not yet implemented for Denario"
        }

    async def pause(self) -> Dict[str, Any]:
        """
        Pause execution and save checkpoint

        Returns:
            Checkpoint data for resuming
        """
        self._pause_requested = True

        # Save current research state
        checkpoint = {
            "session_id": self.session_id,
            "workspace_dir": str(self.workspace_dir),
            "state": "paused",
            "config": self._config,
            "research": {
                "data_description": self.denario.research.data_description,
                "idea": self.denario.research.idea,
                "methodology": self.denario.research.methodology,
                "results": self.denario.research.results,
                "plot_paths": getattr(self.denario.research, 'plot_paths', []),
                "keywords": getattr(self.denario.research, 'keywords', [])
            }
        }

        return checkpoint

    async def resume(self, checkpoint: Dict[str, Any]) -> None:
        """
        Resume from checkpoint

        Args:
            checkpoint: Previously saved checkpoint data
        """
        self._pause_requested = False

        # Restore session info
        self.session_id = checkpoint.get("session_id")
        self.workspace_dir = Path(checkpoint.get("workspace_dir", ""))
        self._config = checkpoint.get("config", {})

        # Reinitialize if needed
        if not self.denario:
            await self.initialize(
                self.session_id,
                str(self.workspace_dir),
                self._config
            )

        # Restore research state
        research_data = checkpoint.get("research", {})
        self.denario.research.data_description = research_data.get("data_description", "")
        self.denario.research.idea = research_data.get("idea", "")
        self.denario.research.methodology = research_data.get("methodology", "")
        self.denario.research.results = research_data.get("results", "")

        if hasattr(self.denario.research, 'plot_paths'):
            self.denario.research.plot_paths = research_data.get("plot_paths", [])
        if hasattr(self.denario.research, 'keywords'):
            self.denario.research.keywords = research_data.get("keywords", [])

    async def intervene(self, intervention: Dict[str, Any]) -> None:
        """
        Handle human intervention during research

        Args:
            intervention: Intervention data including:
                - type: 'modify_idea', 'modify_methodology', etc.
                - new_value: New value to set
        """
        intervention_type = intervention.get("type")

        if intervention_type == "modify_idea":
            new_idea = intervention.get("new_value")
            if new_idea:
                self.denario.research.idea = new_idea
                # Also update the file
                self.denario.set_idea(new_idea)

        elif intervention_type == "modify_methodology":
            new_method = intervention.get("new_value")
            if new_method:
                self.denario.research.methodology = new_method
                self.denario.set_method(new_method)

        elif intervention_type == "modify_data_description":
            new_desc = intervention.get("new_value")
            if new_desc:
                self.denario.research.data_description = new_desc
                self.denario.set_data_description(new_desc)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self.denario = None
        self._config = {}

    def get_cost_estimate(self, input_data: Dict[str, Any]) -> float:
        """
        Estimate cost for research

        Args:
            input_data: Input data to estimate cost for

        Returns:
            Estimated cost in USD
        """
        # Research typically uses significant tokens across multiple stages:
        # - Idea generation
        # - Methodology development
        # - Results analysis
        # - Paper writing

        backend = input_data.get("backend", "fast")

        # Cost estimates based on backend
        estimates = {
            "fast": 3.0,      # Faster but still substantial
            "cmbagent": 8.0   # More detailed, uses more tokens
        }

        return estimates.get(backend, 5.0)
