"""
Agent workflow endpoint for Polix backend.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from app.graph.workflow_graph import create_workflow_graph
from app.core.logger import get_logger
from app.utils.helpers import generate_id

router = APIRouter(prefix="/agent", tags=["agent"])
logger = get_logger(__name__)


class AgentRequest(BaseModel):
    """Agent workflow request model."""
    query: str
    policy_document: Optional[str] = None
    external_data_source: Optional[str] = None


class AgentStep(BaseModel):
    """Individual agent step model."""
    step_id: str
    agent_name: str
    status: str
    result: Optional[Dict[str, Any]] = None
    timestamp: str


class AgentResponse(BaseModel):
    """Agent workflow response model."""
    workflow_id: str
    status: str
    steps: List[AgentStep]
    final_report: Optional[str] = None
    compliance_score: Optional[float] = None


@router.post("/audit", response_model=AgentResponse)
async def trigger_audit_workflow(
    request: AgentRequest,
    background_tasks: BackgroundTasks
):
    """
    Trigger LangGraph workflow for compliance audits.
    
    Args:
        request: AgentRequest with query and optional policy/external data
        background_tasks: FastAPI background tasks
        
    Returns:
        AgentResponse with workflow status and steps
        
    Raises:
        HTTPException: If workflow fails to start
    """
    try:
        workflow_id = generate_id()
        logger.info(f"Starting audit workflow: {workflow_id}")
        
        # Create workflow graph
        graph = create_workflow_graph()
        
        # Prepare initial state
        initial_state = {
            "query": request.query,
            "policy_document": request.policy_document,
            "external_data_source": request.external_data_source,
            "workflow_id": workflow_id,
            "steps": [],
            "status": "running"
        }
        
        # Execute workflow (simplified - in production, run async)
        try:
            # Compile graph
            app = graph.compile()
            
            # Run workflow
            final_state = app.invoke(initial_state)
            
            # Format response
            steps = [
                AgentStep(
                    step_id=step.get("step_id", ""),
                    agent_name=step.get("agent_name", ""),
                    status=step.get("status", "completed"),
                    result=step.get("result"),
                    timestamp=step.get("timestamp", "")
                )
                for step in final_state.get("steps", [])
            ]
            
            return AgentResponse(
                workflow_id=workflow_id,
                status=final_state.get("status", "completed"),
                steps=steps,
                final_report=final_state.get("final_report"),
                compliance_score=final_state.get("compliance_score")
            )
            
        except Exception as e:
            logger.error(f"Workflow execution error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Workflow execution failed: {str(e)}"
            )
        
    except Exception as e:
        logger.error(f"Error starting audit workflow: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start workflow: {str(e)}"
        )

