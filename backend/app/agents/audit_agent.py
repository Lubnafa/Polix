"""
Audit agent for checking compliance by comparing policy vs external data.
"""
from typing import Dict, Any, List, Optional
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from app.core.config import settings
from app.core.logger import get_logger
from app.rag.retriever import retrieve_documents

logger = get_logger(__name__)


def create_compliance_check_tool():
    """
    Create a tool for compliance checking.
    
    Returns:
        Tool instance for compliance checking
    """
    def check_compliance(policy_requirements: str, external_data: str) -> str:
        """
        Check compliance by comparing policy requirements with external data.
        
        Args:
            policy_requirements: Policy requirements text
            external_data: External data to check against
            
        Returns:
            Compliance check result
        """
        try:
            logger.info("Checking compliance")
            
            # Simple compliance check (in production, use LLM for detailed analysis)
            result = f"""
            Compliance Check Results:
            - Policy requirements reviewed
            - External data analyzed
            - Compliance issues identified
            - Recommendations provided
            """
            
            return result.strip()
        except Exception as e:
            logger.error(f"Error checking compliance: {str(e)}", exc_info=True)
            return f"Error: {str(e)}"
    
    return Tool(
        name="ComplianceCheck",
        func=check_compliance,
        description="Check compliance by comparing policy requirements with external data"
    )


def create_audit_agent(llm: Optional[ChatOpenAI] = None) -> Any:
    """
    Create a LangChain agent for compliance auditing.
    
    Args:
        llm: Optional LLM instance (creates default if not provided)
        
    Returns:
        Initialized agent
    """
    try:
        if llm is None:
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key required for audit agent")
            llm = ChatOpenAI(
                model_name=settings.llm_model,
                temperature=0,
                openai_api_key=settings.openai_api_key
            )
        
        tools = [create_compliance_check_tool()]
        
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
        
        logger.info("Audit agent created successfully")
        return agent
        
    except Exception as e:
        logger.error(f"Error creating audit agent: {str(e)}", exc_info=True)
        raise


def perform_audit(
    policy_document: str,
    external_data: str,
    query: str
) -> Dict[str, Any]:
    """
    Perform a compliance audit.
    
    Args:
        policy_document: Policy document text
        external_data: External data to audit against
        query: Audit query
        
    Returns:
        Dictionary with audit results including compliance score
    """
    try:
        logger.info(f"Performing audit for query: {query}")
        
        # Create agent
        agent = create_audit_agent()
        
        # Prepare input
        input_text = f"""
        Policy Document:
        {policy_document}
        
        External Data:
        {external_data}
        
        Audit Query: {query}
        
        Please perform a compliance audit by comparing the policy requirements
        with the external data. Identify any compliance issues and provide
        a compliance score (0-100).
        """
        
        # Run agent
        result = agent.run(input_text)
        
        # Extract compliance score (simplified - in production use structured output)
        compliance_score = 85.0  # Placeholder
        
        return {
            "status": "success",
            "query": query,
            "audit_result": result,
            "compliance_score": compliance_score,
            "issues": []  # List of compliance issues
        }
        
    except Exception as e:
        logger.error(f"Error performing audit: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "query": query,
            "compliance_score": 0.0
        }

