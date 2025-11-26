"""
Configuration management for Polix backend.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    
    # Vector Store Configuration
    vector_store_path: str = Field(
        default="./data/vectorstore",
        env="VECTOR_STORE_PATH"
    )
    vector_store_type: str = Field(
        default="chromadb",
        env="VECTOR_STORE_TYPE"
    )
    
    # Model Configuration
    embedding_model: str = Field(
        default="text-embedding-3-small",
        env="EMBEDDING_MODEL"
    )
    llm_model: str = Field(
        default="gpt-4-turbo-preview",
        env="LLM_MODEL"
    )
    
    # Qwen Local Configuration
    use_qwen_local: bool = Field(
        default=False,
        env="USE_QWEN_LOCAL"
    )
    qwen_model_path: Optional[str] = Field(
        default=None,
        env="QWEN_MODEL_PATH"
    )
    
    # ChromaDB Configuration
    chroma_host: str = Field(default="localhost", env="CHROMA_HOST")
    chroma_port: int = Field(default=8000, env="CHROMA_PORT")
    
    # Application Configuration
    app_name: str = Field(default="Polix", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # MCP Configuration
    mcp_enabled: bool = Field(default=True, env="MCP_ENABLED")
    github_token: Optional[str] = Field(default=None, env="GITHUB_TOKEN")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

