"""
RAG module for Polix backend.
"""
from .loaders import load_document, load_pdf, load_txt, load_website
from .splitters import split_documents, split_text
from .embeddings import get_embedding_model
from .vectorstore import (
    initialize_vectorstore,
    get_vectorstore,
    add_documents,
    similarity_search,
    similarity_search_with_score
)
from .retriever import retrieve_documents

__all__ = [
    "load_document",
    "load_pdf",
    "load_txt",
    "load_website",
    "split_documents",
    "split_text",
    "get_embedding_model",
    "initialize_vectorstore",
    "get_vectorstore",
    "add_documents",
    "similarity_search",
    "similarity_search_with_score",
    "retrieve_documents"
]

