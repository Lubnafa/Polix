"""
Utility functions for Polix backend.
"""
import re
import uuid
import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional
from app.core.logger import get_logger

logger = get_logger(__name__)


def generate_id(prefix: str = "polix") -> str:
    """
    Generate a unique ID for workflows, queries, etc.
    
    Args:
        prefix: Optional prefix for the ID
        
    Returns:
        Unique ID string
    """
    unique_id = str(uuid.uuid4())
    if prefix:
        return f"{prefix}_{unique_id}"
    return unique_id


def generate_timestamp() -> str:
    """
    Generate an ISO format timestamp.
    
    Returns:
        ISO format timestamp string
    """
    return datetime.now().isoformat()


def clean_text(text: str, remove_extra_whitespace: bool = True) -> str:
    """
    Clean text by removing extra whitespace and special characters.
    
    Args:
        text: Text to clean
        remove_extra_whitespace: Whether to remove extra whitespace
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    if remove_extra_whitespace:
        text = re.sub(r"\s+", " ", text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def hash_text(text: str, algorithm: str = "sha256") -> str:
    """
    Generate a hash of text.
    
    Args:
        text: Text to hash
        algorithm: Hash algorithm (md5, sha1, sha256)
        
    Returns:
        Hash string
    """
    if algorithm == "md5":
        return hashlib.md5(text.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(text.encode()).hexdigest()
    else:
        return hashlib.sha256(text.encode()).hexdigest()


def truncate_text(text: str, max_length: int = 1000, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def extract_metadata(text: str) -> Dict[str, Any]:
    """
    Extract metadata from text (simple implementation).
    
    Args:
        text: Text to extract metadata from
        
    Returns:
        Dictionary with metadata
    """
    return {
        "length": len(text),
        "word_count": len(text.split()),
        "char_count": len(text),
        "line_count": len(text.splitlines())
    }


def format_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

