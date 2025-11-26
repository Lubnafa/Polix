"""
MCP tool for GitHub repository access.
"""
import os
import subprocess
import tempfile
import shutil
from typing import Dict, Any, Optional, List
from pathlib import Path
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


def clone_github_repo(
    repo_url: str,
    branch: Optional[str] = None,
    local_path: Optional[str] = None
) -> str:
    """
    Clone a GitHub repository to a local path.
    
    Args:
        repo_url: GitHub repository URL
        branch: Optional branch name (defaults to main)
        local_path: Optional local path to clone to
        
    Returns:
        Path to cloned repository
    """
    try:
        logger.info(f"Cloning repository: {repo_url}")
        
        # Create temporary directory if not specified
        if not local_path:
            temp_dir = tempfile.mkdtemp(prefix="polix_github_")
            local_path = os.path.join(temp_dir, Path(repo_url).stem)
        else:
            os.makedirs(local_path, exist_ok=True)
        
        # Prepare git command
        cmd = ["git", "clone"]
        if branch:
            cmd.extend(["-b", branch])
        cmd.extend([repo_url, local_path])
        
        # Execute git clone
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        logger.info(f"Repository cloned to: {local_path}")
        return local_path
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error cloning repository: {str(e)}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Unexpected error cloning repository: {str(e)}", exc_info=True)
        raise


def read_github_repo(repo_url: str, file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Read code content from a GitHub repository.
    
    Args:
        repo_url: GitHub repository URL
        file_path: Optional specific file path to read
        
    Returns:
        Dictionary with repository content
    """
    try:
        logger.info(f"Reading GitHub repository: {repo_url}")
        
        # Clone repository temporarily
        temp_path = None
        try:
            temp_path = clone_github_repo(repo_url)
            
            if file_path:
                # Read specific file
                full_path = os.path.join(temp_path, file_path)
                if os.path.exists(full_path):
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    return {
                        "repo_url": repo_url,
                        "file_path": file_path,
                        "content": content,
                        "size": len(content)
                    }
                else:
                    raise FileNotFoundError(f"File not found: {file_path}")
            else:
                # Read all code files
                code_files = []
                for root, dirs, files in os.walk(temp_path):
                    # Skip hidden directories
                    dirs[:] = [d for d in dirs if not d.startswith(".")]
                    
                    for file in files:
                        # Only read text files
                        if file.endswith((
                            ".py", ".js", ".jsx", ".ts", ".tsx", ".java",
                            ".cpp", ".c", ".h", ".hpp", ".go", ".rs",
                            ".rb", ".php", ".swift", ".kt", ".scala",
                            ".md", ".txt", ".json", ".yaml", ".yml"
                        )):
                            file_path_full = os.path.join(root, file)
                            rel_path = os.path.relpath(file_path_full, temp_path)
                            
                            try:
                                with open(file_path_full, "r", encoding="utf-8") as f:
                                    content = f.read()
                                
                                code_files.append({
                                    "path": rel_path,
                                    "content": content,
                                    "size": len(content)
                                })
                            except Exception as e:
                                logger.warning(f"Could not read {file_path_full}: {str(e)}")
                
                return {
                    "repo_url": repo_url,
                    "files": code_files,
                    "total_files": len(code_files)
                }
                
        finally:
            # Clean up temporary directory
            if temp_path and os.path.exists(temp_path):
                shutil.rmtree(temp_path, ignore_errors=True)
                logger.info(f"Cleaned up temporary repository: {temp_path}")
        
    except Exception as e:
        logger.error(f"Error reading GitHub repository: {str(e)}", exc_info=True)
        raise


class GitHubTool:
    """
    MCP tool for GitHub repository operations.
    """
    
    def __init__(self):
        """Initialize GitHub tool."""
        self.github_token = settings.github_token
    
    def clone_repo(self, repo_url: str, branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Clone a GitHub repository.
        
        Args:
            repo_url: Repository URL
            branch: Optional branch name
            
        Returns:
            Dictionary with clone result
        """
        try:
            path = clone_github_repo(repo_url, branch)
            return {
                "status": "success",
                "repo_url": repo_url,
                "local_path": path
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "repo_url": repo_url
            }
    
    def read_repo(self, repo_url: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Read repository content.
        
        Args:
            repo_url: Repository URL
            file_path: Optional file path
            
        Returns:
            Dictionary with repository content
        """
        try:
            result = read_github_repo(repo_url, file_path)
            result["status"] = "success"
            return result
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "repo_url": repo_url
            }

