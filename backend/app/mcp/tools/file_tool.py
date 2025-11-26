"""
MCP tool for local file system access.
"""
import os
from typing import Dict, Any, Optional, List
from pathlib import Path
from app.core.logger import get_logger

logger = get_logger(__name__)


def read_file(file_path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """
    Read content from a local file.
    
    Args:
        file_path: Path to file
        encoding: File encoding (default: utf-8)
        
    Returns:
        Dictionary with file content
    """
    try:
        logger.info(f"Reading file: {file_path}")
        
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        # Check file size (limit to 10MB)
        file_size = path.stat().st_size
        max_size = 10 * 1024 * 1024  # 10MB
        
        if file_size > max_size:
            raise ValueError(f"File too large: {file_size} bytes (max: {max_size})")
        
        with open(path, "r", encoding=encoding) as f:
            content = f.read()
        
        return {
            "status": "success",
            "file_path": str(path),
            "content": content,
            "size": len(content),
            "file_size": file_size
        }
        
    except Exception as e:
        logger.error(f"Error reading file: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "file_path": file_path
        }


def list_directory(directory_path: str, recursive: bool = False) -> Dict[str, Any]:
    """
    List files and directories in a local directory.
    
    Args:
        directory_path: Path to directory
        recursive: Whether to list recursively
        
    Returns:
        Dictionary with directory listing
    """
    try:
        logger.info(f"Listing directory: {directory_path}")
        
        path = Path(directory_path)
        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {directory_path}")
        
        files = []
        directories = []
        
        if recursive:
            for root, dirs, filenames in os.walk(path):
                # Filter out hidden directories
                dirs[:] = [d for d in dirs if not d.startswith(".")]
                
                for filename in filenames:
                    if not filename.startswith("."):
                        file_path = Path(root) / filename
                        rel_path = file_path.relative_to(path)
                        files.append({
                            "name": filename,
                            "path": str(rel_path),
                            "full_path": str(file_path),
                            "size": file_path.stat().st_size
                        })
                
                for dirname in dirs:
                    dir_path = Path(root) / dirname
                    rel_path = dir_path.relative_to(path)
                    directories.append({
                        "name": dirname,
                        "path": str(rel_path),
                        "full_path": str(dir_path)
                    })
        else:
            for item in path.iterdir():
                if item.name.startswith("."):
                    continue
                
                if item.is_file():
                    files.append({
                        "name": item.name,
                        "path": str(item.relative_to(path)),
                        "full_path": str(item),
                        "size": item.stat().st_size
                    })
                elif item.is_dir():
                    directories.append({
                        "name": item.name,
                        "path": str(item.relative_to(path)),
                        "full_path": str(item)
                    })
        
        return {
            "status": "success",
            "directory_path": str(path),
            "files": files,
            "directories": directories,
            "total_files": len(files),
            "total_directories": len(directories)
        }
        
    except Exception as e:
        logger.error(f"Error listing directory: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "directory_path": directory_path
        }


class FileTool:
    """
    MCP tool for local file system operations.
    """
    
    def read_file(self, file_path: str) -> Dict[str, Any]:
        """
        Read a local file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary with file content
        """
        return read_file(file_path)
    
    def list_directory(self, directory_path: str, recursive: bool = False) -> Dict[str, Any]:
        """
        List directory contents.
        
        Args:
            directory_path: Path to directory
            recursive: Whether to list recursively
            
        Returns:
            Dictionary with directory listing
        """
        return list_directory(directory_path, recursive)
    
    def read_directory(self, directory_path: str, file_extensions: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Read all files in a directory matching extensions.
        
        Args:
            directory_path: Path to directory
            file_extensions: Optional list of file extensions to filter
            
        Returns:
            Dictionary with all file contents
        """
        try:
            listing = list_directory(directory_path, recursive=True)
            
            if listing["status"] != "success":
                return listing
            
            files_content = []
            for file_info in listing["files"]:
                file_path = file_info["full_path"]
                
                # Filter by extension if provided
                if file_extensions:
                    if not any(file_path.endswith(ext) for ext in file_extensions):
                        continue
                
                # Read file content
                file_result = read_file(file_path)
                if file_result["status"] == "success":
                    files_content.append({
                        "path": file_info["path"],
                        "content": file_result["content"]
                    })
            
            return {
                "status": "success",
                "directory_path": directory_path,
                "files": files_content,
                "total_files": len(files_content)
            }
            
        except Exception as e:
            logger.error(f"Error reading directory: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "directory_path": directory_path
            }

