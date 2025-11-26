"""
LangGraph workflow for Polix compliance audit system.
"""
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from datetime import datetime
from app.agents.policy_agent import analyze_policy
from app.agents.audit_agent import perform_audit
from app.agents.report_agent import generate_final_report
from app.rag.retriever import retrieve_documents
from app.core.logger import get_logger

logger = get_logger(__name__)


class WorkflowState(TypedDict):
    """State definition for the workflow graph."""
    query: str
    policy_document: str
    external_data_source: str
    workflow_id: str
    status: str
    steps: list
    policy_summary: str
    audit_results: dict
    compliance_score: float
    final_report: str
    approval_required: bool
    approved: bool


def policy_ingestion_node(state: WorkflowState) -> WorkflowState:
    """
    Node for policy document ingestion and analysis.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with policy analysis
    """
    try:
        logger.info(f"Policy ingestion node: {state['workflow_id']}")
        
        step = {
            "step_id": f"policy_{datetime.now().isoformat()}",
            "agent_name": "policy_agent",
            "status": "running",
            "timestamp": datetime.now().isoformat()
        }
        
        # Analyze policy document
        if state.get("policy_document"):
            policy_result = analyze_policy(
                policy_document=state["policy_document"],
                query=state["query"]
            )
            
            step["status"] = "completed"
            step["result"] = policy_result
            
            state["steps"].append(step)
            state["policy_summary"] = policy_result.get("analysis", "")
        else:
            step["status"] = "skipped"
            step["result"] = {"message": "No policy document provided"}
            state["steps"].append(step)
            state["policy_summary"] = "No policy document provided"
        
        return state
        
    except Exception as e:
        logger.error(f"Error in policy ingestion node: {str(e)}", exc_info=True)
        state["steps"].append({
            "step_id": f"policy_error_{datetime.now().isoformat()}",
            "agent_name": "policy_agent",
            "status": "error",
            "result": {"error": str(e)},
            "timestamp": datetime.now().isoformat()
        })
        state["status"] = "error"
        return state


def rag_retrieval_node(state: WorkflowState) -> WorkflowState:
    """
    Node for RAG retrieval of relevant documents.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with retrieved documents
    """
    try:
        logger.info(f"RAG retrieval node: {state['workflow_id']}")
        
        step = {
            "step_id": f"rag_{datetime.now().isoformat()}",
            "agent_name": "rag_retriever",
            "status": "running",
            "timestamp": datetime.now().isoformat()
        }
        
        # Retrieve relevant documents
        retrieved_docs = retrieve_documents(
            query=state["query"],
            top_k=5
        )
        
        step["status"] = "completed"
        step["result"] = {
            "documents_found": len(retrieved_docs),
            "documents": retrieved_docs
        }
        
        state["steps"].append(step)
        
        # Store retrieved documents in external_data_source if not already set
        if not state.get("external_data_source"):
            state["external_data_source"] = "\n\n".join(
                [doc["content"] for doc in retrieved_docs]
            )
        
        return state
        
    except Exception as e:
        logger.error(f"Error in RAG retrieval node: {str(e)}", exc_info=True)
        state["steps"].append({
            "step_id": f"rag_error_{datetime.now().isoformat()}",
            "agent_name": "rag_retriever",
            "status": "error",
            "result": {"error": str(e)},
            "timestamp": datetime.now().isoformat()
        })
        return state


def audit_check_node(state: WorkflowState) -> WorkflowState:
    """
    Node for compliance audit check.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with audit results
    """
    try:
        logger.info(f"Audit check node: {state['workflow_id']}")
        
        step = {
            "step_id": f"audit_{datetime.now().isoformat()}",
            "agent_name": "audit_agent",
            "status": "running",
            "timestamp": datetime.now().isoformat()
        }
        
        # Perform audit
        audit_result = perform_audit(
            policy_document=state.get("policy_document", ""),
            external_data=state.get("external_data_source", ""),
            query=state["query"]
        )
        
        step["status"] = "completed"
        step["result"] = audit_result
        
        state["steps"].append(step)
        state["audit_results"] = audit_result
        state["compliance_score"] = audit_result.get("compliance_score", 0.0)
        
        return state
        
    except Exception as e:
        logger.error(f"Error in audit check node: {str(e)}", exc_info=True)
        state["steps"].append({
            "step_id": f"audit_error_{datetime.now().isoformat()}",
            "agent_name": "audit_agent",
            "status": "error",
            "result": {"error": str(e)},
            "timestamp": datetime.now().isoformat()
        })
        state["compliance_score"] = 0.0
        return state


def report_generation_node(state: WorkflowState) -> WorkflowState:
    """
    Node for generating final audit report.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with final report
    """
    try:
        logger.info(f"Report generation node: {state['workflow_id']}")
        
        step = {
            "step_id": f"report_{datetime.now().isoformat()}",
            "agent_name": "report_agent",
            "status": "running",
            "timestamp": datetime.now().isoformat()
        }
        
        # Generate final report
        report_result = generate_final_report(
            audit_results=state.get("audit_results", {}),
            policy_summary=state.get("policy_summary", ""),
            compliance_score=state.get("compliance_score", 0.0)
        )
        
        step["status"] = "completed"
        step["result"] = report_result
        
        state["steps"].append(step)
        state["final_report"] = report_result.get("report", "")
        state["approval_required"] = True
        
        return state
        
    except Exception as e:
        logger.error(f"Error in report generation node: {str(e)}", exc_info=True)
        state["steps"].append({
            "step_id": f"report_error_{datetime.now().isoformat()}",
            "agent_name": "report_agent",
            "status": "error",
            "result": {"error": str(e)},
            "timestamp": datetime.now().isoformat()
        })
        return state


def human_approval_node(state: WorkflowState) -> WorkflowState:
    """
    Node for human approval event (placeholder for future implementation).
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with approval status
    """
    try:
        logger.info(f"Human approval node: {state['workflow_id']}")
        
        step = {
            "step_id": f"approval_{datetime.now().isoformat()}",
            "agent_name": "human_approval",
            "status": "pending",
            "timestamp": datetime.now().isoformat()
        }
        
        # For now, auto-approve (in production, implement actual approval workflow)
        state["approved"] = True
        step["status"] = "approved"
        step["result"] = {"approved": True, "message": "Auto-approved in demo mode"}
        
        state["steps"].append(step)
        state["status"] = "completed"
        
        return state
        
    except Exception as e:
        logger.error(f"Error in human approval node: {str(e)}", exc_info=True)
        state["steps"].append({
            "step_id": f"approval_error_{datetime.now().isoformat()}",
            "agent_name": "human_approval",
            "status": "error",
            "result": {"error": str(e)},
            "timestamp": datetime.now().isoformat()
        })
        return state


def create_workflow_graph() -> StateGraph:
    """
    Create the LangGraph workflow graph.
    
    Returns:
        StateGraph instance representing the workflow
    """
    try:
        logger.info("Creating workflow graph")
        
        # Create state graph
        workflow = StateGraph(WorkflowState)
        
        # Add nodes
        workflow.add_node("policy_ingestion", policy_ingestion_node)
        workflow.add_node("rag_retrieval", rag_retrieval_node)
        workflow.add_node("audit_check", audit_check_node)
        workflow.add_node("report_generation", report_generation_node)
        workflow.add_node("human_approval", human_approval_node)
        
        # Define edges
        workflow.set_entry_point("policy_ingestion")
        workflow.add_edge("policy_ingestion", "rag_retrieval")
        workflow.add_edge("rag_retrieval", "audit_check")
        workflow.add_edge("audit_check", "report_generation")
        workflow.add_edge("report_generation", "human_approval")
        workflow.add_edge("human_approval", END)
        
        logger.info("Workflow graph created successfully")
        return workflow
        
    except Exception as e:
        logger.error(f"Error creating workflow graph: {str(e)}", exc_info=True)
        raise

