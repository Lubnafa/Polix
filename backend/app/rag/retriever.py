"""
High-level retriever for Polix RAG system.
"""
from typing import List, Dict, Any
from app.rag.vectorstore import (
    similarity_search_with_score,
    get_vectorstore
)
from app.core.logger import get_logger

logger = get_logger(__name__)


def retrieve_documents(
    query: str,
    top_k: int = 5,
    score_threshold: float = 0.0,
    metadata_filter: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """
    Retrieve relevant documents for a query.
    
    Args:
        query: Query text
        top_k: Number of documents to retrieve
        score_threshold: Minimum similarity score (0.0 to 1.0)
        metadata_filter: Optional metadata filter dictionary
        
    Returns:
        List of dictionaries containing:
        - content: Document content
        - metadata: Document metadata
        - score: Similarity score (if available)
    """
    try:
        logger.info(f"Retrieving documents for query: {query}")
        
        # Perform similarity search with scores
        results = similarity_search_with_score(
            query=query,
            k=top_k,
            filter=metadata_filter
        )
        
        # Format results
        formatted_results = []
        for doc, score in results:
            # Convert score (distance) to similarity (higher is better)
            # For cosine similarity, distance = 1 - similarity
            similarity = 1.0 - score if score <= 1.0 else 1.0 / (1.0 + score)
            
            # Filter by threshold
            if similarity >= score_threshold:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": similarity
                })
        
        logger.info(
            f"Retrieved {len(formatted_results)} documents "
            f"(threshold: {score_threshold})"
        )
        return formatted_results
        
    except Exception as e:
        logger.error(f"Error retrieving documents: {str(e)}", exc_info=True)
        # Return empty list on error
        return []

