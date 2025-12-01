import sys
from pathlib import Path
from typing import Dict, Any
from core.mode_registry import registry

# Add Denario to path for imports
DENARIO_PATH = Path(__file__).parent.parent.parent.parent / "Denario"
sys.path.insert(0, str(DENARIO_PATH))

try:
    from denario import Journal
    DENARIO_AVAILABLE = True
except ImportError:
    DENARIO_AVAILABLE = False
    # Mock Journal enum
    class Journal:
        NONE = "NONE"
        AAS = "AAS"
        APS = "APS"
        ICML = "ICML"
        NeurIPS = "NeurIPS"
        JHEP = "JHEP"
        PASJ = "PASJ"

def execute_research_mode(
    denario,
    input_data: Dict[str, Any],
    mode_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute research mode using Denario's original workflow

    This is the baseline mode that uses Denario exactly as designed.
    """
    # Extract inputs
    data_description = input_data.get("data_description")
    mode = input_data.get("mode", "fast")
    llm = input_data.get("llm", "gpt-4o")
    journal_name = input_data.get("journal", "NONE")
    iterations = int(input_data.get("iterations", 4))

    results = {}

    try:
        # Stage 1: Set data description
        print("📝 Setting data description...")
        denario.set_data_description(data_description)
        results['data_description'] = data_description

        # Stage 2: Generate idea
        print("💡 Generating research idea...")
        denario.get_idea(mode=mode, llm=llm, iterations=iterations, verbose=True)
        results['idea'] = denario.research.idea

        # Stage 3: Check idea novelty (optional, can be slow)
        # print("🔍 Checking idea novelty...")
        # denario.check_idea(mode="semantic_scholar", llm=llm)

        # Stage 4: Generate methodology
        print("🔬 Developing methodology...")
        denario.get_method(mode=mode, llm=llm, verbose=True)
        results['methodology'] = denario.research.methodology

        # Stage 5: Execute experiments
        print("⚙️ Executing experiments...")
        denario.get_results(
            involved_agents=['engineer', 'researcher'],
            engineer_model=llm,
            researcher_model=llm
        )
        results['results'] = denario.research.results
        results['plots'] = denario.research.plot_paths

        # Stage 6: Generate paper
        print("📄 Generating paper...")
        journal = Journal[journal_name] if journal_name != "NONE" else Journal.NONE
        denario.get_paper(journal=journal, llm=llm, add_citations=True)

        results['status'] = 'success'
        results['paper_location'] = f"{denario.project_dir}/paper/"
        results['message'] = "Research workflow completed successfully"

        return results

    except Exception as e:
        print(f"❌ Error in research mode: {str(e)}")
        results['status'] = 'error'
        results['error'] = str(e)
        raise e

# Register strategy with mode
mode = registry.get("research")
if mode:
    mode.strategy = execute_research_mode
    print("✅ Research strategy registered")
