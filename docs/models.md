# Models Used in Polix

This document describes all AI models and their usage in the Polix system.

## Overview

Polix uses OpenAI models by default, with optional support for local Qwen models. All models are configured via environment variables.

## Current Models

### 1. Embedding Model

**Default: `text-embedding-3-small` (OpenAI)**

- **Purpose**: Generates vector embeddings for RAG (Retrieval-Augmented Generation) system
- **Usage**: Used to embed documents and queries for similarity search in the vector store
- **Configuration**: Set via `EMBEDDING_MODEL` environment variable
- **Location**: `backend/app/rag/embeddings.py`
- **Alternative**: Local Qwen embeddings (if `USE_QWEN_LOCAL=true` and `QWEN_MODEL_PATH` is set)

**Features:**
- 1536-dimensional embeddings (text-embedding-3-small)
- Used for document similarity search
- Powers the RAG retrieval system

### 2. Large Language Model (LLM)

**Default: `gpt-4-turbo-preview` (OpenAI)**

- **Purpose**: Powers all LangChain agents for reasoning and text generation
- **Usage**: Used by all three agents:
  - **Policy Agent**: Analyzes and understands policy documents
  - **Audit Agent**: Performs compliance checks and comparisons
  - **Report Agent**: Generates comprehensive audit reports
- **Configuration**: Set via `LLM_MODEL` environment variable
- **Location**: Used in `backend/app/agents/*.py` files

**Model Settings:**
- **Policy Agent**: `temperature=0` (deterministic, precise analysis)
- **Audit Agent**: `temperature=0` (accurate compliance checking)
- **Report Agent**: `temperature=0.7` (more creative report generation)

## Model Configuration

All models are configured in `backend/app/core/config.py` and can be overridden via environment variables in `.env`:

```env
# Embedding Model
EMBEDDING_MODEL=text-embedding-3-small

# LLM Model
LLM_MODEL=gpt-4-turbo-preview

# Optional: Use Local Qwen Models
USE_QWEN_LOCAL=false
QWEN_MODEL_PATH=
```

## Alternative Models

### Qwen Local Models

Polix supports using local Qwen models for embeddings (and potentially LLMs in the future):

1. **Enable**: Set `USE_QWEN_LOCAL=true`
2. **Configure**: Provide path in `QWEN_MODEL_PATH`
3. **Status**: Currently placeholder implementation - needs integration with actual Qwen models

**Note**: The Qwen embedding wrapper is currently a placeholder. To use Qwen models, you'll need to:
- Install Qwen model dependencies
- Implement the actual embedding generation logic
- Configure the model path correctly

## Model Usage by Component

### RAG System
- **Embedding Model**: Converts text to vectors
- **Vector Store**: Stores and retrieves embeddings (ChromaDB/FAISS)
- **Retriever**: Uses embeddings for similarity search

### Agents
- **Policy Agent**: Uses LLM to understand policies
- **Audit Agent**: Uses LLM to check compliance
- **Report Agent**: Uses LLM to generate reports

### LangGraph Workflow
- Orchestrates all agents sequentially
- Each agent uses the configured LLM model
- No additional models required

## Cost Considerations

### OpenAI Models

- **Embeddings**: `text-embedding-3-small` - Cost-effective for large-scale embedding
- **LLM**: `gpt-4-turbo-preview` - More expensive but powerful

**Cost Optimization Tips:**
1. Use `text-embedding-3-small` instead of larger embedding models
2. Consider using `gpt-3.5-turbo` for LLM if cost is a concern (change `LLM_MODEL`)
3. Cache embeddings to avoid re-computation
4. Use local Qwen models for zero-cost inference (once implemented)

## Recommended Models by Use Case

### Development/Testing
```env
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-3.5-turbo
```

### Production (High Accuracy)
```env
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4-turbo-preview
```

### Cost-Optimized
```env
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-3.5-turbo
```

### Local/Private (Future)
```env
USE_QWEN_LOCAL=true
QWEN_MODEL_PATH=/path/to/qwen/model
```

## Model Requirements

### OpenAI Models
- **API Key**: Required (`OPENAI_API_KEY`)
- **Internet**: Required for API access
- **Cost**: Pay-per-use pricing

### Qwen Models
- **Local Storage**: Model files required
- **Hardware**: GPU recommended for performance
- **Cost**: Free (after initial setup)

## Updating Models

To change models, simply update the environment variables:

1. Edit `.env` file
2. Change `EMBEDDING_MODEL` or `LLM_MODEL`
3. Restart the backend service
4. Models will be loaded automatically

No code changes required - the system is designed to be model-agnostic.

