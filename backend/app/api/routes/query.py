"""
RAG query endpoint for Polix backend.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.rag.retriever import retrieve_documents
from app.utils.helpers import generate_id
from app.core.logger import get_logger

router = APIRouter(prefix="/query", tags=["query"])
logger = get_logger(__name__)


class QueryRequest(BaseModel):
    """RAG query request model."""
    question: str
    top_k: Optional[int] = 5


class DocumentChunk(BaseModel):
    """Document chunk response model."""
    content: str
    metadata: dict
    score: Optional[float] = None


class QueryResponse(BaseModel):
    """RAG query response model."""
    query_id: str
    question: str
    answer: str
    documents: List[DocumentChunk]
    total_results: int


@router.post("/", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Query RAG system with user question.
    
    Args:
        request: QueryRequest containing question and optional top_k
        
    Returns:
        QueryResponse with answer and retrieved documents
        
    Raises:
        HTTPException: If query fails
    """
    try:
        query_id = generate_id()
        logger.info(f"Processing RAG query: {request.question} (ID: {query_id})")
        
        # Retrieve relevant documents
        results = retrieve_documents(
            query=request.question,
            top_k=request.top_k
        )
        
        if not results:
            return QueryResponse(
                query_id=query_id,
                question=request.question,
                answer="No relevant documents found in the knowledge base.",
                documents=[],
                total_results=0
            )
        
        # Format documents
        documents = [
            DocumentChunk(
                content=doc["content"],
                metadata=doc.get("metadata", {}),
                score=doc.get("score")
            )
            for doc in results
        ]
        
        # Generate simple answer from retrieved context
        context = "\n\n".join([doc["content"] for doc in results])
        answer = f"Based on the retrieved documents:\n\n{context[:500]}..."
        
        logger.info(f"Query {query_id} completed with {len(documents)} documents")
        
        return QueryResponse(
            query_id=query_id,
            question=request.question,
            answer=answer,
            documents=documents,
            total_results=len(documents)
        )
        
    except Exception as e:
        logger.error(f"Error processing RAG query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

