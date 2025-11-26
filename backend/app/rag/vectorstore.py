"""
Vector store management for Polix RAG system.
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from app.rag.embeddings import get_embedding_model
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

# Global vector store instance
_vector_store = None
_embedding_model = None


def initialize_vectorstore() -> None:
    """
    Initialize the vector store based on configuration.
    
    Creates the vector store directory if it doesn't exist.
    """
    global _vector_store, _embedding_model
    
    try:
        # Ensure vector store directory exists
        vector_store_path = Path(settings.vector_store_path)
        vector_store_path.mkdir(parents=True, exist_ok=True)
        
        # Get embedding model
        _embedding_model = get_embedding_model()
        
        # Initialize vector store based on type
        if settings.vector_store_type.lower() == "chromadb":
            logger.info(f"Initializing ChromaDB at: {vector_store_path}")
            _vector_store = Chroma(
                persist_directory=str(vector_store_path),
                embedding_function=_embedding_model,
                collection_name="polix_documents"
            )
        else:
            logger.info(f"Initializing FAISS at: {vector_store_path}")
            # FAISS needs an index file, check if it exists
            index_path = vector_store_path / "faiss_index"
            if index_path.exists():
                _vector_store = FAISS.load_local(
                    str(vector_store_path),
                    _embedding_model,
                    allow_dangerous_deserialization=True
                )
            else:
                # Create new FAISS store
                _vector_store = FAISS.from_texts(
                    [""],  # Dummy text to initialize
                    _embedding_model
                )
                _vector_store.save_local(str(vector_store_path))
        
        logger.info("Vector store initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing vector store: {str(e)}", exc_info=True)
        raise


def get_vectorstore():
    """
    Get the global vector store instance.
    
    Returns:
        Vector store instance
        
    Raises:
        RuntimeError: If vector store not initialized
    """
    global _vector_store
    
    if _vector_store is None:
        initialize_vectorstore()
    
    return _vector_store


def add_documents(documents: List[Document]) -> List[str]:
    """
    Add documents to the vector store.
    
    Args:
        documents: List of Document objects to add
        
    Returns:
        List of document IDs
    """
    try:
        vector_store = get_vectorstore()
        logger.info(f"Adding {len(documents)} documents to vector store")
        
        # Add documents to vector store
        ids = vector_store.add_documents(documents)
        
        # Persist if ChromaDB
        if settings.vector_store_type.lower() == "chromadb":
            vector_store.persist()
        
        logger.info(f"Successfully added {len(ids)} documents")
        return ids
        
    except Exception as e:
        logger.error(f"Error adding documents: {str(e)}", exc_info=True)
        raise


def similarity_search(
    query: str,
    k: int = 5,
    filter: Optional[Dict[str, Any]] = None
) -> List[Document]:
    """
    Perform similarity search in vector store.
    
    Args:
        query: Query text
        k: Number of results to return
        filter: Optional metadata filter
        
    Returns:
        List of similar Document objects
    """
    try:
        vector_store = get_vectorstore()
        logger.info(f"Performing similarity search: {query} (k={k})")
        
        if filter:
            results = vector_store.similarity_search(
                query,
                k=k,
                filter=filter
            )
        else:
            results = vector_store.similarity_search(query, k=k)
        
        logger.info(f"Found {len(results)} similar documents")
        return results
        
    except Exception as e:
        logger.error(f"Error in similarity search: {str(e)}", exc_info=True)
        raise


def similarity_search_with_score(
    query: str,
    k: int = 5,
    filter: Optional[Dict[str, Any]] = None
) -> List[tuple]:
    """
    Perform similarity search with relevance scores.
    
    Args:
        query: Query text
        k: Number of results to return
        filter: Optional metadata filter
        
    Returns:
        List of tuples (Document, score)
    """
    try:
        vector_store = get_vectorstore()
        logger.info(f"Performing similarity search with scores: {query} (k={k})")
        
        if filter:
            results = vector_store.similarity_search_with_score(
                query,
                k=k,
                filter=filter
            )
        else:
            results = vector_store.similarity_search_with_score(query, k=k)
        
        logger.info(f"Found {len(results)} similar documents with scores")
        return results
        
    except Exception as e:
        logger.error(f"Error in similarity search with score: {str(e)}", exc_info=True)
        raise

