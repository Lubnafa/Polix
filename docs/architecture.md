# Polix Architecture Documentation

## Overview

Polix is a full-stack agentic AI system designed for compliance auditing. It combines RAG (Retrieval-Augmented Generation), LangChain agents, LangGraph workflows, and MCP (Model Context Protocol) tools to provide automated compliance analysis.

## System Architecture

### High-Level Architecture

```
┌─────────────┐
│   Frontend  │ React + Vite
│  (React)    │
└──────┬──────┘
       │ HTTP/REST
       │
┌──────▼──────────────────────────────┐
│         FastAPI Backend             │
├─────────────────────────────────────┤
│  ┌──────────────────────────────┐   │
│  │    API Routes                │   │
│  │  - /health                   │   │
│  │  - /query (RAG)              │   │
│  │  - /agent/audit              │   │
│  └──────────────────────────────┘   │
│                                      │
│  ┌──────────────────────────────┐   │
│  │    LangGraph Workflow        │   │
│  │  - Policy Ingestion          │   │
│  │  - RAG Retrieval             │   │
│  │  - Audit Check               │   │
│  │  - Report Generation         │   │
│  │  - Human Approval            │   │
│  └──────────────────────────────┘   │
│                                      │
│  ┌──────────────────────────────┐   │
│  │    LangChain Agents          │   │
│  │  - Policy Agent              │   │
│  │  - Audit Agent               │   │
│  │  - Report Agent              │   │
│  └──────────────────────────────┘   │
│                                      │
│  ┌──────────────────────────────┐   │
│  │    RAG System                │   │
│  │  - Document Loaders          │   │
│  │  - Text Splitters            │   │
│  │  - Embeddings                │   │
│  │  - Vector Store (ChromaDB)   │   │
│  │  - Retriever                 │   │
│  └──────────────────────────────┘   │
│                                      │
│  ┌──────────────────────────────┐   │
│  │    MCP Tools                 │   │
│  │  - GitHub Tool               │   │
│  │  - File Tool                 │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
       │
       │
┌──────▼──────────────────────────────┐
│    Vector Store (ChromaDB)          │
└─────────────────────────────────────┘
```

## Component Details

### 1. RAG (Retrieval-Augmented Generation) System

The RAG system enables the application to retrieve relevant context from a knowledge base before generating responses.

#### Components:

- **Document Loaders** (`rag/loaders.py`): 
  - Load PDF, TXT, and website documents
  - Use LangChain document loaders (PyPDFLoader, TextLoader, WebBaseLoader)

- **Text Splitters** (`rag/splitters.py`):
  - Split documents into chunks for embedding
  - Recursive character splitting with overlap

- **Embeddings** (`rag/embeddings.py`):
  - OpenAI embeddings (default)
  - Optional local Qwen embeddings
  - Generate vector representations of text

- **Vector Store** (`rag/vectorstore.py`):
  - ChromaDB or FAISS for vector storage
  - Similarity search capabilities
  - Persistent storage

- **Retriever** (`rag/retriever.py`):
  - High-level retrieval interface
  - Score-based filtering
  - Metadata filtering support

### 2. LangChain Agents

Three specialized agents handle different aspects of compliance auditing:

#### Policy Agent (`agents/policy_agent.py`)
- Reads and understands policy documents
- Extracts key requirements and rules
- Answers queries about policies

#### Audit Agent (`agents/audit_agent.py`)
- Compares policy requirements with external data
- Identifies compliance issues
- Calculates compliance scores

#### Report Agent (`agents/report_agent.py`)
- Generates comprehensive audit reports
- Summarizes findings
- Provides recommendations

### 3. LangGraph Workflow

The workflow orchestrates the entire audit process:

```
1. Policy Ingestion Node
   └─> Analyzes policy documents
   
2. RAG Retrieval Node
   └─> Retrieves relevant documents from knowledge base
   
3. Audit Check Node
   └─> Performs compliance audit
   
4. Report Generation Node
   └─> Generates final audit report
   
5. Human Approval Node
   └─> Awaits human approval (future)
```

The workflow uses a state machine pattern where each node processes the current state and updates it for the next node.

### 4. MCP (Model Context Protocol) Tools

MCP tools extend the system's capabilities by providing access to external resources:

#### GitHub Tool (`mcp/tools/github_tool.py`)
- Clone GitHub repositories
- Read repository code content
- Access file contents remotely

#### File Tool (`mcp/tools/file_tool.py`)
- Read local files and directories
- List directory contents
- Access file system resources

### 5. Frontend Architecture

The frontend is built with React and Vite:

#### Components:
- **Sidebar**: Navigation between pages
- **ChatWindow**: Interactive chat interface
- **DocumentUploader**: Upload documents for analysis
- **ComplianceScoreCard**: Display compliance scores
- **AgentTimeline**: Visualize workflow steps

#### Pages:
- **Home** (`/`): Landing page with chat interface
- **Upload** (`/upload`): Document upload page
- **Audit** (`/audit`): Audit execution and results

## Data Flow

### Query Flow:
1. User submits query via frontend
2. Frontend sends request to `/query/` endpoint
3. Backend retrieves relevant documents using RAG
4. Documents are returned to frontend
5. Frontend displays results

### Audit Flow:
1. User initiates audit via frontend
2. Frontend sends request to `/agent/audit` endpoint
3. Backend creates LangGraph workflow
4. Workflow executes nodes sequentially:
   - Policy ingestion
   - RAG retrieval
   - Audit check
   - Report generation
   - Human approval
5. Final results returned to frontend
6. Frontend displays timeline and compliance score

## Technology Stack

### Backend:
- **FastAPI**: Modern Python web framework
- **LangChain**: LLM application framework
- **LangGraph**: State machine for agent workflows
- **ChromaDB**: Vector database
- **OpenAI**: Embeddings and LLM

### Frontend:
- **React**: UI library
- **Vite**: Build tool and dev server
- **React Router**: Client-side routing

### Infrastructure:
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Frontend web server (production)

## Configuration

Configuration is managed through environment variables (see `.env.example`):
- API keys
- Model selection
- Vector store settings
- MCP tool configuration

## Extension Points

The architecture is designed for extensibility:

1. **New Agents**: Add new agent classes in `agents/`
2. **New MCP Tools**: Register tools in `mcp/mcp_loader.py`
3. **New Workflow Nodes**: Add nodes to `graph/workflow_graph.py`
4. **New Document Loaders**: Extend `rag/loaders.py`
5. **New Vector Stores**: Implement interface in `rag/vectorstore.py`

## Future Enhancements

- Human-in-the-loop approval workflows
- Real-time workflow updates via WebSockets
- Multi-tenant support
- Advanced analytics and dashboards
- Integration with more external data sources

