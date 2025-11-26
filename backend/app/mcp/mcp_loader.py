"""
MCP (Model Context Protocol) loader for registering tools in Polix backend.
"""
from typing import List, Dict, Any
from app.mcp.tools.github_tool import GitHubTool
from app.mcp.tools.file_tool import FileTool
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

# Global MCP tools registry
_registered_tools: List[Dict[str, Any]] = []


def register_mcp_tools() -> List[Dict[str, Any]]:
    """
    Register all MCP tools in the backend.
    
    Returns:
        List of registered tool definitions
    """
    global _registered_tools
    
    if _registered_tools:
        return _registered_tools
    
    try:
        logger.info("Registering MCP tools")
        
        tools = []
        
        # Register GitHub tool
        if settings.mcp_enabled:
            github_tool = GitHubTool()
            tools.append({
                "name": "github",
                "type": "github",
                "tool": github_tool,
                "description": "Access GitHub repositories and read code content",
                "functions": {
                    "clone_repo": github_tool.clone_repo,
                    "read_repo": github_tool.read_repo
                }
            })
            logger.info("GitHub tool registered")
        
        # Register File tool
        file_tool = FileTool()
        tools.append({
            "name": "file",
            "type": "file",
            "tool": file_tool,
            "description": "Access local file system and read files/directories",
            "functions": {
                "read_file": file_tool.read_file,
                "list_directory": file_tool.list_directory,
                "read_directory": file_tool.read_directory
            }
        })
        logger.info("File tool registered")
        
        _registered_tools = tools
        logger.info(f"Registered {len(tools)} MCP tools")
        
        return tools
        
    except Exception as e:
        logger.error(f"Error registering MCP tools: {str(e)}", exc_info=True)
        return []


def get_mcp_tool(tool_name: str) -> Dict[str, Any]:
    """
    Get a specific MCP tool by name.
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        Tool definition dictionary
        
    Raises:
        ValueError: If tool not found
    """
    tools = register_mcp_tools()
    
    for tool in tools:
        if tool["name"] == tool_name:
            return tool
    
    raise ValueError(f"MCP tool not found: {tool_name}")


def list_mcp_tools() -> List[str]:
    """
    List all registered MCP tool names.
    
    Returns:
        List of tool names
    """
    tools = register_mcp_tools()
    return [tool["name"] for tool in tools]

