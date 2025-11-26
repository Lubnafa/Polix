"""
Text splitters for Polix RAG system.
"""
from typing import List
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter
)
from langchain_core.documents import Document
from app.core.logger import get_logger

logger = get_logger(__name__)


def split_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    splitter_type: str = "recursive"
) -> List[Document]:
    """
    Split documents into chunks for RAG.
    
    Args:
        documents: List of Document objects to split
        chunk_size: Maximum size of each chunk in characters
        chunk_overlap: Number of characters to overlap between chunks
        splitter_type: Type of splitter ('recursive' or 'character')
        
    Returns:
        List of split Document chunks
    """
    try:
        logger.info(f"Splitting {len(documents)} documents into chunks")
        
        if splitter_type == "recursive":
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
        else:
            text_splitter = CharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len
            )
        
        chunks = text_splitter.split_documents(documents)
        
        logger.info(f"Created {len(chunks)} document chunks")
        return chunks
        
    except Exception as e:
        logger.error(f"Error splitting documents: {str(e)}", exc_info=True)
        raise


def split_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[str]:
    """
    Split a single text string into chunks.
    
    Args:
        text: Text to split
        chunk_size: Maximum size of each chunk
        chunk_overlap: Number of characters to overlap
        
    Returns:
        List of text chunks
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        
        chunks = text_splitter.split_text(text)
        return chunks
        
    except Exception as e:
        logger.error(f"Error splitting text: {str(e)}", exc_info=True)
        raise

