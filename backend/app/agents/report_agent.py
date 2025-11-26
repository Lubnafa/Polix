"""
Report agent for generating final audit summaries.
"""
from typing import Dict, Any, List, Optional
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


def create_report_generation_tool():
    """
    Create a tool for report generation.
    
    Returns:
        Tool instance for report generation
    """
    def generate_report(audit_data: str) -> str:
        """
        Generate a comprehensive audit report.
        
        Args:
            audit_data: Audit data and results
            
        Returns:
            Generated report text
        """
        try:
            logger.info("Generating audit report")
            
            # Simple report generation (in production, use LLM)
            report = f"""
            Audit Report
            ============
            
            {audit_data}
            
            Summary:
            - Audit completed successfully
            - Compliance issues documented
            - Recommendations provided
            """
            
            return report.strip()
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}", exc_info=True)
            return f"Error: {str(e)}"
    
    return Tool(
        name="ReportGeneration",
        func=generate_report,
        description="Generate comprehensive audit reports from audit data"
    )


def create_report_agent(llm: Optional[ChatOpenAI] = None) -> Any:
    """
    Create a LangChain agent for report generation.
    
    Args:
        llm: Optional LLM instance (creates default if not provided)
        
    Returns:
        Initialized agent
    """
    try:
        if llm is None:
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key required for report agent")
            llm = ChatOpenAI(
                model_name=settings.llm_model,
                temperature=0.7,  # Higher temperature for more creative reports
                openai_api_key=settings.openai_api_key
            )
        
        tools = [create_report_generation_tool()]
        
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
        
        logger.info("Report agent created successfully")
        return agent
        
    except Exception as e:
        logger.error(f"Error creating report agent: {str(e)}", exc_info=True)
        raise


def generate_final_report(
    audit_results: Dict[str, Any],
    policy_summary: str,
    compliance_score: float
) -> Dict[str, Any]:
    """
    Generate a final audit report.
    
    Args:
        audit_results: Audit results dictionary
        policy_summary: Summary of policy analysis
        compliance_score: Compliance score (0-100)
        
    Returns:
        Dictionary with final report
    """
    try:
        logger.info("Generating final audit report")
        
        # Create agent
        agent = create_report_agent()
        
        # Prepare input
        input_text = f"""
        Policy Summary:
        {policy_summary}
        
        Audit Results:
        {audit_results}
        
        Compliance Score: {compliance_score}/100
        
        Please generate a comprehensive final audit report that includes:
        1. Executive summary
        2. Policy analysis summary
        3. Compliance findings
        4. Recommendations
        5. Next steps
        """
        
        # Run agent
        report_text = agent.run(input_text)
        
        return {
            "status": "success",
            "report": report_text,
            "compliance_score": compliance_score,
            "summary": policy_summary
        }
        
    except Exception as e:
        logger.error(f"Error generating final report: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "report": "Failed to generate report"
        }

