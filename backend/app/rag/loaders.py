"""
Document loaders for Polix RAG system.
"""
from typing import List, Dict, Any
from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    WebBaseLoader
)
from langchain_core.documents import Document
from app.core.logger import get_logger

logger = get_logger(__name__)


def load_pdf(file_path: str) -> List[Document]:
    """
    Load documents from a PDF file.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        List of Document objects
        
    Raises:
        FileNotFoundError: If file doesn't exist
        Exception: If loading fails
    """
    try:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        logger.info(f"Loading PDF: {file_path}")
        loader = PyPDFLoader(str(path))
        documents = loader.load()
        
        logger.info(f"Loaded {len(documents)} pages from PDF")
        return documents
        
    except Exception as e:
        logger.error(f"Error loading PDF {file_path}: {str(e)}", exc_info=True)
        raise


def load_txt(file_path: str) -> List[Document]:
    """
    Load documents from a text file.
    
    Args:
        file_path: Path to text file
        
    Returns:
        List of Document objects
        
    Raises:
        FileNotFoundError: If file doesn't exist
        Exception: If loading fails
    """
    try:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Text file not found: {file_path}")
        
        logger.info(f"Loading text file: {file_path}")
        loader = TextLoader(str(path), encoding="utf-8")
        documents = loader.load()
        
        logger.info(f"Loaded {len(documents)} documents from text file")
        return documents
        
    except Exception as e:
        logger.error(f"Error loading text file {file_path}: {str(e)}", exc_info=True)
        raise


def load_website(url: str) -> List[Document]:
    """
    Load documents from a website URL.
    
    Args:
        url: Website URL to load
        
    Returns:
        List of Document objects
        
    Raises:
        Exception: If loading fails
    """
    try:
        logger.info(f"Loading website: {url}")
        loader = WebBaseLoader(url)
        documents = loader.load()
        
        logger.info(f"Loaded {len(documents)} documents from website")
        return documents
        
    except Exception as e:
        logger.error(f"Error loading website {url}: {str(e)}", exc_info=True)
        raise


def load_document(file_path: str, file_type: str = None) -> List[Document]:
    """
    Load documents from various file types automatically.
    
    Args:
        file_path: Path to file or URL
        file_type: Optional file type hint ('pdf', 'txt', 'website')
        
    Returns:
        List of Document objects
    """
    path_str = str(file_path).lower()
    
    # Auto-detect file type if not provided
    if not file_type:
        if path_str.startswith(("http://", "https://")):
            file_type = "website"
        elif path_str.endswith(".pdf"):
            file_type = "pdf"
        elif path_str.endswith((".txt", ".md")):
            file_type = "txt"
        else:
            # Default to text
            file_type = "txt"
    
    # Load based on type
    if file_type == "pdf":
        return load_pdf(file_path)
    elif file_type == "website":
        return load_website(file_path)
    else:
        return load_txt(file_path)

