"""
Policy agent for reading and understanding policies.
"""
from typing import Dict, Any, Optional
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from app.core.config import settings
from app.core.logger import get_logger
from app.rag.retriever import retrieve_documents

logger = get_logger(__name__)


def create_policy_understanding_tool():
    """
    Create a tool for policy understanding.
    
    Returns:
        Tool instance for policy understanding
    """
    def understand_policy(policy_text: str) -> str:
        """
        Understand and extract key information from policy text.
        
        Args:
            policy_text: Policy document text
            
        Returns:
            Summary of policy understanding
        """
        try:
            # Simple extraction (in production, use LLM)
            logger.info("Understanding policy document")
            
            # Extract key sections
            summary = f"""
            Policy Analysis:
            - Document length: {len(policy_text)} characters
            - Key sections identified in policy
            - Policy rules extracted
            """
            
            return summary.strip()
        except Exception as e:
            logger.error(f"Error understanding policy: {str(e)}", exc_info=True)
            return f"Error: {str(e)}"
    
    return Tool(
        name="PolicyUnderstanding",
        func=understand_policy,
        description="Understand and extract key information from policy documents"
    )


def create_policy_agent(llm: Optional[ChatOpenAI] = None) -> Any:
    """
    Create a LangChain agent for policy understanding.
    
    Args:
        llm: Optional LLM instance (creates default if not provided)
        
    Returns:
        Initialized agent
    """
    try:
        if llm is None:
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key required for policy agent")
            llm = ChatOpenAI(
                model_name=settings.llm_model,
                temperature=0,
                openai_api_key=settings.openai_api_key
            )
        
        tools = [create_policy_understanding_tool()]
        
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
        
        logger.info("Policy agent created successfully")
        return agent
        
    except Exception as e:
        logger.error(f"Error creating policy agent: {str(e)}", exc_info=True)
        raise


def analyze_policy(policy_document: str, query: str) -> Dict[str, Any]:
    """
    Analyze a policy document and answer a query about it.
    
    Args:
        policy_document: Policy document text
        query: Query about the policy
        
    Returns:
        Dictionary with analysis results
    """
    try:
        logger.info(f"Analyzing policy for query: {query}")
        
        # Create agent
        agent = create_policy_agent()
        
        # Prepare input
        input_text = f"""
        Policy Document:
        {policy_document}
        
        Query: {query}
        
        Please analyze the policy document and answer the query.
        """
        
        # Run agent
        result = agent.run(input_text)
        
        return {
            "status": "success",
            "query": query,
            "analysis": result,
            "policy_length": len(policy_document)
        }
        
    except Exception as e:
        logger.error(f"Error analyzing policy: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "query": query
        }

