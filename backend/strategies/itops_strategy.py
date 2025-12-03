"""
ITOps Strategy

Execution strategy for analyzing IT operations tickets
and generating insights and recommendations.
"""

from typing import Dict, Any
from pathlib import Path
import json

def execute_itops_mode(
    denario,
    input_data: Dict[str, Any],
    mode_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute ITOps ticket analysis using Denario
    
    This adapts Denario's research workflow to analyze support tickets
    and identify patterns, root causes, and generate actionable insights.
    """
    
    # Extract inputs
    uploaded_files = input_data.get("uploaded_files", [])
    analysis_focus = input_data.get("analysis_focus", "Comprehensive")
    time_period = input_data.get("time_period", "Last 30 Days")
    priority_filter = input_data.get("priority_filter", ["Critical", "High", "Medium", "Low"])
    llm = input_data.get("llm", "gpt-4o")
    
    results = {}
    
    try:
        # Read ticket data
        ticket_data = ""
        if uploaded_files:
            ticket_file = Path(denario.project_dir) / "input_files" / uploaded_files[0]
            if ticket_file.exists():
                if ticket_file.suffix == '.csv':
                    with open(ticket_file, 'r') as f:
                        ticket_data = f.read()
                elif ticket_file.suffix == '.json':
                    with open(ticket_file, 'r') as f:
                        ticket_data = json.dumps(json.load(f), indent=2)
                else:
                    with open(ticket_file, 'r') as f:
                        ticket_data = f.read()
        
        # Build data description for Denario
        data_description = f"""
# IT Operations Ticket Analysis

## Ticket Data
File: {uploaded_files[0] if uploaded_files else 'No file'}
Time Period: {time_period}
Priority Filter: {', '.join(priority_filter)}

## Data Sample
{ticket_data[:2000] if len(ticket_data) > 2000 else ticket_data}
{'... (truncated for analysis)' if len(ticket_data) > 2000 else ''}

## Analysis Focus
{analysis_focus}

## Tools Available
- Python (pandas, numpy, matplotlib, seaborn)
- Statistical analysis libraries
- Pattern detection algorithms
- Data visualization tools
- Time series analysis

## Expected Analysis
1. **Pattern Detection**: Identify recurring issues and common themes
2. **Root Cause Analysis**: Determine underlying causes of tickets
3. **Trend Analysis**: Track ticket volume, resolution times, trends over time
4. **Performance Metrics**: Calculate SLA compliance, MTTR, first response time
5. **Team Analysis**: Evaluate team performance and workload distribution
6. **Recommendations**: Provide actionable insights for improvement

## Deliverables
- Summary report with key findings
- Pattern analysis with identified trends
- Root cause analysis findings
- Visualizations (charts, graphs, dashboards)
- Actionable recommendations
- Metrics data in structured format
"""
        
        # Stage 1: Set context
        print("🎫 Analyzing ticket data...")
        denario.set_data_description(data_description)
        results['data_description'] = data_description
        
        # Stage 2: Generate analysis plan and initial insights
        print("🔍 Generating analysis insights...")
        denario.get_idea(mode="fast", llm=llm)
        results['summary_report'] = denario.research.idea
        
        # Stage 3: Develop detailed analysis methodology
        print("📊 Developing detailed analysis methodology...")
        denario.get_method(mode="fast", llm=llm, verbose=True)
        results['pattern_analysis'] = denario.research.methodology
        
        # Stage 4: Execute analysis and generate visualizations
        print("📈 Executing analysis and generating visualizations...")
        denario.get_results(
            involved_agents=['engineer', 'researcher'],
            engineer_model=llm,
            researcher_model=llm,
            max_n_steps=5
        )
        results['root_causes'] = denario.research.results
        results['visualizations'] = denario.research.plot_paths
        
        # Generate recommendations
        recommendations = """
# Recommendations for IT Operations Improvement

Based on the ticket analysis, here are actionable recommendations:

## Immediate Actions
1. Address recurring high-priority issues identified in pattern analysis
2. Implement monitoring for detected root causes
3. Review and optimize response times for critical tickets

## Short-term Improvements (1-3 months)
1. Create knowledge base articles for common issues
2. Implement automated responses for frequent low-priority tickets
3. Optimize team workload distribution based on analysis

## Long-term Strategy (3-6 months)
1. Implement preventive measures for identified root causes
2. Enhance monitoring and alerting systems
3. Conduct regular reviews of ticket trends and patterns

## Process Improvements
1. Standardize ticket categorization and prioritization
2. Improve documentation and runbooks
3. Enhance team training based on analysis findings

## Metrics to Track
- Average resolution time by priority
- First response time
- Ticket recurrence rate
- Customer satisfaction scores
- SLA compliance rate

Refer to the detailed analysis for specific insights and data-driven recommendations.
"""
        results['recommendations'] = recommendations
        
        # Create metrics data
        metrics_data = {
            "analysis_period": time_period,
            "priority_filter": priority_filter,
            "total_tickets_analyzed": "See detailed analysis",
            "key_metrics": {
                "avg_resolution_time": "See visualization data",
                "sla_compliance_rate": "See analysis results",
                "top_categories": "See pattern analysis",
                "trend_direction": "See trend analysis"
            },
            "insights": {
                "patterns_detected": "See pattern analysis section",
                "root_causes_identified": "See root cause analysis",
                "recommendations_count": "See recommendations section"
            }
        }
        results['metrics_data'] = metrics_data
        
        # Generate final report
        print("📄 Generating comprehensive analysis report...")
        denario.get_paper(llm=llm, add_citations=False)
        
        results['status'] = 'success'
        results['paper_location'] = f"{denario.project_dir}/paper/"
        results['message'] = "ITOps ticket analysis completed successfully"
        
        return results
        
    except Exception as e:
        print(f"❌ Error in ITOps mode: {str(e)}")
        results['status'] = 'error'
        results['error'] = str(e)
        raise e

# Register strategy with mode
from core.mode_registry import registry
mode = registry.get("itops")
if mode:
    mode.strategy = execute_itops_mode
    print("✅ ITOps strategy registered")
