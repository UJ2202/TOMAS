"""
RFP/SOW Strategy

Execution strategy for analyzing RFP/SOW documents and generating
cloud architecture proposals.
"""

from typing import Dict, Any
from pathlib import Path
import json

def execute_rfp_sow_mode(
    denario,
    input_data: Dict[str, Any],
    mode_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute RFP/SOW analysis using Denario
    
    This adapts Denario's research workflow to analyze RFP documents
    and generate cloud architecture proposals.
    """
    
    # Extract inputs
    uploaded_files = input_data.get("uploaded_files", [])
    additional_context = input_data.get("additional_context", "")
    cloud_provider = input_data.get("cloud_provider", "AWS")
    budget = input_data.get("budget_constraint", "Not specified")
    compliance = input_data.get("compliance_requirements", [])
    llm = input_data.get("llm", "gpt-4o")
    
    results = {}
    
    try:
        # Read RFP document
        rfp_content = ""
        if uploaded_files:
            # In real implementation, parse PDF/DOCX files
            # For now, use simple text reading
            rfp_file = Path(denario.project_dir) / "input_files" / uploaded_files[0]
            if rfp_file.exists():
                if rfp_file.suffix == '.txt':
                    with open(rfp_file, 'r') as f:
                        rfp_content = f.read()
                else:
                    rfp_content = f"RFP document uploaded: {uploaded_files[0]}"
        
        # Build comprehensive data description for Denario
        data_description = f"""
# RFP/SOW Analysis Task

## Document Content
{rfp_content}

## Additional Context
{additional_context}

## Requirements
- **Cloud Provider**: {cloud_provider}
- **Budget Constraint**: ${budget}/month
- **Compliance Requirements**: {', '.join(compliance) if compliance else 'None specified'}

## Tools Available
- Cloud architecture design tools
- Cost estimation calculators
- Compliance frameworks
- Diagram generation (PlantUML, Mermaid)

## Expected Deliverables
1. Cloud architecture design optimized for {cloud_provider}
2. Detailed cost breakdown and monthly estimates
3. Implementation roadmap with phases
4. Risk assessment and mitigation strategies
5. Compliance mapping for {', '.join(compliance) if compliance else 'standard security practices'}
"""
        
        # Stage 1: Set context
        print("📄 Analyzing RFP/SOW document...")
        denario.set_data_description(data_description)
        results['data_description'] = data_description
        
        # Stage 2: Generate architecture proposal (using idea generation)
        print("🏗️ Generating cloud architecture proposal...")
        denario.get_idea(mode="fast", llm=llm, iterations=3, verbose=True)
        results['executive_summary'] = denario.research.idea
        
        # Stage 3: Develop detailed design (using methodology)
        print("📐 Developing detailed architecture design...")
        denario.get_method(mode="fast", llm=llm, verbose=True)
        results['architecture_design'] = denario.research.methodology
        
        # Stage 4: Generate cost estimates and implementation plan (using results)
        print("💰 Generating cost estimates and implementation plan...")
        denario.get_results(
            involved_agents=['engineer', 'researcher'],
            engineer_model=llm,
            researcher_model=llm,
            max_n_steps=4
        )
        results['implementation_plan'] = denario.research.results
        results['architecture_diagram'] = denario.research.plot_paths
        
        # Stage 5: Generate comprehensive report
        print("📊 Generating comprehensive proposal document...")
        denario.get_paper(llm=llm, add_citations=False)
        
        # Create cost estimate JSON
        cost_estimate = {
            "cloud_provider": cloud_provider,
            "monthly_estimate": "See implementation plan for detailed breakdown",
            "budget_constraint": budget,
            "compliance_costs": "Included in estimate",
            "breakdown": {
                "compute": "TBD - See detailed analysis",
                "storage": "TBD - See detailed analysis",
                "networking": "TBD - See detailed analysis",
                "security": "TBD - See detailed analysis",
                "monitoring": "TBD - See detailed analysis"
            }
        }
        results['cost_estimate'] = cost_estimate
        
        # Create risk assessment
        risk_assessment = """
# Risk Assessment

## Technical Risks
- See architecture design for technical considerations
- Refer to implementation plan for mitigation strategies

## Financial Risks
- Budget adherence monitoring required
- See cost estimate for detailed breakdown

## Compliance Risks
- Compliance requirements addressed in architecture
- Regular audits recommended
"""
        results['risk_assessment'] = risk_assessment
        
        results['status'] = 'success'
        results['paper_location'] = f"{denario.project_dir}/paper/"
        results['message'] = "RFP/SOW analysis completed successfully"
        
        return results
        
    except Exception as e:
        print(f"❌ Error in RFP/SOW mode: {str(e)}")
        results['status'] = 'error'
        results['error'] = str(e)
        raise e

# Register strategy with mode
from core.mode_registry import registry
mode = registry.get("rfp_sow")
if mode:
    mode.strategy = execute_rfp_sow_mode
    print("✅ RFP/SOW strategy registered")
